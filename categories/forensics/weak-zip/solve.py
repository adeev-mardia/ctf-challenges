#!/usr/bin/env python3
"""
Solver for weak-zip.

Attack: the zip is protected with classic ZipCrypto encryption and a weak
password taken from a common-password list. We run a genuine dictionary
attack using Python's zipfile module, trying each candidate password from
wordlist.txt until one successfully extracts the archive.
"""
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))


def crack_zip(zip_path, wordlist_path):
    with open(wordlist_path) as f:
        candidates = [line.strip() for line in f if line.strip()]

    with zipfile.ZipFile(zip_path) as zf:
        member = zf.namelist()[0]
        for pwd in candidates:
            try:
                data = zf.read(member, pwd=pwd.encode())
                return pwd, data
            except (RuntimeError, zipfile.BadZipFile):
                continue
    raise RuntimeError("No password in wordlist cracked the zip")


def solve():
    zip_path = os.path.join(HERE, "secret.zip")
    wordlist_path = os.path.join(HERE, "wordlist.txt")
    password, data = crack_zip(zip_path, wordlist_path)
    return data.decode().strip(), password


if __name__ == "__main__":
    flag, password = solve()
    print(f"[+] cracked password: {password}")
    print(flag)
