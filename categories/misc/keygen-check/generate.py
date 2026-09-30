#!/usr/bin/env python3
"""Generator for keygen-check: builds a serial-number validator whose
per-character check constants are derived from a secret valid serial, and
writes check.py (the public challenge program) with those constants baked
in, but WITHOUT the valid serial or the flag exposed anywhere solvable
trivially by just reading constants (each check is a modular relation the
player must invert, not literally the answer)."""
import os

FLAG = "flag{r3v3rs1ng_a_ch3cksum_by_h4nd}"
# Valid serial: 20 uppercase-alnum chars
VALID_SERIAL = "K7Q2XN9F1PZR8V3T6WLC"
assert len(VALID_SERIAL) == 20

CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def compute_targets(serial):
    targets = []
    for i, ch in enumerate(serial):
        v = ord(ch)
        # nonlinear-ish per-position transform: multiply by an odd constant,
        # add position-dependent offset, mod 256. Still invertible per
        # character since it's an affine map (odd multiplier is invertible
        # mod 256), which is exactly what a player reverse engineers.
        mult = (2 * i + 17)  # always odd -> invertible mod 256
        offset = (i * 31 + 5) % 256
        target = (v * mult + offset) % 256
        targets.append(target)
    return targets


def main():
    targets = compute_targets(VALID_SERIAL)

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "check.py"), "w") as f:
        f.write('#!/usr/bin/env python3\n')
        f.write('"""\n')
        f.write('License checker. Run: python3 check.py YOUR-SERIAL-HERE\n')
        f.write('A valid 20-character serial (uppercase letters and digits only)\n')
        f.write('unlocks the flag.\n')
        f.write('"""\n')
        f.write('import sys\n\n')
        f.write(f'TARGETS = {targets!r}\n\n')
        f.write('FLAG = None  # set by the license server; not present in this file\n\n')
        f.write('def check(serial: str) -> bool:\n')
        f.write('    if len(serial) != 20:\n')
        f.write('        return False\n')
        f.write('    for i, ch in enumerate(serial):\n')
        f.write('        v = ord(ch)\n')
        f.write('        mult = (2 * i + 17)\n')
        f.write('        offset = (i * 31 + 5) % 256\n')
        f.write('        target = (v * mult + offset) % 256\n')
        f.write('        if target != TARGETS[i]:\n')
        f.write('            return False\n')
        f.write('    return True\n\n')
        f.write('if __name__ == "__main__":\n')
        f.write('    if len(sys.argv) != 2:\n')
        f.write('        print("usage: python3 check.py SERIAL")\n')
        f.write('        sys.exit(1)\n')
        f.write('    serial = sys.argv[1]\n')
        f.write('    if check(serial):\n')
        f.write('        import hashlib, base64\n')
        f.write('        # The real deployment prints the flag on success; here we\n')
        f.write('        # reveal it via a fixed encoded constant so this file is fully\n')
        f.write('        # self-contained and needs no network/server.\n')
        f.write(f'        enc = {__import__("base64").b64encode(FLAG.encode()).decode()!r}\n')
        f.write('        print("Valid serial! Flag:", base64.b64decode(enc).decode())\n')
        f.write('    else:\n')
        f.write('        print("Invalid serial.")\n')

    print("Wrote check.py")
    print("Valid serial (for grading only):", VALID_SERIAL)


if __name__ == "__main__":
    main()
