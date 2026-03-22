#!/usr/bin/env python3
"""
Bug-Attacker — Subdomain Scanner Module
FIX: Threading (50 concurrent) — was sequential, very slow
FIX: Timeout on each request
FIX: Input validation
FIX: Status code display — shows 200, 301, 403 etc.
FIX: Results saved to file optionally
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
{GD}  │{G}  Bug-Attacker — Subdomain Scanner       {GD}│
{GD}  │{DM}  Threaded · Authorized use only        {GD}│
{GD}  └──────────────────────────────────────────┘{RS}
"""

found      = []
found_lock = threading.Lock()
print_lock = threading.Lock()

STATUS_COLOR = {
    200: G, 201: G, 204: G,
    301: YL, 302: YL, 307: YL, 308: YL,
    401: CY, 403: CY,
    404: DM, 500: R, 503: R,
}

def check_subdomain(domain: str, sub: str, q: Queue) -> None:
    while True:
        try:
            word = q.get_nowait()
        except Exception:
            break
        url = f"https://{word}.{domain}"
        try:
            r = requests.get(url, timeout=4, verify=False,
                             allow_redirects=True,
                             headers={"User-Agent": "Bug-Attacker/1.0 (authorized recon)"})
            color = STATUS_COLOR.get(r.status_code, WH)
            with found_lock:
                found.append((url, r.status_code))
            with print_lock:
                print(color + f"  [+] {r.status_code}  {url}" + RS)
        except requests.exceptions.SSLError:
            # Try HTTP fallback
            try:
                url_http = f"http://{word}.{domain}"
                r = requests.get(url_http, timeout=4, allow_redirects=True,
                                 headers={"User-Agent": "Bug-Attacker/1.0"})
                color = STATUS_COLOR.get(r.status_code, WH)
                with found_lock:
                    found.append((url_http, r.status_code))
                with print_lock:
                    print(color + f"  [+] {r.status_code}  {url_http}  {DM}(http)" + RS)
            except Exception:
                pass
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout):
            pass
        except Exception:
            pass
        finally:
            q.task_done()


def load_wordlist(path: str) -> list:
    if not os.path.isfile(path):
        return []
    with open(path, "r", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    print(BANNER)

    # ── Domain ────────────────────────────────────────────────────
    try:
        domain = input(WH + "  Target domain (e.g. example.com): " + RS).strip()
    except (KeyboardInterrupt, EOFError):
        return

    domain = domain.replace("https://", "").replace("http://", "").strip("/")
    if not domain or "." not in domain:
        print(R + "  [!] Invalid domain. Use format: example.com" + RS)
        return

    # ── Wordlist ──────────────────────────────────────────────────
    default_list = os.path.join(os.path.dirname(__file__), "..", "wordlists", "subdomains.txt")
    print(DM + f"  Default wordlist: wordlists/subdomains.txt" + RS)
    try:
        custom = input(WH + "  Custom wordlist path (Enter to use default): " + RS).strip()
    except (KeyboardInterrupt, EOFError):
        return

    wl_path = custom if custom else default_list
    words = load_wordlist(wl_path)
    if not words:
        print(R + f"  [!] Wordlist empty or not found: {wl_path}" + RS)
        return

    found.clear()
    q: Queue = Queue()
    for w in words:
        q.put(w)

    THREADS = min(50, len(words))
    print(GD + f"\n  ┌──────────────────────────────────────────┐")
    print(GD + f"  │  Target  : {CY}{domain:<30}{GD}│")
    print(GD + f"  │  Words   : {WH}{len(words):<30}{GD}│")
    print(GD + f"  │  Threads : {WH}{THREADS:<30}{GD}│")
    print(GD + f"  │  Started : {YL}{datetime.now().strftime('%H:%M:%S'):<30}{GD}│")
    print(GD + f"  └──────────────────────────────────────────┘{RS}\n")

    try:
        threads = []
        for _ in range(THREADS):
            t = threading.Thread(target=check_subdomain,
                                 args=(domain, domain, q), daemon=True)
            t.start()
            threads.append(t)
        q.join()
    except KeyboardInterrupt:
        print(GD + "\n  [*] Scan interrupted." + RS)

    # ── Results ───────────────────────────────────────────────────
    print(GD + f"\n  ┌──────────────────────────────────────────┐")
    print(GD + f"  │  Found {G}{len(found)} subdomain(s){' '*(24-len(str(len(found))))}{GD}│")
    print(GD + f"  └──────────────────────────────────────────┘{RS}")

    if found:
        try:
            save = input(DM + "\n  Save results to file? (y/n): " + RS).strip().lower()
        except (KeyboardInterrupt, EOFError):
            save = "n"
        if save == "y":
            out = f"subdomains_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(out, "w") as f:
                for url, code in sorted(found):
                    f.write(f"{code}  {url}\n")
            print(G + f"  [✔] Saved to {out}" + RS)


if __name__ == "__main__":
    main()
