#!/usr/bin/env python3
"""
jwt-none-alg: a tiny Flask app that "authenticates" users via a hand-rolled
JWT-like token, and is vulnerable to the classic alg=none bypass because it
naively decodes whatever algorithm the token header claims instead of
enforcing HS256 server-side.

Run: python3 app.py   (listens on 127.0.0.1:5000)
"""
import base64
import hashlib
import hmac
import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

SECRET = os.environ.get("APP_SECRET", "s3cr3t-signing-key-do-not-leak")
FLAG = os.environ.get("APP_FLAG", "flag{jwt_n0ne_alg_byp4ss_str1kes_ag41n}")


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def issue_token(payload: dict) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())
    signing_input = f"{header_b64}.{payload_b64}".encode()
    sig = hmac.new(SECRET.encode(), signing_input, hashlib.sha256).digest()
    sig_b64 = b64url_encode(sig)
    return f"{header_b64}.{payload_b64}.{sig_b64}"


def decode_token(token: str):
    """VULNERABLE: trusts the `alg` field from the attacker-controlled header
    instead of pinning it server-side. If alg == "none", it skips signature
    verification entirely, matching the real-world CVE-class bug in several
    early JWT library integrations."""
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError:
        return None

    header = json.loads(b64url_decode(header_b64))
    payload = json.loads(b64url_decode(payload_b64))
    alg = header.get("alg", "")

    if alg.lower() == "none":
        # No signature required/verified -- this is the bug.
        return payload

    if alg == "HS256":
        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_sig = hmac.new(SECRET.encode(), signing_input, hashlib.sha256).digest()
        actual_sig = b64url_decode(sig_b64)
        if hmac.compare_digest(expected_sig, actual_sig):
            return payload
        return None

    return None


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")
    # Only a normal, unprivileged demo account is available for login.
    if username == "guest" and password == "guest123":
        token = issue_token({"username": "guest", "admin": False})
        return jsonify({"token": token})
    return jsonify({"error": "invalid credentials"}), 401


@app.route("/admin", methods=["GET"])
def admin():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return jsonify({"error": "missing token"}), 401
    token = auth[len("Bearer "):]
    payload = decode_token(token)
    if payload is None:
        return jsonify({"error": "invalid token"}), 401
    if not payload.get("admin"):
        return jsonify({"error": "admin only"}), 403
    return jsonify({"flag": FLAG})


@app.route("/")
def index():
    return jsonify({
        "service": "jwt-none-alg",
        "routes": {
            "POST /login": "login with username/password to get a token",
            "GET /admin": "requires a Bearer token with admin=true",
        },
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
