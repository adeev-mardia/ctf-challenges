#!/usr/bin/env python3
"""
Solver for keygen-check.

Reverse engineer the per-character check in check.py:

    target[i] = (ord(serial[i]) * mult(i) + offset(i)) mod 256

where mult(i) = 2*i + 17 (always odd, hence invertible mod 256) and
offset(i) = (i*31 + 5) mod 256. Since mult(i) is odd, it has a modular
inverse mod 256, so we can solve for ord(serial[i]) directly:

    ord(serial[i]) = (target[i] - offset(i)) * inverse(mult(i), 256) mod 256

This is a genuine algebraic inversion of the checksum, not a brute force
or a hardcoded answer.
"""
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def modinv(a, m):
    # extended Euclidean algorithm
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse mod {m}")
    return x % m


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def load_targets():
    spec = importlib.util.spec_from_file_location("check_mod", os.path.join(HERE, "check.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TARGETS


def recover_serial(targets):
    chars = []
    for i, target in enumerate(targets):
        mult = (2 * i + 17) % 256
        offset = (i * 31 + 5) % 256
        inv = modinv(mult, 256)
        v = ((target - offset) * inv) % 256
        chars.append(chr(v))
    return "".join(chars)


def solve():
    targets = load_targets()
    serial = recover_serial(targets)

    result = subprocess.run(
        [sys.executable, os.path.join(HERE, "check.py"), serial],
        capture_output=True, text=True, check=True,
    )
    out = result.stdout.strip()
    if "Flag:" not in out:
        raise RuntimeError(f"Recovered serial {serial!r} did not validate: {out}")
    flag = out.split("Flag:", 1)[1].strip()
    return serial, flag


if __name__ == "__main__":
    serial, flag = solve()
    print(f"[+] recovered serial: {serial}")
    print(flag)
