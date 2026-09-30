#!/usr/bin/env python3
"""
Solver for repeating-xor.

Classic break of repeating-key XOR ("Vigenere XOR"):
1. Guess the key size by finding the size that minimizes normalized
   Hamming distance between consecutive blocks of ciphertext.
2. Split ciphertext into `keysize` interleaved column-transposed blocks
   (byte i, i+keysize, i+2*keysize, ... goes in block i).
3. Each block is now single-byte XOR — brute-force all 256 key bytes and
   score by English letter-frequency / printability to find the best one.
4. Reassemble the key, decrypt, extract the flag.
"""
import binascii
import os
import re
import string

HERE = os.path.dirname(os.path.abspath(__file__))

ENGLISH_FREQ = {
    'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75,
    's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
    'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97,
    'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15,
    'q': 0.10, 'z': 0.07, ' ': 13.00,
}


def hamming_distance(a: bytes, b: bytes) -> int:
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def guess_keysize(ct: bytes, lo=2, hi=40):
    scores = []
    for size in range(lo, hi + 1):
        chunks = [ct[i * size:(i + 1) * size] for i in range(4)]
        if any(len(c) < size for c in chunks):
            continue
        dists = []
        for i in range(len(chunks) - 1):
            dists.append(hamming_distance(chunks[i], chunks[i + 1]) / size)
        avg = sum(dists) / len(dists)
        scores.append((avg, size))
    scores.sort()
    return [size for _, size in scores[:5]]


def score_text(data: bytes) -> float:
    score = 0.0
    for b in data:
        c = chr(b).lower()
        if c in ENGLISH_FREQ:
            score += ENGLISH_FREQ[c]
        elif chr(b) in string.printable:
            score += 0.05
        else:
            score -= 5.0
    return score


def break_single_byte_xor(block: bytes):
    best_score = float("-inf")
    best_key = 0
    for key in range(256):
        plain = bytes(b ^ key for b in block)
        s = score_text(plain)
        if s > best_score:
            best_score = s
            best_key = key
    return best_key, best_score


def transpose(ct: bytes, keysize: int):
    blocks = [bytearray() for _ in range(keysize)]
    for i, b in enumerate(ct):
        blocks[i % keysize].append(b)
    return blocks


def xor_decrypt(ct: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(ct))


def solve():
    hexdata = open(os.path.join(HERE, "ciphertext.hex")).read().strip()
    ct = binascii.unhexlify(hexdata)

    candidate_sizes = guess_keysize(ct)
    best_overall = None
    for keysize in candidate_sizes:
        blocks = transpose(ct, keysize)
        key = bytes(break_single_byte_xor(bytes(block))[0] for block in blocks)
        plaintext = xor_decrypt(ct, key)
        printable_ratio = sum(chr(b) in string.printable for b in plaintext) / len(plaintext)
        if best_overall is None or printable_ratio > best_overall[0]:
            best_overall = (printable_ratio, key, plaintext)

    _, key, plaintext = best_overall
    text = plaintext.decode(errors="replace")
    m = re.search(r"flag\{[^}]+\}", text)
    if not m:
        raise RuntimeError(f"No flag found. Recovered key={key}, text=\n{text}")
    return m.group(0)


if __name__ == "__main__":
    print(solve())
