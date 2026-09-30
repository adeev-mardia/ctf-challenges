# repeating-xor — Writeup

## The bug

Repeating-key XOR (the "Vigenere cipher" applied byte-wise) is not real
encryption: if the key is shorter than the plaintext (and it always is, or
it'd just be a one-time pad), the same key byte repeats periodically, and
each "column" of the ciphertext (bytes at position `i, i+keysize,
i+2*keysize, ...`) is really just single-byte XOR of that portion of the
plaintext — which is trivially breakable with frequency analysis.

## Steps

### 1. Recover the key length

For candidate key sizes `k`, take a few consecutive `k`-byte chunks of
ciphertext and compute the average (normalized) Hamming distance between
them. XOR of two chunks encrypted under the *same* key stream is
`(p1 XOR k) XOR (p2 XOR k) = p1 XOR p2`, i.e. it depends only on the
plaintext, and English plaintext has much lower bit-level entropy than
random data — so the correct key size gives noticeably lower Hamming
distance than a wrong one.

```python
def hamming_distance(a, b):
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))
```

We try key sizes from 2 to 40 and keep the ones with lowest normalized
distance.

### 2. Transpose into columns

Given the guessed key size `k`, split the ciphertext into `k` interleaved
blocks (block `i` = bytes at positions `i, i+k, i+2k, ...`). Every byte in
block `i` was XORed with the same single key byte `key[i]`.

### 3. Break each column as single-byte XOR

For each of the 256 possible key bytes, XOR-decrypt the column and score
the result against English letter frequencies (plus a penalty for
non-printable bytes). The key byte with the highest score wins.

### 4. Reassemble and decrypt

Concatenate the recovered key bytes, XOR-decrypt the whole ciphertext with
the repeating key, and read off the flag with a regex for `flag\{...\}`.

## Running it

```
$ python3 solve.py
flag{r3p3at1ng_k3y_x0r_1s_n0t_3ncrypt10n}
```

## Takeaway

XOR with a short, reused key provides no real confidentiality once an
attacker has enough ciphertext — always use an authenticated stream/block
cipher (AES-GCM, ChaCha20-Poly1305) with a unique key/nonce per message.
