# encoding-layers — Writeup

## The chain

The flag was encoded through five stages, in order:

1. ROT13
2. hex encode
3. base64 encode
4. base32 encode
5. reverse the string

To recover the flag, undo each stage in **reverse order**.

## Steps

1. **Identify stage 5 (reverse):** the string uses only uppercase letters
   `A-Z` and digits `2-7` — that's the base32 alphabet, but base32 output
   is normally padded with `=` and here it isn't, and standard base32
   decoding fails until we reverse the string first (a natural thing to
   try once decoding fails outright).

2. **Undo base32:** `base64.b32decode(reversed_string)` → gives a
   base64-looking ASCII string.

3. **Undo base64:** `base64.b64decode(...)` → gives a string of hex
   digits.

4. **Undo hex:** `bytes.fromhex(...)` → gives ROT13'd ASCII text
   (recognizable as English-shaped but scrambled letters, e.g.
   `synt{...}` instead of `flag{...}`).

5. **Undo ROT13:** `codecs.decode(text, "rot13")` → the flag.

```python
def decode(encoded):
    stage4 = encoded[::-1]
    stage3 = base64.b32decode(stage4).decode()
    stage2 = base64.b64decode(stage3).decode()
    stage1 = bytes.fromhex(stage2).decode()
    return codecs.decode(stage1, "rot13")
```

## Running it

```
$ python3 solve.py
flag{lay3rs_0f_3nc0d1ng_ar3nt_crypt0}
```

## Takeaway

Layered encoding (as opposed to encryption) provides zero real
confidentiality — every stage is a well-known, reversible, keyless
transform. This challenge is about pattern recognition (alphabets,
padding, character distributions) and methodically peeling back
transformations, a skill that generalizes to real malware/obfuscation
analysis.
