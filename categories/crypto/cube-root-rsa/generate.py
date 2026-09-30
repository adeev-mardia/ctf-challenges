#!/usr/bin/env python3
"""Generator for the cube-root-rsa challenge.
Produces a genuine RSA keypair with e=3 and NO padding applied to the message,
encrypts the flag, and writes public.txt (n, e, c) for players.
Because e is tiny and no padding is used, if m^3 < n (true here, since the
2048-bit modulus gives plenty of headroom over the short flag), the ciphertext
is simply c = m**3 with no modular wraparound, so m = integer_cube_root(c).
"""
from Crypto.Util.number import getPrime, bytes_to_long

FLAG = b"flag{cube_r00t_att4ck_n0_padd1ng_1s_bad}"

def main():
    e = 3
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    m = bytes_to_long(FLAG)
    assert m.bit_length() * e < n.bit_length(), "flag too long for clean cube-root attack"
    c = pow(m, e, n)
    # sanity: confirm no wraparound occurred
    assert m ** e == c, "modular wraparound occurred, regenerate with bigger modulus"

    with open("public.txt", "w") as f:
        f.write(f"n = {n}\ne = {e}\nc = {c}\n")
    print("Wrote public.txt")
    print("n bits:", n.bit_length(), "m bits:", m.bit_length())

if __name__ == "__main__":
    main()
