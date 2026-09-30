# keygen-check — Writeup

## The check

`check.py` validates a 20-character serial one character at a time:

```python
mult = (2 * i + 17)
offset = (i * 31 + 5) % 256
target = (v * mult + offset) % 256
if target != TARGETS[i]:
    return False
```

where `v = ord(serial[i])`. This is an **affine map mod 256**:
`target = v * mult + offset (mod 256)`. `mult` is always odd (`2*i+17` is
odd for any integer `i`), and every odd number is invertible modulo 256
(since gcd(odd, 256) = 1), so this map is a bijection — every `target`
value corresponds to exactly one `v`. That means we can solve for the
original character directly, without any guessing or brute force:

```
v = (target - offset) * inverse(mult, 256) mod 256
```

## Steps

1. Load `TARGETS` from `check.py` (importing the module directly, since
   it's plain, safe Python with no side effects at import time other than
   defining functions/constants — no `check(...)` call happens on
   import).
2. For each position `i` (0..19), recompute `mult` and `offset`, find the
   modular inverse of `mult` mod 256 via the extended Euclidean
   algorithm, and solve for `ord(serial[i])`.
3. Concatenate the recovered characters into the serial.
4. Run `check.py` with the recovered serial — it validates and prints the
   flag.

```python
def modinv(a, m):
    g, x, _ = extended_gcd(a % m, m)
    return x % m  # valid since gcd(a, m) == 1 here

def recover_serial(targets):
    chars = []
    for i, target in enumerate(targets):
        mult = (2 * i + 17) % 256
        offset = (i * 31 + 5) % 256
        v = ((target - offset) * modinv(mult, 256)) % 256
        chars.append(chr(v))
    return "".join(chars)
```

## Running it

```
$ python3 solve.py
[+] recovered serial: K7Q2XN9F1PZR8V3T6WLC
flag{r3v3rs1ng_a_ch3cksum_by_h4nd}
```

## Takeaway

Simple linear/affine per-character checksums look obscure but are
cryptographically meaningless — modular inverses make them fully and
efficiently invertible. Real license/serial validation should use actual
public-key signature verification (e.g. sign the license data with a
private key the vendor holds, verify with the embedded public key) rather
than a reversible transform.
