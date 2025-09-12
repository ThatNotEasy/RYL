#!/usr/bin/env python3
# wpe.py — Pure-Python multi-port TCP proxy + PID connection monitor (authorized testing only)
# Features:
# - Map multiple ports: --map [bind_host:]bind_port:target_host:target_port  (repeatable)
# - Hexdump logging per direction (client->server / server->client)
# - Optional ASCII/hex find/replace rules per direction (cs/sc/both)
# - Read-only PID attach: --attach-pid PID (shows that process's TCP connections)
# - Optional --spawn "cmd args" to launch a program and auto-attach
# - Tunables: --idle (per-conn inactivity), --conn-timeout (upstream connect timeout)
#
# Notes:
# - This does NOT hook or hijack existing sockets. To see payloads, your client must
#   connect THROUGH this proxy (e.g., hostname→127.0.0.1 via hosts or app config).
# - Use only on systems/traffic you are authorized to test.

import argparse, asyncio, binascii, logging, os, sys, time, signal, shlex
from typing import List, Tuple, Optional

LOG_DIR = "proxy_logs"

def setup_logging(v: int):
    level = logging.WARNING if v == 0 else (logging.INFO if v == 1 else logging.DEBUG)
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

def addr_str(addr) -> str:
    """Return 'ip:port' for psutil addr (supports tuple or .ip/.port objects)."""
    if not addr:
        return "?:0"
    ip = getattr(addr, "ip", None)
    port = getattr(addr, "port", None)
    if ip is not None and port is not None:
        return f"{ip}:{port}"
    try:
        ip, port = addr
        return f"{ip}:{port}"
    except Exception:
        return "?:0"

def hexdump(b: bytes, w: int = 16) -> str:
    out = []
    for i in range(0, len(b), w):
        chunk = b[i:i+w]
        hexp = " ".join(f"{x:02X}" for x in chunk)
        ascp = "".join(chr(x) if 32 <= x < 127 else "." for x in chunk)
        out.append(f"{i:08X}  {hexp:<{w*3}}  |{ascp}|")
    return "\n".join(out)

def parse_bytes(spec: str) -> bytes:
    # ascii:TEXT  or  hex:de ad be ef
    if spec.startswith("ascii:"):
        return spec[6:].encode()
    if spec.startswith("hex:"):
        s = spec[4:].replace(" ", "")
        try:
            return binascii.unhexlify(s)
        except binascii.Error:
            raise SystemExit(f"Bad hex: {s}")
    raise SystemExit("Patterns must start with ascii: or hex:")

def parse_map(s: str) -> Tuple[str,int,str,int]:
    parts = s.split(":")
    if len(parts) == 3:
        bh = "127.0.0.1"; bp, th, tp = parts
    elif len(parts) == 4:
        bh, bp, th, tp = parts
    else:
        raise SystemExit("Map must be [bind_host:]bind_port:target_host:target_port")
    return bh, int(bp), th, int(tp)

class Rule:
    def __init__(self, direction: str, find_b: bytes, repl_b: bytes, count: int):
        self.dir = direction  # cs/sc/both
        self.find = find_b
        self.repl = repl_b
        self.count = count  # 0 = unlimited

    def applies(self, is_cs: bool) -> bool:
        return self.dir == "both" or (self.dir == "cs" and is_cs) or (self.dir == "sc" and not is_cs)

    def apply(self, data: bytes) -> Tuple[bytes,int]:
        if not self.find:
            return data, 0
        n = -1 if self.count == 0 else self.count
        out = data.replace(self.find, self.repl, n)
        changed = 0 if out == data else (data.count(self.find) if n == -1 else min(data.count(self.find), self.count))
        return out, changed

class ConnLog:
    def __init__(self, tag: str, cid: int):
        os.makedirs(os.path.join(LOG_DIR, tag), exist_ok=True)
        base = os.path.join(LOG_DIR, tag, f"{int(time.time())}_{cid}")
        self.cs = base + "_cs.log"
        self.sc = base + "_sc.log"

    def _w(self, path: str, label: str, data: bytes):
        with open(path, "ab") as f:
            f.write(f"\n=== {time.strftime('%H:%M:%S')} {label} {len(data)} bytes ===\n".encode())
            f.write(hexdump(data).encode() + b"\n")

    def cs_log(self, data: bytes): self._w(self.cs, "C->S", data)
    def sc_log(self, data: bytes): self._w(self.sc, "S->C", data)

class Proxy:
    def __init__(self, bh: str, bp: int, th: str, tp: int,
                 rules: List[Rule], tag: str, idle: float, conn_timeout: float):
        self.bh, self.bp, self.th, self.tp = bh, bp, th, tp
        self.rules, self.tag, self.idle = rules, tag, idle
        self.conn_timeout = conn_timeout
        self.srv: Optional[asyncio.base_events.Server] = None
        self.cid = 0

    async def start(self):
        self.srv = await asyncio.start_server(self._accept, self.bh, self.bp)
        addrs = ", ".join(str(s.getsockname()) for s in self.srv.sockets or [])
        logging.info("[%s] listening on %s -> %s:%d", self.tag, addrs, self.th, self.tp)

    async def stop(self):
        if self.srv:
            self.srv.close()
            await self.srv.wait_closed()

    async def _accept(self, cr: asyncio.StreamReader, cw: asyncio.StreamWriter):
        self.cid += 1
        cid = self.cid
        log = ConnLog(self.tag, cid)
        try:
            sr, sw = await asyncio.wait_for(
                asyncio.open_connection(self.th, self.tp),
                timeout=self.conn_timeout
            )
        except asyncio.TimeoutError:
            logging.warning("[%s#%d] upstream connect timed out after %.1fs",
                            self.tag, cid, self.conn_timeout)
            cw.close(); await cw.wait_closed(); return
        except Exception as e:
            logging.warning("[%s#%d] upstream connect failed: %r", self.tag, cid, e)
            cw.close(); await cw.wait_closed(); return

        async def pump(src, dst, is_cs: bool):
            try:
                while True:
                    data = await asyncio.wait_for(src.read(65536), timeout=self.idle)
                    if not data:
                        break
                    (log.cs_log if is_cs else log.sc_log)(data)
                    for r in self.rules:
                        if r.applies(is_cs):
                            data, changed = r.apply(data)
                            if changed:
                                logging.info("[%s#%d] %s replaced %d occurrence(s)",
                                             self.tag, cid, "C->S" if is_cs else "S->C", changed)
                    dst.write(data); await dst.drain()
            except asyncio.TimeoutError:
                logging.info("[%s#%d] %s idle timeout", self.tag, cid, "C->S" if is_cs else "S->C")
            finally:
                try: dst.close()
                except: pass

        a = asyncio.create_task(pump(cr, sw, True))
        b = asyncio.create_task(pump(sr, cw, False))
        await asyncio.gather(a, b, return_exceptions=True)
        try: cw.close(); await cw.wait_closed()
        except: pass
        try: sw.close(); await sw.wait_closed()
        except: pass
        logging.info("[%s#%d] closed", self.tag, cid)

def build_rules(args) -> List[Rule]:
    rules = []
    if args.find or args.replace:
        if not (args.find and args.replace) or len(args.find) != len(args.replace):
            raise SystemExit("Match --find and --replace counts.")
        for i, (f, r) in enumerate(zip(args.find, args.replace)):
            direction = (args.direction[i] if args.direction and i < len(args.direction) else "both").lower()
            count = int(args.count[i]) if args.count and i < len(args.count) else 0
            rules.append(Rule(direction, parse_bytes(f), parse_bytes(r), count))
    return rules

# ---------------------------
# Optional PID monitor helpers
# ---------------------------
try:
    import psutil  # type: ignore
    _HAS_PSUTIL = True
except Exception:
    _HAS_PSUTIL = False

async def monitor_pid(pid: int, refresh: float = 1.0):
    """
    Read-only, live view of a PID's TCP connections (needs psutil).
    Prints a compact table whenever something changes.
    """
    if not _HAS_PSUTIL:
        logging.warning("--attach-pid requires 'psutil' (pip install psutil). Skipping.")
        return

    try:
        proc = psutil.Process(pid)
    except Exception as e:
        logging.error("Could not open PID %s: %s", pid, e)
        return

    try:
        name = proc.name()
    except Exception:
        name = ""

    last = set()
    logging.info("Monitoring PID %d (%s) TCP connections...", pid, name or "?")
    while True:
        rows = set()
        try:
            for c in proc.net_connections(kind="tcp"):
                laddr = addr_str(c.laddr)
                raddr = addr_str(c.raddr)
                rows.add((laddr, raddr, c.status))
        except psutil.NoSuchProcess:
            logging.info("PID %d exited.", pid)
            return
        except Exception as e:
            logging.debug("monitor error: %s", e)

        if rows != last:
            last = rows
            print("\nPID", pid, name or "")
            print(" Local                -> Remote               | State")
            print("-----------------------------------------------------------")
            for laddr, raddr, st in sorted(rows):
                print(f" {laddr:<20} -> {raddr:<20} | {st}")
            print("(Connect your client through this proxy to see payloads.)")

        await asyncio.sleep(refresh)

async def spawn_and_get_pid(cmdline: str) -> Optional[int]:
    """
    Spawn a child program (non-blocking) and return its PID.
    This does NOT inject or change the child's networking.
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            *shlex.split(cmdline),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL
        )
        logging.info("Spawned '%s' with PID %d", cmdline, proc.pid)
        return proc.pid
    except Exception as e:
        logging.error("Failed to spawn: %s", e)
        return None

async def main_async():
    p = argparse.ArgumentParser(description="Safe TCP proxy + PID monitor (authorized use only)")
    p.add_argument("--map", action="append", help="[bind_host:]bind_port:target_host:target_port (repeatable)")
    p.add_argument("--find", action="append", help="ascii:TEXT or hex:DE AD BE EF (repeatable)")
    p.add_argument("--replace", action="append", help="ascii:TEXT or hex:BA AD F0 0D (repeatable)")
    p.add_argument("--direction", action="append", help="cs | sc | both (repeatable; default both)")
    p.add_argument("--count", action="append", help="max replacements per chunk (repeatable; default 0=all)")
    p.add_argument("--conn-timeout", type=float, default=15.0, help="Upstream connect timeout seconds")
    p.add_argument("--idle", type=float, default=300.0, help="Idle timeout seconds per stream")
    p.add_argument("-v", action="count", default=0)

    # Attach/spawn
    p.add_argument("--attach-pid", type=int, help="Monitor a process's TCP connections (read-only; requires psutil)")
    p.add_argument("--spawn", help="Spawn a program and auto-attach (quote the whole command)")

    args = p.parse_args()
    setup_logging(args.v)

    # Build rules
    rules = build_rules(args)

    # Start proxies (if any)
    proxies: List[Proxy] = []
    if args.map:
        for m in args.map:
            bh, bp, th, tp = parse_map(m)
            tag = f"{bh.replace('.','_')}_{bp}_to_{th.replace('.','_')}_{tp}"
            proxies.append(Proxy(bh, bp, th, tp, rules, tag, args.idle, args.conn_timeout))

        for px in proxies:
            try:
                await px.start()
            except OSError as e:
                logging.error("Bind failed on %s:%d — %s", px.bh, px.bp, e); sys.exit(1)
        logging.info("Proxy running. Ctrl+C to stop.")

    # spawn → attach
    tasks = []
    if args.spawn:
        pid = await spawn_and_get_pid(args.spawn)
        if pid:
            args.attach_pid = pid

    if args.attach_pid:
        tasks.append(asyncio.create_task(monitor_pid(args.attach_pid)))

    if not proxies and not tasks:
        print("Nothing to do. Provide --map and/or --attach-pid. Use -h for help.")
        return

    # Wait for signal
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, stop.set)
        except NotImplementedError:
            pass

    try:
        await stop.wait()
    finally:
        for t in tasks:
            t.cancel()
        for px in proxies:
            await px.stop()

if __name__ == "__main__":
    if sys.platform.startswith("win"):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore[attr-defined]
        except Exception:
            pass
    asyncio.run(main_async())
