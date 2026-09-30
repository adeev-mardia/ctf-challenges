# weak-zip — Writeup

## The bug

`secret.zip` was created with classic ZipCrypto encryption (the same
scheme `zip -e` uses), protected with a password pulled straight from a
list of extremely common/weak passwords. There's no need to break the
cryptography itself (ZipCrypto is weak too, but that's a different
attack) — a plain dictionary attack against the small candidate list in
`wordlist.txt` is enough.

## Steps

1. Load every candidate password from `wordlist.txt`.
2. For each one, try to read the file inside `secret.zip` using Python's
   built-in `zipfile` module with that password. A wrong password raises
   `RuntimeError: Bad password for file ...` (or, occasionally,
   `zipfile.BadZipFile` for garbage output); we simply move on to the
   next candidate.
3. The first password that successfully extracts data is the real one.

```python
import zipfile

with zipfile.ZipFile("secret.zip") as zf:
    member = zf.namelist()[0]
    for pwd in candidates:
        try:
            data = zf.read(member, pwd=pwd.encode())
            print("cracked:", pwd, data)
            break
        except RuntimeError:
            continue
```

4. Read the extracted `secret.txt` contents — that's the flag.

## Running it

```
$ python3 solve.py
[+] cracked password: dragon
flag{z1p_p4ssw0rds_ar3nt_r3al_s3curity}
```

## Takeaway

Zip's classic ("ZipCrypto") password protection is not real encryption by
modern standards, and even where it is used, a weak/common password makes
the archive trivial to open via dictionary or brute-force attack. Use
strong, unique, randomly generated passwords and prefer AES-256 zip
encryption (or better, a dedicated encrypted container/tool) for anything
sensitive.
