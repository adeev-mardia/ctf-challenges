#!/usr/bin/env python3
"""Generator for weak-zip: creates a password-protected zip (using classic
ZipCrypto, the standard 'zip -e' encryption, so it's crackable via a
dictionary attack) containing a flag file. The password is a common,
wordlist-guessable password planted among a small bundled wordlist."""
import subprocess
import os

FLAG = "flag{z1p_p4ssw0rds_ar3nt_r3al_s3curity}"
PASSWORD = "dragon"  # a genuinely common/weak password

WORDLIST = [
    "123456", "password", "letmein", "qwerty", "dragon", "monkey",
    "football", "iloveyou", "admin", "welcome", "sunshine", "master",
    "abc123", "trustno1", "princess", "shadow", "superman", "baseball",
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    secret_path = os.path.join(here, "secret.txt")
    with open(secret_path, "w") as f:
        f.write(FLAG + "\n")

    zip_path = os.path.join(here, "secret.zip")
    if os.path.exists(zip_path):
        os.remove(zip_path)

    # Use the `zip` CLI's classic (ZipCrypto) encryption, which is what
    # `zip -e` produces -- genuinely crackable, unlike AES zip encryption.
    subprocess.run(
        ["zip", "-j", "-e", "-P", PASSWORD, zip_path, secret_path],
        check=True,
        stdout=subprocess.DEVNULL,
    )
    os.remove(secret_path)

    wordlist_path = os.path.join(here, "wordlist.txt")
    with open(wordlist_path, "w") as f:
        f.write("\n".join(WORDLIST) + "\n")

    print("Created secret.zip (password-protected) and wordlist.txt")


if __name__ == "__main__":
    main()
