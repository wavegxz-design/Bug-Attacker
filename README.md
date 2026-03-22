<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=00ff41&height=200&section=header&text=Bug-Attacker&fontSize=60&fontColor=000000&animation=fadeIn&fontAlignY=38&desc=Security+Recon+Toolkit&descAlignY=60&descSize=18&descColor=000000" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=20&pause=1000&color=00FF41&center=true&vCenter=true&width=600&lines=Port+Scanner+%7C+IP+Lookup+%7C+Phone+Lookup;Subdomain+%26+Subdirectory+Scanner;Threaded+%C2%B7+Fast+%C2%B7+Safe;Authorized+Use+Only+%E2%80%94+Stay+Legal" alt="Typing SVG" />
</a>

<br/><br/>

![Python](https://img.shields.io/badge/Python-3.8%2B-00ff41?style=for-the-badge&logo=python&logoColor=00ff41&labelColor=0d1117)
![Platform](https://img.shields.io/badge/Linux%20%7C%20Windows%20%7C%20macOS-supported-00ff41?style=for-the-badge&logo=linux&logoColor=00ff41&labelColor=0d1117)
![Version](https://img.shields.io/badge/Version-1.0-00cfff?style=for-the-badge&labelColor=0d1117)
![Threaded](https://img.shields.io/badge/Threaded-50_concurrent-00ff41?style=for-the-badge&labelColor=0d1117)
![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge&labelColor=0d1117)
![Ethics](https://img.shields.io/badge/Authorized_Use_Only-⚠️-ff2d2d?style=for-the-badge&labelColor=0d1117)

</div>

---

## 🌐 What is Bug-Attacker?

**Bug-Attacker** is a modular, terminal-based security recon toolkit for bug bounty hunters, CTF players, and authorized penetration testers. It provides fast, threaded scanning and intelligence gathering from a clean, unified interface.

Actively maintained and hardened by **[krypthane](https://github.com/wavegxz-design)** — Red Team Operator from Mexico 🇲🇽.

---

## 🧩 Modules

```
╔═══════════════════════════════════════════════════╗
║            Bug-Attacker  v1.0                    ║
╠═══════════════════╦═══════════════════════════════╣
║  [1] IP Lookup    ║  [4] Subdomain Scanner        ║
║  [2] Port Scanner ║  [5] Subdirectory Scanner     ║
║  [3] Phone Lookup ║  [0] Quit                     ║
╚═══════════════════╩═══════════════════════════════╝
```

---

## 🔒 Security Improvements — v1.0

> Audit and fixes applied by **krypthane**

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | API key hardcoded in `ip-lookup.py` | 🔴 HIGH | Moved to `APILAYER_KEY` env var |
| 2 | `os.system()` for subprocess calls | 🟡 MED | Replaced with `subprocess.run()` |
| 3 | No threading in scanners | 🟡 MED | 50 concurrent threads added |
| 4 | No timeout on requests | 🟡 MED | 4–8s timeout on all requests |
| 5 | No input validation | 🟡 MED | Full validation on all inputs |
| 6 | No error handling on network calls | 🟡 MED | try/except on every network op |
| 7 | Status codes hidden in subdomain scan | 🟢 LOW | Shows 200/301/403 with colors |

---

## 🚀 Installation

```bash
git clone https://github.com/wavegxz-design/Bug-Attacker
cd Bug-Attacker
pip install -r requirements.txt
python bug-attacker.py
```

---

## ⚙️ Configuration

Set API keys as environment variables — **never hardcode them**:

```bash
# Optional — required only for Phone Lookup module
export APILAYER_KEY="your_key_here"
# Get a free key at: https://apilayer.com/marketplace/number_verification-api
```

Add to `~/.bashrc` or `~/.zshrc` to persist.

---

## 🖥️ Usage

```bash
python bug-attacker.py
```

```
  ┌────────────────────────────────────────────────────────┐
  │  Bug-Attacker — Security Recon Toolkit                │
  ├────────────────────────────────────────────────────────┤
  │  [1] IP Lookup        │  [4] Subdomain Scanner        │
  │  [2] Port Scanner     │  [5] Subdirectory Scanner     │
  │  [3] Phone Lookup     │  [0] Quit                     │
  └────────────────────────────────────────────────────────┘

  bug-attacker>>
```

---

## 📁 Project Structure

```
Bug-Attacker/
├── bug-attacker.py          ← Main launcher
├── requirements.txt
├── .gitignore
├── wordlists/
│   ├── subdomains.txt       ← Subdomain wordlist
│   └── directories.txt      ← Directory wordlist
└── tools/
    ├── ip-lookup.py         ← IP + Phone lookup
    ├── port-scanner.py      ← Threaded port scanner
    ├── subdomain-scanner.py ← Threaded subdomain scanner
    └── subdir-scanner.py    ← Threaded directory scanner
```

---

## 🤝 Contributing

```bash
git checkout -b feat/module-name
git commit -m "feat: add [module] — description"
git push origin feat/module-name
```

**Security checklist before PR:**
- [ ] No hardcoded API keys or tokens
- [ ] No `shell=True` with user input
- [ ] Input validated before use
- [ ] Tested on Linux and Windows

---

## ⚠️ Legal Disclaimer

```
For AUTHORIZED security research and educational purposes ONLY.

✅  Bug bounty programs (within scope)
✅  CTF competitions
✅  Authorized penetration testing
✅  Personal lab environments

❌  Unauthorized scanning of systems you don't own
❌  Any illegal activity under local or international law

The author assumes NO responsibility for misuse.
```

---

## 👤 Author & Maintainer

<div align="center">

| | |
|:---:|:---|
| <img src="https://github.com/wavegxz-design.png" width="80" style="border-radius:50%"/> | **krypthane** — Red Team Operator & Open Source Developer<br/>📍 Mexico 🇲🇽 UTC-6<br/>*"Know the attack to build the defense."* |

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-wavegxz--design-00ff41?style=for-the-badge&logo=github&labelColor=0d1117)](https://github.com/wavegxz-design)
[![Telegram](https://img.shields.io/badge/Telegram-Skrylakk-00cfff?style=for-the-badge&logo=telegram&labelColor=0d1117)](https://t.me/Skrylakk)
[![Email](https://img.shields.io/badge/Email-Workernova@proton.me-ff2d2d?style=for-the-badge&logo=protonmail&labelColor=0d1117)](mailto:Workernova@proton.me)
[![Portfolio](https://img.shields.io/badge/Portfolio-krypthane-00ff41?style=for-the-badge&logo=cloudflare&labelColor=0d1117)](https://krypthane.workernova.workers.dev)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=00ff41&height=120&section=footer&fontColor=000000&animation=fadeIn&text=krypthane+%C2%B7+wavegxz-design+%C2%B7+Ethical+Hacking+Only" width="100%"/>

</div>
