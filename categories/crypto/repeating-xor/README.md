# repeating-xor

**Category:** Crypto
**Difficulty:** Easy

We intercepted a field transmission. It looks like it was "encrypted" with
some kind of repeating XOR key before being hex-encoded. Recover the
plaintext and find the flag.

## Files

- `ciphertext.hex` — the intercepted, hex-encoded ciphertext

## Hint

Repeating-key XOR is breakable without knowing the key in advance: figure
out the key length first (Hamming distance between blocks), then break
each column as single-byte XOR using English letter frequency.
