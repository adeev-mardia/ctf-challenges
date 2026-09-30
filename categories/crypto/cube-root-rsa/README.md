# cube-root-rsa

**Category:** Crypto
**Difficulty:** Easy

Our intern rolled his own RSA encryption for a "quick and secure" message.
He used a public exponent of `e = 3` because "smaller is faster" and didn't
bother with any padding scheme. Surely that's fine for a 2048-bit modulus?

Recover the flag from the ciphertext.

## Files

- `public.txt` — the RSA public parameters (`n`, `e`) and the ciphertext (`c`)

## Hint

No padding + a tiny public exponent is a classic, real-world mistake. Think
about what happens to `m^e` when `m` is much smaller than the cube root of
`n`.
