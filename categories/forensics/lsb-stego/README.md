# lsb-stego

**Category:** Forensics
**Difficulty:** Easy

We found this innocuous-looking PNG on a compromised machine. Nothing
looks unusual to the eye, but our analysts suspect something's hidden
inside it.

## Files

- `cover.png` — the image in question

## Hint

Least-significant-bit steganography hides data in the low bits of pixel
color channels, which barely change how the image looks. Try reading the
LSB of every R/G/B value in order.
