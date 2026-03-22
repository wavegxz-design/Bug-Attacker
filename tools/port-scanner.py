#!/usr/bin/env python3
"""
Bug-Attacker — Port Scanner Module
FIX: Threading for speed (50 concurrent threads)
FIX: Input validation — range, IP format
FIX: Per-socket timeout (was using global setdefaulttimeout)
FIX: Results sorted and formatted cleanly
FIX: str|None union type → Optional[str] (Python 3.8+ compat)
"""

import sys
import socket
import threading
from datetime import datetime
from queue import Queue
from typing import Optional, Tuple

# ── COLORS ─────────────────────────────────────────────────────────
G  = "\033[38;5;46m"
GD = "\033[38;5;34m"
R  = "\033[38;5;196m"
CY = "\033[38;5;51m"
WH = "\033[1;97m"
YL = "\033[38;5;226m"
DM = "\033[38;5;240m"
RS = "\033[0m"

BANNER = f"""
{GD}  ┌──────────────────────────────────────────┐
{GD}  │{G}  Bug-Attacker — Port Scanner            {GD}│
{GD}  │{DM}  Threaded · Authorized use only        {GD}│
{GD}  └──────────────────────────────────────────┘{RS}
"""

COMMON_PORTS = {
    21:"FTP", 22:"SSH", 23:"Telnet", 25:"SMTP",
    53:"DNS", 80:"HTTP", 110:"POP3", 143:"IMAP",
    443:"HTTPS", 445:"SMB", 3306:"MySQL",
    3389:"RDP", 5432:"PostgreSQL", 6379:"Redis",
    8080:"HTTP-Alt", 8443:"HTTPS-Alt", 27017:"MongoDB"
}

open_ports   = []
ports_lock   = threading.Lock()
print_lock   = threading.Lock()

def validate_ip(host: str) -> Optional[str]:  # FIX: str|None requires Python 3.10+ → Optional
    """Resolve hostname or validate IP. Returns resolved IP or None."""
    try:
        return socket.gethostbyname(host.strip())
    except socket.gaierror:
        return None

def validate_range(raw: str, min_p: int = 1, max_p: int = 65535) -> Optional[Tuple[int,int]]:  # FIX: added return type
    """Parse 'start-end' or single port. Returns (start, end) or None."""
    raw = raw.strip()
    try:
        if "-" in raw:
            parts = raw.split("-", 1)
            start, end = int(parts[0]), int(parts[1])
        else:
            start = end = int(raw)
        if not (min_p <= start <= max_p and min_p <= end <= max_p and start <= end):
            return None
        return start, end
    except ValueError:
        return None

def scan_port(host: str, port: int, timeout: float = 0.8) -> bool:
    """Return True if port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except (socket.error, OSError):
        return False

def worker(host: str, q: Queue) -> None:
    while not q.empty():
        try:
            port = q.get_nowait()
        except Exception:
            break
        if scan_port(host, port):
            service = COMMON_PORTS.get(port, "Unknown")
            with ports_lock:
                open_ports.append((port, service))
            with print_lock:
                print(G + f"  [OPEN] {port:5d}  →  {service}" + RS)
        q.task_done()

def main():
    print(BANNER)

    # ── Target input ───────────────────────────────────────────────
    try:
        raw_host = input(WH + "  Target IP or hostname: " + RS).strip()
    except (KeyboardInterrupt, EOFError):
        return

    host = validate_ip(raw_host)
    if not host:
        print(R + f"  [!] Cannot resolve '{raw_host}'. Check the address." + RS)
        return

    # ── Port range input ───────────────────────────────────────────
    print(DM + "  Examples: 80  |  1-1000  |  1-65535" + RS)
    try:
        raw_range = input(WH + "  Port range: " + RS).strip()
    except (KeyboardInterrupt, EOFError):
        return

    result = validate_range(raw_range)
    if not result:
        print(R + "  [!] Invalid range. Use format: 1-1000 or single port like 80" + RS)
        return
    start_port, end_port = result
    total = end_port - start_port + 1

    # ── Thread count ───────────────────────────────────────────────
    MAX_THREADS = min(100, total)
    open_ports.clear()
    q: Queue = Queue()
    for p in range(start_port, end_port + 1):
        q.put(p)

    # ── Scan ───────────────────────────────────────────────────────
    print(GD + f"\n  ┌─────────────────────────────────────────┐")
    print(GD + f"  │  Target   : {CY}{host:<28}{GD}│")
    print(GD + f"  │  Range    : {YL}{start_port} → {end_port:<26}{GD}│")
    print(GD + f"  │  Threads  : {WH}{MAX_THREADS:<28}{GD}│")
    print(GD + f"  │  Started  : {WH}{datetime.now().strftime('%H:%M:%S'):<28}{GD}│")
    print(GD + f"  └─────────────────────────────────────────┘{RS}\n")

    try:
        threads = []
        for _ in range(MAX_THREADS):
            t = threading.Thread(target=worker, args=(host, q), daemon=True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print(GD + "\n  [*] Scan interrupted." + RS)

    # ── Results ────────────────────────────────────────────────────
    print(GD + f"\n  ┌─────────────────────────────────────────┐")
    print(GD + f"  │  Scan complete — {G}{len(open_ports)} open port(s) found{' '*(12-len(str(len(open_ports))))}{GD}│")
    print(GD + f"  │  Finished : {WH}{datetime.now().strftime('%H:%M:%S'):<28}{GD}│")
    print(GD + f"  └─────────────────────────────────────────┘{RS}")

    if open_ports:
        print(GD + "\n  OPEN PORTS:" + RS)
        for port, svc in sorted(open_ports):
            print(G + f"    {port:5d}  {DM}│{RS}  {svc}")
    else:
        print(DM + "\n  No open ports found in the specified range.\n" + RS)


if __name__ == "__main__":
    main()
