# cube-root-rsa — Writeup

## The bug

RSA encryption is `c = m^e mod n`. Security depends on it being infeasible
to invert this without the private key — but that assumption breaks down
when:

1. `e` is small (here `e = 3`), **and**
2. no padding scheme (like OAEP) is applied to `m`, **and**
3. the plaintext `m` is small enough that `m^e < n`.

In that situation, `m^e mod n` never actually wraps around the modulus —
it *is* `m^e` as a plain integer. So the "modular" exponentiation is really
just ordinary exponentiation, and we can invert it with an ordinary integer
cube root, no factoring of `n` required.

Here `n` is a 2048-bit modulus, and the flag is only 42 bytes (336 bits),
so `m` is far smaller than `n^(1/3)` (~683 bits) and condition 3 holds.

## Steps

1. Parse `n`, `e`, `c` out of `public.txt`.
2. Compute the integer cube root of `c` (binary search, since Python has no
   built-in exact integer nth-root for huge numbers pre-3.11's `math.isqrt`
   is square-root only):

```python
def integer_nth_root(x, n):
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
```

3. Verify `m ** e == c` exactly (confirms no modular wraparound happened —
   if it doesn't hold, the attack doesn't directly apply and you'd need
   Coppersmith's method or the Hastad broadcast attack instead).
4. Convert `m` to bytes and decode as ASCII.

## Running it

```
$ python3 solve.py
flag{cube_r00t_att4ck_n0_padd1ng_1s_bad}
```

## Takeaway

Never use RSA with a small public exponent on unpadded/short messages.
Always use a proper padding scheme (OAEP) — it randomizes the plaintext so
`m^e` is always close to the full size of `n`, defeating this attack.
