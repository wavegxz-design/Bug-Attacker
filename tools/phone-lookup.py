#!/usr/bin/env python3
"""
Bug-Attacker — Phone Lookup Module
Redirects to ip-lookup.py phone section.
"""
import subprocess, sys, os
tool = os.path.join(os.path.dirname(__file__), "ip-lookup.py")
subprocess.run([sys.executable, tool])
