#!/usr/bin/env python3
"""
Solver for lsb-stego.

Attack: extract the least significant bit of every R, G, B channel value
in raster order, first reading a 32-bit big-endian length prefix, then
that many bytes of payload.
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))


def extract_lsb_bits(img: Image.Image):
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = px[x, y][:3]
            for c in (r, g, b):
                yield c & 1


def bits_to_bytes(bit_iter, n_bytes):
    out = bytearray()
    for _ in range(n_bytes):
        byte = 0
        for _ in range(8):
            byte = (byte << 1) | next(bit_iter)
        out.append(byte)
    return bytes(out)


def solve():
    img = Image.open(os.path.join(HERE, "cover.png"))
    bit_iter = extract_lsb_bits(img)
    length_bytes = bits_to_bytes(bit_iter, 4)
    length = int.from_bytes(length_bytes, "big")
    flag_bytes = bits_to_bytes(bit_iter, length)
    return flag_bytes.decode()


if __name__ == "__main__":
    print(solve())
