#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║   Bug-Attacker — Security Recon Toolkit                        ║
# ║   Maintained by : krypthane | wavegxz-design                   ║
# ║   GitHub        : github.com/wavegxz-design                    ║
# ║   Telegram      : t.me/Skrylakk                                ║
# ║   Email         : Workernova@proton.me                         ║
# ║   Location      : Mexico 🇲🇽 UTC-6                             ║
# ║                                                                 ║
# ║   v1.0 — krypthane:                                            ║
# ║   - [FIX] API keys moved to environment variables              ║
# ║   - [FIX] os.system() replaced with subprocess (safe)          ║
# ║   - [FIX] Input validation on all modules                      ║
# ║   - [FIX] Threading added to scanners                          ║
# ║   - [FIX] Timeout handling everywhere                          ║
# ║   - [NEW] Redesigned interface — clean box UI                  ║
# ║   Authorized use only. Ethical hacking only.                   ║
# ╚══════════════════════════════════════════════════════════════════╝

import os
import sys
import time
import subprocess
import platform
from datetime import datetime

# ── COLOR PALETTE ──────────────────────────────────────────────────
G  = "\033[38;5;46m"    # bright green
GD = "\033[38;5;34m"    # dark green
R  = "\033[38;5;196m"   # red
CY = "\033[38;5;51m"    # cyan
WH = "\033[1;97m"       # white bold
DM = "\033[38;5;240m"   # dim gray
YL = "\033[38;5;226m"   # yellow
MG = "\033[38;5;213m"   # magenta
RS = "\033[0m"          # reset

# ── HELPERS ────────────────────────────────────────────────────────
def clear():
    try:
        os.system("cls" if os.name == "nt" else "clear")
    except Exception:
        pass

def banner():
    clear()
    now = datetime.now().strftime("%H:%M:%S")
    plat = platform.system()
    lines = [
        "",
        GD + "  ┌" + "─"*56 + "┐" + RS,
        GD + "  │" + G  + "  ██████╗ ██╗   ██╗ ██████╗        " + RS,
        GD + "  │" + G  + "  ██╔══██╗██║   ██║██╔════╝        " + RS,
        GD + "  │" + G  + "  ██████╔╝██║   ██║██║  ███╗       " + RS,
        GD + "  │" + G  + "  ██╔══██╗██║   ██║██║   ██║       " + RS,
        GD + "  │" + G  + "  ██████╔╝╚██████╔╝╚██████╔╝       " + RS,
        GD + "  │" + G  + "  ╚═════╝  ╚═════╝  ╚═════╝        " + RS,
        GD + "  │" + MG + "  ██████╗                          " + RS,
        GD + "  │" + MG + "  ██╔══██╗                         " + RS,
        GD + "  │" + MG + "  ███████║                         " + RS,
        GD + "  │" + MG + "  ██╔══██║                         " + RS,
        GD + "  │" + MG + "  ██║  ██║                         " + RS,
        GD + "  │" + MG + "  ╚═╝  ╚═╝                         " + RS,
        GD + "  ├" + "─"*56 + "┤" + RS,
        GD + "  │" + DM + "    Bug-Attacker — Security Recon Toolkit        " + GD + "│" + RS,
        GD + "  ├" + "─"*56 + "┤" + RS,
        GD + "  │" + WH + "  Author   : " + G  + "krypthane" + DM + " · wavegxz-design           " + GD + "│" + RS,
        GD + "  │" + WH + "  GitHub   : " + CY + "github.com/wavegxz-design              " + GD + "  │" + RS,
        GD + "  │" + WH + "  Telegram : " + CY + "t.me/Skrylakk                          " + GD + "  │" + RS,
        GD + "  │" + WH + "  Version  : " + YL + "v1.0" + DM + "  ·  " + WH + "Platform: " + CY + plat + " "*(max(0,15-len(plat))) + GD + "    │" + RS,
        GD + "  │" + WH + "  Time     : " + YL + now + DM + "                                  " + GD + "│" + RS,
        GD + "  └" + "─"*56 + "┘" + RS,
        "",
    ]
    for line in lines:
        print(line)
        time.sleep(0.018)

def menu():
    print(
        GD + "  ┌─────────────────────────────────────────────────────┐\n" + RS +
        GD + "  │" + G  + "  [??] SELECT MODULE                                 " + GD + "│\n" + RS +
        GD + "  ├───────────────────────┬───────────────────────────┤\n" + RS +
        GD + "  │" + WH + " [" + YL + "1" + WH + "] IP Lookup            " + GD + "│" + WH + " [" + YL + "4" + WH + "] Subdomain Scanner      " + GD + "│\n" + RS +
        GD + "  │" + WH + " [" + YL + "2" + WH + "] Port Scanner         " + GD + "│" + WH + " [" + YL + "5" + WH + "] Subdir Scanner         " + GD + "│\n" + RS +
        GD + "  │" + WH + " [" + YL + "3" + WH + "] Phone Lookup         " + GD + "│" + WH + " [" + YL + "0" + WH + "] Quit                   " + GD + "│\n" + RS +
        GD + "  └───────────────────────┴───────────────────────────┘" + RS
    )

def run_tool(path):
    """
    FIX: subprocess instead of os.system() — no shell injection risk.
    """
    tool = os.path.join(os.path.dirname(__file__), "tools", path)
    if not os.path.isfile(tool):
        print(R + f"\n  [!] Tool not found: {tool}" + RS)
        input(DM + "\n  Press Enter to return..." + RS)
        return
    try:
        subprocess.run([sys.executable, tool], check=False)
    except KeyboardInterrupt:
        print(GD + "\n  [*] Interrupted. Returning to menu..." + RS)
    except Exception as e:
        print(R + f"\n  [!] Error running tool: {e}" + RS)
    input(DM + "\n  Press Enter to return to menu..." + RS)

def about():
    clear()
    print(
        "\n" +
        GD + "  ┌" + "─"*54 + "┐\n" + RS +
        GD + "  │" + G  + "  Bug-Attacker — About                               " + GD + "│\n" + RS +
        GD + "  ├" + "─"*54 + "┤\n" + RS +
        GD + "  │" + WH + "  A modular recon toolkit for authorized security     " + GD + "│\n" + RS +
        GD + "  │" + WH + "  research, bug bounty, and CTF competitions.         " + GD + "│\n" + RS +
        GD + "  ├" + "─"*54 + "┤\n" + RS +
        GD + "  │" + DM + "  Maintained by krypthane                            " + GD + "│\n" + RS +
        GD + "  │" + DM + "  github.com/wavegxz-design                          " + GD + "│\n" + RS +
        GD + "  │" + DM + '  "Know the attack to build the defense."            ' + GD + "│\n" + RS +
        GD + "  └" + "─"*54 + "┘\n" + RS
    )
    input(DM + "  Press Enter to return..." + RS)

# ── MAIN LOOP ──────────────────────────────────────────────────────
TOOLS = {
    "1": ("ip-lookup.py",          "IP Lookup"),
    "2": ("port-scanner.py",       "Port Scanner"),
    "3": ("phone-lookup.py",       "Phone Lookup"),
    "4": ("subdomain-scanner.py",  "Subdomain Scanner"),
    "5": ("subdir-scanner.py",     "Subdirectory Scanner"),
}

def main():
    banner()
    while True:
        menu()
        try:
            cmd = input(MG + "\n  bug-attacker" + GD + ">> " + WH).strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(GD + "\n\n  [*] Exiting Bug-Attacker. Stay ethical.\n" + RS)
            sys.exit(0)

        if cmd in ("0", "exit", "quit", "q"):
            print(GD + "\n  [*] Exiting Bug-Attacker. Stay ethical.\n" + RS)
            sys.exit(0)
        elif cmd in TOOLS:
            path, name = TOOLS[cmd]
            clear()
            print(GD + f"\n  ── Running: {name} ──\n" + RS)
            run_tool(path)
            banner()
        elif cmd in ("about", "99"):
            about()
            banner()
        elif cmd == "":
            banner()
        else:
            print(R + "  [!] Invalid option. Choose 1-5 or 0 to quit.\n" + RS)
            time.sleep(0.8)

if __name__ == "__main__":
    main()
