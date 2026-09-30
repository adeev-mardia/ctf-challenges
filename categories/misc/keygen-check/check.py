#!/usr/bin/env python3
"""
License checker. Run: python3 check.py YOUR-SERIAL-HERE
A valid 20-character serial (uppercase letters and digits only)
unlocks the flag.
"""
import sys

TARGETS = [0, 57, 232, 224, 25, 218, 52, 88, 78, 12, 61, 216, 113, 10, 174, 66, 75, 105, 239, 183]

FLAG = None  # set by the license server; not present in this file

def check(serial: str) -> bool:
    if len(serial) != 20:
        return False
    for i, ch in enumerate(serial):
        v = ord(ch)
        mult = (2 * i + 17)
        offset = (i * 31 + 5) % 256
        target = (v * mult + offset) % 256
        if target != TARGETS[i]:
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 check.py SERIAL")
        sys.exit(1)
    serial = sys.argv[1]
    if check(serial):
        import hashlib, base64
        # The real deployment prints the flag on success; here we
        # reveal it via a fixed encoded constant so this file is fully
        # self-contained and needs no network/server.
        enc = 'ZmxhZ3tyM3YzcnMxbmdfYV9jaDNja3N1bV9ieV9oNG5kfQ=='
        print("Valid serial! Flag:", base64.b64decode(enc).decode())
    else:
        print("Invalid serial.")
