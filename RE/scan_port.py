#!/usr/bin/env python3
import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

COMMON_PORTS = [
    21,22,23,25,53,80,110,135,139,143,443,445,
    3306,3389,5432,5900,8080,8443
]

def scan_port(host: str, port: int, timeout: float = 1.0) -> tuple[int, bool]:
    """Attempt to connect to a port; return (port, True/False)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return port, (result == 0)
    except Exception:
        return port, False

def main():
    parser = argparse.ArgumentParser(description="Simple Python3 Port Scanner")
    parser.add_argument("host", help="Target host/IP to scan")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds (default: 1.0)")
    parser.add_argument("--common", action="store_true", help="Scan only common ports instead of a range")
    args = parser.parse_args()

    host, start, end = args.host, args.start, args.end
    ports = COMMON_PORTS if args.common else list(range(start, end+1))

    print(Fore.YELLOW + f"[*] Scanning {host} from port {ports[0]} to {ports[-1]}..."
          if not args.common else f"[*] Scanning {host} (common ports only)...")

    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(scan_port, host, port, args.timeout) for port in ports]
        for f in as_completed(futures):
            port, is_open = f.result()
            if is_open:
                print(Fore.GREEN + f"[+] Port {port} is OPEN")
                open_ports.append(port)

    if open_ports:
        print(Style.BRIGHT + Fore.GREEN + "\nOpen ports: " + ", ".join(map(str, sorted(open_ports))))
    else:
        print(Style.BRIGHT + Fore.RED + "\nNo open ports found.")

if __name__ == "__main__":
    main()
