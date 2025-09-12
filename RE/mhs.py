#!/usr/bin/env python3
# Minimal MHS-like scanner + extras:
# - int32 scan/write
# - string scan/write
# - raw bytes write
# - hex/bin dump; write-bin
# - module list; scan offsets (module/base-relative 32-bit)
# - absolute pointer scan (QWORD/DWORD)
# - mapped-file path lookup; dump entire mapped view
#
# Windows-only (uses WinAPI via ctypes)

import ctypes as C
from ctypes import wintypes as W
import sys, struct, os
import zlib

# --- WinAPI constants ---
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ          = 0x0010
PROCESS_VM_WRITE         = 0x0020
PROCESS_VM_OPERATION     = 0x0008

PAGE_READWRITE = 0x04
PAGE_READONLY  = 0x02
PAGE_EXECUTE_READ      = 0x20
PAGE_EXECUTE_READWRITE = 0x40

MEM_COMMIT  = 0x1000
MEM_PRIVATE = 0x20000
MEM_MAPPED  = 0x40000

TH32CS_SNAPMODULE   = 0x00000008
TH32CS_SNAPMODULE32 = 0x00000010

# --- Structures ---
class MEMORY_BASIC_INFORMATION(C.Structure):
    _fields_ = [
        ("BaseAddress",      W.LPVOID),
        ("AllocationBase",   W.LPVOID),
        ("AllocationProtect",W.DWORD),
        ("RegionSize",       C.c_size_t),
        ("State",            W.DWORD),
        ("Protect",          W.DWORD),
        ("Type",             W.DWORD),
    ]

class MODULEENTRY32W(C.Structure):
    _fields_ = [
        ("dwSize", W.DWORD),
        ("th32ModuleID", W.DWORD),
        ("th32ProcessID", W.DWORD),
        ("GlblcntUsage", W.DWORD),
        ("ProccntUsage", W.DWORD),
        ("modBaseAddr", W.LPBYTE),
        ("modBaseSize", W.DWORD),
        ("hModule", W.HMODULE),
        ("szModule", W.WCHAR * 256),
        ("szExePath", W.WCHAR * 260),
    ]

# --- Bindings ---
kernel32 = C.WinDLL("kernel32", use_last_error=True)
psapi    = C.WinDLL("Psapi.dll", use_last_error=True)

OpenProcess       = kernel32.OpenProcess
OpenProcess.argtypes  = [W.DWORD, W.BOOL, W.DWORD]
OpenProcess.restype   = W.HANDLE

ReadProcessMemory  = kernel32.ReadProcessMemory
ReadProcessMemory.argtypes = [W.HANDLE, W.LPCVOID, W.LPVOID, C.c_size_t, C.POINTER(C.c_size_t)]
ReadProcessMemory.restype  = W.BOOL

WriteProcessMemory = kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = [W.HANDLE, W.LPVOID, W.LPCVOID, C.c_size_t, C.POINTER(C.c_size_t)]
WriteProcessMemory.restype  = W.BOOL

VirtualQueryEx    = kernel32.VirtualQueryEx
VirtualQueryEx.argtypes = [W.HANDLE, W.LPCVOID, C.POINTER(MEMORY_BASIC_INFORMATION), C.c_size_t]
VirtualQueryEx.restype  = C.c_size_t

CreateToolhelp32Snapshot = kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.argtypes = [W.DWORD, W.DWORD]
CreateToolhelp32Snapshot.restype  = W.HANDLE

Module32FirstW = kernel32.Module32FirstW
Module32FirstW.argtypes = [W.HANDLE, C.POINTER(MODULEENTRY32W)]
Module32FirstW.restype  = W.BOOL

Module32NextW = kernel32.Module32NextW
Module32NextW.argtypes = [W.HANDLE, C.POINTER(MODULEENTRY32W)]
Module32NextW.restype  = W.BOOL

GetMappedFileNameW = psapi.GetMappedFileNameW
GetMappedFileNameW.argtypes = [W.HANDLE, W.LPVOID, W.LPWSTR, W.DWORD]
GetMappedFileNameW.restype  = W.DWORD

CloseHandle       = kernel32.CloseHandle

# --- Helpers ---
def open_process(pid: int) -> int:
    access = PROCESS_QUERY_INFORMATION | PROCESS_VM_READ | PROCESS_VM_WRITE | PROCESS_VM_OPERATION
    h = OpenProcess(access, False, pid)
    if not h:
        raise OSError(C.get_last_error(), "OpenProcess failed")
    return h

def iter_regions(hproc):
    """Yield (base, size) for committed, readable regions."""
    mbi = MEMORY_BASIC_INFORMATION()
    addr = 0
    sz_mbi = C.sizeof(mbi)
    max_addr = (1 << (8 * C.sizeof(W.LPVOID))) - 1
    while addr < max_addr:
        ret = VirtualQueryEx(hproc, C.c_void_p(addr), C.byref(mbi), sz_mbi)
        if not ret:
            addr += 0x1000
            continue
        protect_ok = mbi.Protect in (PAGE_READONLY, PAGE_READWRITE, PAGE_EXECUTE_READ, PAGE_EXECUTE_READWRITE)
        if (mbi.State & MEM_COMMIT) and (mbi.Type in (MEM_PRIVATE, MEM_MAPPED)) and protect_ok:
            base = int(C.cast(mbi.BaseAddress, C.c_void_p).value or 0)
            size = int(mbi.RegionSize)
            if size > 0:
                yield base, size
        addr = int(C.cast(mbi.BaseAddress, C.c_void_p).value or 0) + int(mbi.RegionSize)

def read_block(hproc, base, size) -> bytes | None:
    buf = (C.c_char * size)()
    read = C.c_size_t(0)
    ok = ReadProcessMemory(hproc, C.c_void_p(base), buf, size, C.byref(read))
    if not ok or read.value == 0:
        return None
    return bytes(buf[:read.value])

def get_region_info(hproc, addr: int) -> MEMORY_BASIC_INFORMATION | None:
    mbi = MEMORY_BASIC_INFORMATION()
    ret = VirtualQueryEx(hproc, C.c_void_p(addr), C.byref(mbi), C.sizeof(mbi))
    return mbi if ret else None

try:
    import lz4.frame
    HAVE_LZ4 = True
except ImportError:
    HAVE_LZ4 = False

def try_decompress(data: bytes) -> bytes | None:
    """
    Try common decompressors (zlib/deflate, LZ4).
    Returns decompressed data or None if nothing matched.
    """
    # --- zlib/deflate ---
    if len(data) >= 2 and data[0] == 0x78 and data[1] in (0x01, 0x9C, 0xDA):
        try:
            return zlib.decompress(data)
        except Exception:
            pass

    # --- LZ4 ---
    if HAVE_LZ4 and len(data) >= 4 and data[:4] == b"\x04\x22\x4D\x18":
        try:
            return lz4.frame.decompress(data)
        except Exception:
            pass

    return None

def dump_region(pid: int, any_address: int, out_path: str, max_len: int | None = None, decompress: bool = False):
    """Dump the memory REGION that contains any_address (MEM_PRIVATE or MEM_MAPPED)."""
    h = open_process(pid)
    try:
        mbi = MEMORY_BASIC_INFORMATION()
        ret = VirtualQueryEx(h, C.c_void_p(any_address), C.byref(mbi), C.sizeof(mbi))
        if not ret:
            raise ValueError("VirtualQueryEx failed for address")

        base = int(C.cast(mbi.BaseAddress, C.c_void_p).value or 0)
        size = int(mbi.RegionSize)
        if max_len is not None:
            size = min(size, max_len)

        buf = (C.c_char * size)()
        read = C.c_size_t(0)
        ok = ReadProcessMemory(h, C.c_void_p(base), buf, size, C.byref(read))
        if not ok or read.value == 0:
            raise OSError(C.get_last_error(), "ReadProcessMemory failed for region")

        data = bytes(buf[:read.value])

        if decompress:
            decomp = try_decompress(data)
            if decomp:
                out_path = out_path.replace(".bin", "_decomp.bin")
                with open(out_path, "wb") as f:
                    f.write(decomp)
                print(f"Decompressed {len(data)} → {len(decomp)} bytes to {out_path}")
                return
            else:
                print("No known compression detected; wrote raw region")

        with open(out_path, "wb") as f:
            f.write(data)
        print(f"Dumped region 0x{base:016X}-0x{base+read.value:016X} ({read.value} bytes) to {out_path}")
    finally:
        CloseHandle(h)

        
# --- Scans ---
def scan_int32(pid: int, value: int, limit_mb: int = 512):
    """Scan for a 4-byte little-endian integer; returns list of addresses."""
    h = open_process(pid)
    try:
        needle = struct.pack("<i", value)
        matches = []
        seen = 0
        limit_bytes = limit_mb * 1024 * 1024
        CHUNK = 8 * 1024 * 1024  # 8MB
        OVERLAP = max(0, len(needle) - 1)

        for base, size in iter_regions(h):
            if seen > limit_bytes:
                break
            offset = 0
            prev_tail = b""
            while offset < size:
                to_read = min(CHUNK, size - offset)
                data = read_block(h, base + offset, to_read)
                if not data:
                    break
                block = prev_tail + data
                i = block.find(needle)
                while i != -1:
                    addr = base + offset - len(prev_tail) + i
                    matches.append(addr)
                    i = block.find(needle, i + 1)
                prev_tail = block[-OVERLAP:] if OVERLAP else b""
                offset += to_read
                seen += len(data)
        return matches
    finally:
        CloseHandle(h)

def scan_bytes(pid: int, needle: bytes, limit_mb: int = 512):
    """Generic byte-pattern scan."""
    h = open_process(pid)
    try:
        matches = []
        seen = 0
        limit_bytes = limit_mb * 1024 * 1024
        CHUNK = 8 * 1024 * 1024
        OVERLAP = max(0, len(needle) - 1)
        for base, size in iter_regions(h):
            if seen > limit_bytes:
                break
            offset = 0
            prev_tail = b""
            while offset < size:
                to_read = min(CHUNK, size - offset)
                data = read_block(h, base + offset, to_read)
                if not data:
                    break
                block = prev_tail + data
                i = block.find(needle)
                while i != -1:
                    matches.append(base + offset - len(prev_tail) + i)
                    i = block.find(needle, i + 1)
                prev_tail = block[-OVERLAP:] if OVERLAP else b""
                offset += to_read
                seen += len(data)
        return matches
    finally:
        CloseHandle(h)

def _encode_string(s: str, encoding: str, nullterm: bool) -> bytes:
    enc = encoding.lower()
    if enc in ("ascii", "ansi"):
        b = s.encode("ascii", errors="ignore")
        return b + (b"\x00" if nullterm else b"")
    elif enc in ("utf-16", "utf-16le", "unicode"):
        b = s.encode("utf-16le")
        return b + (b"\x00\x00" if nullterm else b"")
    elif enc in ("utf8", "utf-8"):
        b = s.encode("utf-8")
        return b + (b"\x00" if nullterm else b"")
    else:
        raise ValueError("Unsupported encoding. Use ascii | utf-16le | utf-8")

def scan_string(pid: int, text: str, encoding: str = "ascii",
                case_insensitive: bool = False, nullterm: bool = False,
                limit_mb: int = 512):
    """Scan for an exact string; returns list of addresses (byte offsets)."""
    h = open_process(pid)
    try:
        needle = _encode_string(text, encoding, nullterm)
        if case_insensitive:
            needle_ci = needle.lower()
        matches = []
        seen = 0
        limit_bytes = limit_mb * 1024 * 1024
        CHUNK = 8 * 1024 * 1024
        OVERLAP = max(0, len(needle) - 1)

        for base, size in iter_regions(h):
            if seen > limit_bytes:
                break
            offset = 0
            prev_tail = b""
            while offset < size:
                to_read = min(CHUNK, size - offset)
                data = read_block(h, base + offset, to_read)
                if not data:
                    break
                block = prev_tail + data
                hay = block.lower() if case_insensitive else block
                ndl = needle_ci if case_insensitive else needle

                i = hay.find(ndl)
                while i != -1:
                    addr = base + offset - len(prev_tail) + i
                    matches.append(addr)
                    i = hay.find(ndl, i + 1)

                prev_tail = block[-OVERLAP:] if OVERLAP else b""
                offset += to_read
                seen += len(data)
        return matches
    finally:
        CloseHandle(h)

# --- Writers ---
def write_string(pid: int, address: int, text: str, encoding: str = "ascii",
                 nullterm: bool = False, mode: str = "exact", length: int | None = None):
    buf = _encode_string(text, encoding, nullterm)
    if mode not in ("exact", "pad-null", "truncate"):
        raise ValueError("mode must be exact | pad-null | truncate")
    if mode in ("pad-null", "truncate") and (length is None or length <= 0):
        raise ValueError("length must be provided for pad-null / truncate modes")

    h = open_process(pid)
    try:
        if mode == "pad-null":
            out = (buf + b"\x00" * max(0, length - len(buf)))[:length]
        elif mode == "truncate":
            out = buf[:length]
        else:
            out = buf

        written = C.c_size_t(0)
        ok = WriteProcessMemory(h, C.c_void_p(address), out, len(out), C.byref(written))
        if not ok or written.value != len(out):
            raise OSError(C.get_last_error(), "WriteProcessMemory failed")
        return True
    finally:
        CloseHandle(h)

def write_bytes(pid: int, address: int, data: bytes):
    h = open_process(pid)
    try:
        written = C.c_size_t(0)
        ok = WriteProcessMemory(h, C.c_void_p(address), data, len(data), C.byref(written))
        if not ok or written.value != len(data):
            raise OSError(C.get_last_error(), "WriteProcessMemory failed")
        return True
    finally:
        CloseHandle(h)

def write_int32(pid: int, address: int, new_value: int):
    h = open_process(pid)
    try:
        buf = struct.pack("<i", new_value)
        written = C.c_size_t(0)
        ok = WriteProcessMemory(h, C.c_void_p(address), buf, len(buf), C.byref(written))
        if not ok or written.value != len(buf):
            raise OSError(C.get_last_error(), "WriteProcessMemory failed")
        return True
    finally:
        CloseHandle(h)

# --- Hex/bin dump ---
def dump_hex(pid: int, address: int, length: int = 64):
    h = open_process(pid)
    try:
        buf = (C.c_char * length)()
        read = C.c_size_t(0)
        ok = ReadProcessMemory(h, C.c_void_p(address), buf, length, C.byref(read))
        if not ok or read.value == 0:
            raise OSError(C.get_last_error(), "ReadProcessMemory failed")

        data = bytes(buf[:read.value])
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hexs = " ".join(f"{b:02X}" for b in chunk)
            ascii_s = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            print(f"0x{address+i:016X}  {hexs:<48}  {ascii_s}")
    finally:
        CloseHandle(h)

def dump_bin(pid: int, address: int, length: int, out_path: str):
    h = open_process(pid)
    try:
        buf = (C.c_char * length)()
        read = C.c_size_t(0)
        ok = ReadProcessMemory(h, C.c_void_p(address), buf, length, C.byref(read))
        if not ok or read.value == 0:
            raise OSError(C.get_last_error(), "ReadProcessMemory failed")
        data = bytes(buf[:read.value])
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"Dumped {len(data)} bytes from 0x{address:016X} to {out_path}")
    finally:
        CloseHandle(h)

def write_bin(pid: int, address: int, in_path: str):
    with open(in_path, "rb") as f:
        data = f.read()
    if not data:
        raise ValueError("Input file is empty")
    h = open_process(pid)
    try:
        written = C.c_size_t(0)
        ok = WriteProcessMemory(h, C.c_void_p(address), data, len(data), C.byref(written))
        if not ok or written.value != len(data):
            raise OSError(C.get_last_error(), "WriteProcessMemory failed")
        print(f"Wrote {len(data)} bytes to 0x{address:016X} from {in_path}")
        return True
    finally:
        CloseHandle(h)

# --- Module enumeration / base resolution ---
def get_module_base(pid: int, module_name: str) -> int | None:
    snap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snap == W.HANDLE(-1).value:
        raise OSError(C.get_last_error(), "CreateToolhelp32Snapshot failed")
    try:
        me = MODULEENTRY32W()
        me.dwSize = C.sizeof(MODULEENTRY32W)
        if not Module32FirstW(snap, C.byref(me)):
            return None
        target = module_name.lower()
        while True:
            if me.szModule.lower() == target:
                return C.addressof(me.modBaseAddr.contents)
            if not Module32NextW(snap, C.byref(me)):
                break
        return None
    finally:
        CloseHandle(snap)

def resolve_base(pid: int, base_or_module: str) -> int:
    s = base_or_module.strip()
    try:
        return int(s, 0)  # allow 0x..., decimal, etc.
    except ValueError:
        b = get_module_base(pid, s)
        if b is None:
            raise ValueError(f"Module not found: {s}")
        return b

def list_modules(pid: int):
    snap = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snap == W.HANDLE(-1).value:
        raise OSError(C.get_last_error(), "CreateToolhelp32Snapshot failed")
    try:
        me = MODULEENTRY32W()
        me.dwSize = C.sizeof(MODULEENTRY32W)
        if not Module32FirstW(snap, C.byref(me)):
            print("No modules.")
            return
        print("Modules:")
        while True:
            base = C.addressof(me.modBaseAddr.contents)
            size = me.modBaseSize
            print(f"  {me.szModule}  base=0x{base:016X}  size=0x{size:X}")
            if not Module32NextW(snap, C.byref(me)):
                break
    finally:
        CloseHandle(snap)

# --- Offset & pointer scans ---
def scan_offset(pid: int, base_or_module: str, abs_addr: int, signed: bool = False):
    """
    Find places that store the 32-bit little-endian offset == abs_addr - base.
    Typical for module-relative pointers.
    """
    base = resolve_base(pid, base_or_module)
    off = abs_addr - base
    if not (-0x8000_0000 <= off <= 0xFFFF_FFFF):
        print(f"Offset 0x{off:X} out of 32-bit range relative to base 0x{base:016X}")
        return []
    needles = [struct.pack("<I", off & 0xFFFF_FFFF)]
    if signed and (-0x8000_0000 <= off <= 0x7FFF_FFFF):
        needles.append(struct.pack("<i", off))
    found = set()
    for ndl in needles:
        for a in scan_bytes(pid, ndl):
            found.add(a)
    found = sorted(found)
    if found:
        print(f"Found {len(found)} matches for offset 0x{off:X} (base=0x{base:016X}):")
        for a in found[:200]:
            print(f"  abs=0x{a:016X}  (stores 0x{off:X})")
        if len(found) > 200:
            print("  ... (truncated)")
    else:
        print("No matches.")
    return found

def scan_ptr(pid: int, abs_addr: int):
    """
    Find places where the absolute pointer is stored (QWORD and DWORD).
    Useful when something stores absolute addresses.
    """
    qword = struct.pack("<Q", abs_addr & 0xFFFF_FFFF_FFFF_FFFF)
    dword = struct.pack("<I", abs_addr & 0xFFFF_FFFF)
    found = set()
    for ndl in (qword, dword):
        for a in scan_bytes(pid, ndl):
            found.add(a)
    found = sorted(found)
    if found:
        print(f"Found {len(found)} absolute pointer matches to 0x{abs_addr:016X}:")
        for a in found[:200]:
            print(f"  0x{a:016X}")
        if len(found) > 200:
            print("  ... (truncated)")
    else:
        print("No matches.")
    return found

# --- Mapped file helpers ---
def get_mapped_filename(pid: int, address: int) -> str | None:
    h = open_process(pid)
    try:
        buf = C.create_unicode_buffer(32768)
        n = GetMappedFileNameW(h, C.c_void_p(address), buf, len(buf))
        return buf.value if n else None
    finally:
        CloseHandle(h)

def collect_mapped_view(pid: int, address: int):
    """
    From any address inside a mapped file, collect the full contiguous MEM_MAPPED view
    sharing the same AllocationBase. Returns (base, total_size).
    """
    h = open_process(pid)
    try:
        mbi = get_region_info(h, address)
        if not mbi or not (mbi.Type & MEM_MAPPED):
            raise ValueError("Address is not inside a MEM_MAPPED region")
        alloc_base = int(C.cast(mbi.AllocationBase, C.c_void_p).value or 0)

        base = alloc_base
        total = 0
        cur = alloc_base
        sz_mbi = C.sizeof(MEMORY_BASIC_INFORMATION)
        info = MEMORY_BASIC_INFORMATION()

        max_addr = (1 << (8 * C.sizeof(W.LPVOID))) - 1
        while cur < max_addr:
            ret = VirtualQueryEx(h, C.c_void_p(cur), C.byref(info), sz_mbi)
            if not ret:
                break
            same_alloc = (int(C.cast(info.AllocationBase, C.c_void_p).value or 0) == alloc_base)
            if not same_alloc or not (info.Type & MEM_MAPPED):
                break
            total += int(info.RegionSize)
            cur += int(info.RegionSize)
        return base, total
    finally:
        CloseHandle(h)

def dump_mapped_file(pid: int, any_address_in_file: int, out_path: str, limit: int | None = None):
    """
    Dump the entire mapped view that contains 'any_address_in_file' to 'out_path'.
    If 'limit' is provided, cap the dump to that many bytes.
    """
    h = open_process(pid)
    try:
        base, total = collect_mapped_view(pid, any_address_in_file)
        if limit is not None:
            total = min(total, limit)
        buf = (C.c_char * total)()
        read = C.c_size_t(0)
        ok = ReadProcessMemory(h, C.c_void_p(base), buf, total, C.byref(read))
        if not ok or read.value == 0:
            raise OSError(C.get_last_error(), "ReadProcessMemory failed on mapped view")
        data = bytes(buf[:read.value])
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"Dumped mapped view from 0x{base:016X} ({read.value} bytes) to {out_path}")
    finally:
        CloseHandle(h)

# --- CLI ---
def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Scan int     : python mhs.py scan-int        <PID> <int_value>")
        print("  Write int    : python mhs.py write-int       <PID> <hex_address> <int_value>")
        print("  Scan str     : python mhs.py scan-str        <PID> <text> [ascii|utf-16le|utf-8] [ci] [null]")
        print("  Write str    : python mhs.py write-str       <PID> <hex_address> <text> [ascii|utf-16le|utf-8] [null] [mode=exact|pad-null|truncate] [length]")
        print("  Write bytes  : python mhs.py write-bytes     <PID> <hex_address> <space-separated-hex>")
        print("  Dump hex     : python mhs.py dump-hex        <PID> <hex_address> [length]")
        print("  Dump bin     : python mhs.py dump-bin        <PID> <hex_address> <length> <out_file>")
        print("  Write bin    : python mhs.py write-bin       <PID> <hex_address> <in_file>")
        print("  List mods    : python mhs.py list-mods       <PID>")
        print("  Scan offset  : python mhs.py scan-offset     <PID> <base|module|0xBASE> <abs_address> [signed]")
        print("  Scan ptr     : python mhs.py scan-ptr        <PID> <abs_address>")
        print("  Mapped path  : python mhs.py mapped-file     <PID> <hex_address>")
        print("  Dump mapped  : python mhs.py dump-mapped     <PID> <hex_address> <out_file> [max_len]")
        print("  Scan+paths   : python mhs.py scan-str-path   <PID> <text> [ascii|utf-16le|utf-8] [ci] [null]")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "scan-int":
        if len(sys.argv) < 4:
            print("Usage: python mhs.py scan-int <PID> <int_value>")
            sys.exit(1)
        pid = int(sys.argv[2], 0); val = int(sys.argv[3], 0)
        addrs = scan_int32(pid, val)
        if not addrs:
            print("No matches.")
        else:
            print(f"Found {len(addrs)} matches:")
            for a in addrs[:200]:
                print(f"  0x{a:016X}")
            if len(addrs) > 200:
                print("  ... (truncated)")

    elif cmd == "write-int":
        if len(sys.argv) < 5:
            print("Usage: python mhs.py write-int <PID> <hex_address> <int_value>")
            sys.exit(1)
        pid = int(sys.argv[2], 0); addr = int(sys.argv[3], 0); val = int(sys.argv[4], 0)
        if write_int32(pid, addr, val):
            print(f"Wrote {val} to 0x{addr:016X}")

    elif cmd == "scan-str":
        if len(sys.argv) < 4:
            print("Usage: python mhs.py scan-str <PID> <text> [ascii|utf-16le|utf-8] [ci] [null]")
            sys.exit(1)
        pid = int(sys.argv[2], 0); text = sys.argv[3]
        enc = sys.argv[4] if len(sys.argv) >= 5 else "ascii"
        ci  = (len(sys.argv) >= 6 and sys.argv[5].lower() == "ci")
        nul = (len(sys.argv) >= 7 and sys.argv[6].lower() == "null")
        addrs = scan_string(pid, text, encoding=enc, case_insensitive=ci, nullterm=nul)
        if not addrs:
            print("No matches.")
        else:
            print(f"Found {len(addrs)} matches:")
            for a in addrs[:200]:
                print(f"  0x{a:016X}")
            if len(addrs) > 200:
                print("  ... (truncated)")

    elif cmd == "write-str":
        if len(sys.argv) < 6:
            print("Usage: python mhs.py write-str <PID> <hex_address> <text> [ascii|utf-16le|utf-8] [null] [mode] [length]")
            sys.exit(1)
        pid = int(sys.argv[2], 0); addr = int(sys.argv[3], 0); text = sys.argv[4]
        enc = sys.argv[5] if len(sys.argv) >= 6 else "ascii"
        nul = (len(sys.argv) >= 7 and sys.argv[6].lower() == "null")
        mode = sys.argv[7] if len(sys.argv) >= 8 else "exact"
        length = int(sys.argv[8], 0) if len(sys.argv) >= 9 else None
        if write_string(pid, addr, text, encoding=enc, nullterm=nul, mode=mode, length=length):
            print(f"Wrote '{text}' ({enc}) to 0x{addr:016X} [{mode}{'' if length is None else f', len={length}'}]")

    elif cmd == "write-bytes":
        if len(sys.argv) < 5:
            print("Usage: python mhs.py write-bytes <PID> <hex_address> <space-separated-hex>")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        addr = int(sys.argv[3], 0)
        hexbytes = "".join(sys.argv[4:]).replace(" ", "")
        data = bytes.fromhex(hexbytes)
        if write_bytes(pid, addr, data):
            print(f"Wrote {len(data)} bytes to 0x{addr:016X}")

    elif cmd == "dump-hex":
        if len(sys.argv) < 4:
            print("Usage: python mhs.py dump-hex <PID> <hex_address> [length]")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        addr = int(sys.argv[3], 0)
        length = int(sys.argv[4], 0) if len(sys.argv) >= 5 else 64
        dump_hex(pid, addr, length)

    elif cmd == "dump-bin":
        if len(sys.argv) < 6:
            print("Usage: python mhs.py dump-bin <PID> <hex_address> <length> <out_file>")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        addr = int(sys.argv[3], 0)
        length = int(sys.argv[4], 0)
        out_file = sys.argv[5]
        dump_bin(pid, addr, length, out_file)

    elif cmd == "write-bin":
        if len(sys.argv) < 5:
            print("Usage: python mhs.py write-bin <PID> <hex_address> <in_file>")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        addr = int(sys.argv[3], 0)
        in_file = sys.argv[4]
        write_bin(pid, addr, in_file)

    elif cmd == "list-mods":
        if len(sys.argv) < 3:
            print("Usage: python mhs.py list-mods <PID>")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        list_modules(pid)

    elif cmd == "scan-offset":
        if len(sys.argv) < 5:
            print("Usage: python mhs.py scan-offset <PID> <base|module|0xBASE> <abs_address> [signed]")
            sys.exit(1)
        pid      = int(sys.argv[2], 0)
        base_or_module = sys.argv[3]
        abs_addr = int(sys.argv[4], 0)
        signed   = (len(sys.argv) >= 6 and sys.argv[5].lower() == "signed")
        scan_offset(pid, base_or_module, abs_addr, signed=signed)

    elif cmd == "scan-ptr":
        if len(sys.argv) < 4:
            print("Usage: python mhs.py scan-ptr <PID> <abs_address>")
            sys.exit(1)
        pid      = int(sys.argv[2], 0)
        abs_addr = int(sys.argv[3], 0)
        scan_ptr(pid, abs_addr)

    elif cmd == "mapped-file":
        if len(sys.argv) < 4:
            print("Usage: python mhs.py mapped-file <PID> <hex_address>")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        addr = int(sys.argv[3], 0)
        path = get_mapped_filename(pid, addr)
        if path:
            print(path)
        else:
            print("No mapped file for this address.")

    elif cmd == "dump-mapped":
        if len(sys.argv) < 5:
            print("Usage: python mhs.py dump-mapped <PID> <hex_address> <out_file> [max_len]")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        addr = int(sys.argv[3], 0)
        out_file = sys.argv[4]
        max_len = int(sys.argv[5], 0) if len(sys.argv) >= 6 else None
        dump_mapped_file(pid, addr, out_file, limit=max_len)
        
    elif cmd == "dump-region":
        if len(sys.argv) < 5:
            print("Usage: python mhs.py dump-region <PID> <hex_address> <out_file> [max_len] [decomp]")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        addr = int(sys.argv[3], 0)
        out_file = sys.argv[4]
        max_len = int(sys.argv[5], 0) if len(sys.argv) >= 6 else None
        decompress = (len(sys.argv) >= 7 and sys.argv[6].lower() in ("1","true","yes","decomp"))
        dump_region(pid, addr, out_file, max_len, decompress)


    elif cmd == "scan-str-path":
        if len(sys.argv) < 4:
            print("Usage: python mhs.py scan-str-path <PID> <text> [ascii|utf-16le|utf-8] [ci] [null]")
            sys.exit(1)
        pid = int(sys.argv[2], 0)
        text = sys.argv[3]
        enc  = sys.argv[4] if len(sys.argv) >= 5 else "ascii"
        ci   = (len(sys.argv) >= 6 and sys.argv[5].lower() == "ci")
        nul  = (len(sys.argv) >= 7 and sys.argv[6].lower() == "null")
        addrs = scan_string(pid, text, encoding=enc, case_insensitive=ci, nullterm=nul)
        if not addrs:
            print("No matches.")
        else:
            print(f"Found {len(addrs)} matches:")
            for a in addrs[:200]:
                path = get_mapped_filename(pid, a) or ""
                print(f"  0x{a:016X}  {path}")
            if len(addrs) > 200:
                print("  ... (truncated)")

    else:
        print("Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
