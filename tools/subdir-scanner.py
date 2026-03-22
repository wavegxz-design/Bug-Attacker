#!/usr/bin/env python3
"""
Bug-Attacker — Subdirectory Scanner Module
FIX: Threading (50 concurrent) — was sequential
FIX: Timeout per request
FIX: Shows status codes (200, 301, 403) not just 200
FIX: Input validation + URL normalization
FIX: Results export
"""

import sys
import os
import threading
import requests
from queue import Queue
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
{GD}  │{G}  Bug-Attacker — Subdirectory Scanner    {GD}│
{GD}  │{DM}  Threaded · Authorized use only        {GD}│
{GD}  └──────────────────────────────────────────┘{RS}
"""

found      = []
found_lock = threading.Lock()
print_lock = threading.Lock()

STATUS_COLOR = {
    200: G, 201: G, 204: G,
    301: YL, 302: YL, 307: YL,
    401: CY, 403: CY,
    404: DM, 500: R,
}

INTERESTING = {200, 201, 204, 301, 302, 307, 401, 403}


def check_dir(base_url: str, q: Queue) -> None:
    while True:
        try:
            word = q.get_nowait()
        except Exception:
            break
        url = f"{base_url}/{word}"
        try:
            r = requests.get(
                url, timeout=4, verify=False,
                allow_redirects=False,
                headers={"User-Agent": "Bug-Attacker/1.0 (authorized recon)"}
            )
            if r.status_code in INTERESTING:
                color = STATUS_COLOR.get(r.status_code, WH)
                with found_lock:
                    found.append((url, r.status_code))
                with print_lock:
                    print(color + f"  [{r.status_code}] {url}" + RS)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.SSLError):
            pass
        except Exception:
            pass
        finally:
            q.task_done()


def load_wordlist(path: str) -> list:
    if not os.path.isfile(path):
        return []
    with open(path, "r", errors="ignore") as f:
        return [ln.strip().strip("/") for ln in f if ln.strip()]


def normalize_url(raw: str) -> str:
    raw = raw.strip().rstrip("/")
    if not raw.startswith(("http://", "https://")):
        raw = "https://" + raw
    return raw


def main():
    print(BANNER)

    try:
        raw = input(WH + "  Target URL or domain (e.g. example.com): " + RS).strip()
    except (KeyboardInterrupt, EOFError):
        return

    if not raw:
        print(R + "  [!] Empty input." + RS)
        return

    base_url = normalize_url(raw)
    default_list = os.path.join(os.path.dirname(__file__), "..", "wordlists", "directories.txt")
    print(DM + f"  Default wordlist: wordlists/directories.txt" + RS)

    try:
        custom = input(WH + "  Custom wordlist path (Enter to use default): " + RS).strip()
    except (KeyboardInterrupt, EOFError):
        return

    wl_path = custom if custom else default_list
    words = load_wordlist(wl_path)
    if not words:
        print(R + f"  [!] Wordlist empty or not found: {wl_path}" + RS)
        print(DM + "  Place your wordlist at: wordlists/directories.txt" + RS)
        return

    found.clear()
    q: Queue = Queue()
    for w in words:
        q.put(w)

    THREADS = min(50, len(words))

    print(GD + f"\n  ┌──────────────────────────────────────────┐")
    print(GD + f"  │  Target  : {CY}{base_url[:30]:<30}{GD}│")
    print(GD + f"  │  Words   : {WH}{len(words):<30}{GD}│")
    print(GD + f"  │  Threads : {WH}{THREADS:<30}{GD}│")
    print(GD + f"  │  Started : {YL}{datetime.now().strftime('%H:%M:%S'):<30}{GD}│")
    print(GD + f"  └──────────────────────────────────────────┘{RS}\n")
    print(DM + "  Showing: 200 ✓  301/302 ⟶  401/403 🔒  (hiding 404s)\n" + RS)

    try:
        threads = []
        for _ in range(THREADS):
            t = threading.Thread(target=check_dir, args=(base_url, q), daemon=True)
            t.start()
            threads.append(t)
        q.join()
    except KeyboardInterrupt:
        print(GD + "\n  [*] Scan interrupted." + RS)

    print(GD + f"\n  ┌──────────────────────────────────────────┐")
    print(GD + f"  │  Found {G}{len(found)} interesting path(s){' '*(19-len(str(len(found))))}{GD}│")
    print(GD + f"  └──────────────────────────────────────────┘{RS}")

    if found:
        try:
            save = input(DM + "\n  Save results? (y/n): " + RS).strip().lower()
        except (KeyboardInterrupt, EOFError):
            save = "n"
        if save == "y":
            out = f"dirs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(out, "w") as f:
                for url, code in sorted(found):
                    f.write(f"{code}  {url}\n")
            print(G + f"  [✔] Saved to {out}" + RS)


if __name__ == "__main__":
    main()
