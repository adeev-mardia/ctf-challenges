#!/usr/bin/env python3
"""
Solver for encoding-layers.

Undo the encoding chain in reverse order:
  reverse -> base32-decode -> base64-decode -> unhex -> rot13
"""
import base64
import codecs
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def decode(encoded: str) -> str:
    stage4 = encoded[::-1]                                  # undo reverse
    stage3 = base64.b32decode(stage4).decode()               # undo base32
    stage2 = base64.b64decode(stage3).decode()                # undo base64
    stage1 = bytes.fromhex(stage2).decode()                   # undo hex
    plaintext = codecs.decode(stage1, "rot13")                # undo rot13
    return plaintext


def solve():
    encoded = open(os.path.join(HERE, "message.txt")).read().strip()
    return decode(encoded)


if __name__ == "__main__":
    print(solve())
