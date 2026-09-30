#!/usr/bin/env python3
"""
Solver for cube-root-rsa.

Attack: e=3 with no padding means c = m**3 (no modular reduction, since the
message is much shorter than the modulus). So we just take the integer cube
root of c to recover m.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def parse_public(path):
    text = open(path).read()
    n = int(re.search(r"n\s*=\s*(\d+)", text).group(1))
    e = int(re.search(r"e\s*=\s*(\d+)", text).group(1))
    c = int(re.search(r"c\s*=\s*(\d+)", text).group(1))
    return n, e, c


def integer_nth_root(x, n):
    """Exact/floor integer n-th root via binary search."""
    if x < 0:
        raise ValueError("x must be non-negative")
    lo, hi = 0, 1
    while hi ** n <= x:
        hi <<= 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** n <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def solve():
    n, e, c = parse_public(os.path.join(HERE, "public.txt"))
    m = integer_nth_root(c, e)
    assert m ** e == c, "c is not a perfect e-th power; attack assumptions violated"
    flag = m.to_bytes((m.bit_length() + 7) // 8, "big")
    return flag.decode()


if __name__ == "__main__":
    flag = solve()
    print(flag)
