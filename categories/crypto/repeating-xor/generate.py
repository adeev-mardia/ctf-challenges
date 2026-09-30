#!/usr/bin/env python3
"""Generator for repeating-xor challenge: encrypts a plaintext blob (English
text containing the flag) with a short repeating-key XOR cipher, hex-encodes it."""
import binascii

KEY = b"n1nja"  # 5-byte key, secret to players
FLAG = "flag{r3p3at1ng_k3y_x0r_1s_n0t_3ncrypt10n}"

PLAINTEXT = f"""SECURE TRANSMISSION - PRIORITY ONE
FROM: FIELD OFFICE ALPHA
TO: COMMAND

The shipment has been delayed due to weather conditions along the northern
route. We expect to resume operations by Thursday morning at the latest.
All personnel have been briefed on the updated schedule and contingency
plans are in place should further delays occur.

In the meantime, please find below the authentication string required for
the next phase of the operation. Treat this transmission as classified and
destroy after reading. Do not transmit over unsecured channels.

AUTH STRING: {FLAG}

Further updates will follow as the situation develops. Maintain radio
silence unless there is an emergency. End of message.
""".encode()


def xor_encrypt(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))


def main():
    ct = xor_encrypt(PLAINTEXT, KEY)
    with open("ciphertext.hex", "w") as f:
        f.write(binascii.hexlify(ct).decode())
    print("key:", KEY)
    print("wrote ciphertext.hex, length", len(ct))


if __name__ == "__main__":
    main()
