# lsb-stego — Writeup

## The technique

LSB (least significant bit) steganography hides data by overwriting the
lowest bit of each color channel byte in an image. Since flipping the
lowest bit changes a channel value by at most 1 (e.g. 200 -> 201), it's
visually imperceptible, but a program can read those bits back out in
order.

This challenge embeds the payload as:

- 4 bytes: big-endian length of the flag (in bytes)
- N bytes: the flag itself

...bit by bit (MSB first per byte), one bit per R/G/B channel value, in
raster (row-major) pixel order.

## Steps

1. Open `cover.png` with Pillow and iterate pixels in row-major order.
2. For each pixel, take the R, G, B channel values (ignore alpha if
   present) and extract the lowest bit (`value & 1`) of each, in order.
3. Read the first 32 bits as a big-endian integer: that's the flag length
   in bytes.
4. Read the next `length * 8` bits, pack them 8-at-a-time (MSB first) into
   bytes, and decode as ASCII.

```python
def extract_lsb_bits(img):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = px[x, y][:3]
            for c in (r, g, b):
                yield c & 1
```

## Running it

```
$ python3 solve.py
flag{lsb_st3g0_hidd3n_1n_pl41n_s1ght}
```

## Takeaway

LSB steganography is easy to both create and detect once you know to look
for it — statistical tests (like chi-square analysis on bit-plane
distributions) or simply extracting and trying to parse the LSB plane
will reveal hidden payloads like this. It provides no cryptographic
confidentiality, only obscurity.
