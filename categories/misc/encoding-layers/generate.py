#!/usr/bin/env python3
"""Generator for encoding-layers: applies a genuine multi-stage encoding
chain to the flag: flag -> ROT13 -> hex -> base64 -> base32 -> reverse."""
import base64
import codecs

FLAG = "flag{lay3rs_0f_3nc0d1ng_ar3nt_crypt0}"


def encode(plaintext: str) -> str:
    stage1 = codecs.encode(plaintext, "rot13")                 # rot13
    stage2 = stage1.encode().hex()                              # hex
    stage3 = base64.b64encode(stage2.encode()).decode()         # base64
    stage4 = base64.b32encode(stage3.encode()).decode()         # base32
    stage5 = stage4[::-1]                                       # reverse
    return stage5


def main():
    encoded = encode(FLAG)
    with open("message.txt", "w") as f:
        f.write(encoded + "\n")
    print("Wrote message.txt")
    print(encoded)


if __name__ == "__main__":
    main()
