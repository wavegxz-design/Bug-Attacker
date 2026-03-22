#!/usr/bin/env python3
"""
Bug-Attacker — IP Lookup Module
FIX: API key from environment variable (was hardcoded)
FIX: Full error handling — network errors, invalid input, API errors
FIX: Timeout on requests
"""

import os
import sys
import requests

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
{GD}  │{G}  Bug-Attacker — IP / Phone Lookup       {GD}│
{GD}  │{DM}  Powered by ipinfo.io + apilayer.com   {GD}│
{GD}  └──────────────────────────────────────────┘{RS}
"""

def lookup_ip(ip: str) -> None:
    """Look up IP using ipinfo.io — no key required for basic use."""
    ip = ip.strip()
    if not ip:
        print(R + "  [!] Empty input." + RS)
        return

    print(GD + f"\n  [*] Looking up: {ip}\n" + RS)
    try:
        r = requests.get(
            f"https://ipinfo.io/{ip}/json",
            timeout=8,
            headers={"Accept": "application/json"}
        )
        r.raise_for_status()
        data = r.json()

        if "bogon" in data:
            print(R + "  [!] Bogon/private IP — no public info available." + RS)
            return

        fields = [
            ("IP",       data.get("ip",       "N/A")),
            ("Hostname", data.get("hostname",  "N/A")),
            ("City",     data.get("city",      "N/A")),
            ("Region",   data.get("region",    "N/A")),
            ("Country",  data.get("country",   "N/A")),
            ("Location", data.get("loc",       "N/A")),
            ("Org/ISP",  data.get("org",       "N/A")),
            ("Timezone", data.get("timezone",  "N/A")),
        ]
        print(GD + "  ┌" + "─"*42 + "┐" + RS)
        for label, value in fields:
            pad = 10 - len(label)
            print(GD + "  │" + WH + f"  {label}" + " "*pad + ": " + CY + str(value) + " "*(28-len(str(value))) + GD + "│" + RS)
        print(GD + "  └" + "─"*42 + "┘" + RS)

    except requests.exceptions.Timeout:
        print(R + "  [!] Request timed out. Check your connection." + RS)
    except requests.exceptions.ConnectionError:
        print(R + "  [!] Network error. Are you connected?" + RS)
    except requests.exceptions.HTTPError as e:
        print(R + f"  [!] HTTP error: {e}" + RS)
    except ValueError:
        print(R + "  [!] Invalid response from API." + RS)
    except Exception as e:
        print(R + f"  [!] Unexpected error: {e}" + RS)


def lookup_phone(number: str) -> None:
    """
    Phone lookup via apilayer.
    FIX: API key from APILAYER_KEY env var — never hardcoded.
    """
    api_key = os.environ.get("APILAYER_KEY", "").strip()
    if not api_key:
        print(
            YL + "\n  [!] APILAYER_KEY not set.\n" + RS +
            DM + "  Set it with:\n" +
            "  export APILAYER_KEY=\"your_key_here\"\n" +
            "  Get a free key at: https://apilayer.com/marketplace/number_verification-api\n" + RS
        )
        return

    number = number.strip()
    if not number.startswith("+"):
        print(YL + "  [!] Include country code, e.g. +521234567890" + RS)
        return

    print(GD + f"\n  [*] Looking up: {number}\n" + RS)
    try:
        r = requests.get(
            f"https://api.apilayer.com/number_verification/validate?number={number}",
            headers={"apikey": api_key},
            timeout=8
        )
        r.raise_for_status()
        d = r.json()

        if not d.get("valid"):
            print(R + "  [!] Number is invalid or not found." + RS)
            return

        fields = [
            ("Number",      d.get("number",       "N/A")),
            ("Country",     d.get("country_name", "N/A")),
            ("Code",        d.get("country_code", "N/A")),
            ("Carrier",     d.get("carrier",      "N/A")),
            ("Line Type",   d.get("line_type",    "N/A")),
            ("Location",    d.get("location",     "N/A")),
        ]
        print(GD + "  ┌" + "─"*42 + "┐" + RS)
        for label, value in fields:
            pad = 10 - len(label)
            print(GD + "  │" + WH + f"  {label}" + " "*pad + ": " + CY + str(value) + " "*(28-len(str(value))) + GD + "│" + RS)
        print(GD + "  └" + "─"*42 + "┘" + RS)

    except requests.exceptions.Timeout:
        print(R + "  [!] Request timed out." + RS)
    except requests.exceptions.ConnectionError:
        print(R + "  [!] Network error." + RS)
    except requests.exceptions.HTTPError as e:
        print(R + f"  [!] HTTP {r.status_code}: {e}" + RS)
    except Exception as e:
        print(R + f"  [!] Unexpected error: {e}" + RS)


def main():
    print(BANNER)
    print(GD + "  [1]" + WH + " IP Address Lookup")
    print(GD + "  [2]" + WH + " Phone Number Lookup")
    print(GD + "  [0]" + WH + " Back\n" + RS)

    try:
        choice = input(GD + "  >> " + WH).strip()
    except (KeyboardInterrupt, EOFError):
        return

    if choice == "1":
        try:
            ip = input(GD + "\n  Enter IP address: " + WH).strip()
        except (KeyboardInterrupt, EOFError):
            return
        lookup_ip(ip)

    elif choice == "2":
        try:
            number = input(GD + "\n  Enter phone number (with +country code): " + WH).strip()
        except (KeyboardInterrupt, EOFError):
            return
        lookup_phone(number)

    elif choice == "0":
        return
    else:
        print(R + "  [!] Invalid option." + RS)


if __name__ == "__main__":
    main()
