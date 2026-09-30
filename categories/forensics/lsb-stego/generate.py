#!/usr/bin/env python3
"""Generator for lsb-stego: embeds the flag into the least-significant bit
of each RGB channel of a procedurally generated cover image (no external
image asset needed), using a 32-bit length prefix then the flag bytes."""
from PIL import Image
import random

FLAG = b"flag{lsb_st3g0_hidd3n_1n_pl41n_s1ght}"
WIDTH, HEIGHT = 64, 48


def make_cover_image(seed=42):
    rng = random.Random(seed)
    img = Image.new("RGB", (WIDTH, HEIGHT))
    px = img.load()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            # simple gradient + noise cover pattern
            r = (x * 255 // WIDTH + rng.randint(-5, 5)) % 256
            g = (y * 255 // HEIGHT + rng.randint(-5, 5)) % 256
            b = ((x + y) * 255 // (WIDTH + HEIGHT) + rng.randint(-5, 5)) % 256
            px[x, y] = (r, g, b)
    return img


def embed_lsb(img: Image.Image, data: bytes) -> Image.Image:
    length_prefix = len(data).to_bytes(4, "big")
    payload = length_prefix + data
    bits = []
    for byte in payload:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    img = img.copy()
    px = img.load()
    w, h = img.size
    bit_idx = 0
    total_bits = len(bits)
    for y in range(h):
        for x in range(w):
            if bit_idx >= total_bits:
                return img
            r, g, b = px[x, y]
            channels = [r, g, b]
            for c in range(3):
                if bit_idx >= total_bits:
                    break
                channels[c] = (channels[c] & ~1) | bits[bit_idx]
                bit_idx += 1
            px[x, y] = tuple(channels)
    return img


def main():
    cover = make_cover_image()
    stego = embed_lsb(cover, FLAG)
    stego.save("cover.png")
    print("Saved cover.png with", len(FLAG), "byte flag embedded via LSB")


if __name__ == "__main__":
    main()
