#!/usr/bin/env python3
"""
sqli-login: a tiny Flask + sqlite3 login form vulnerable to classic
string-concatenation SQL injection in the login query.

Run: python3 app.py   (listens on 127.0.0.1:5001)
"""
import os
import sqlite3

from flask import Flask, request, jsonify

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")
FLAG = os.environ.get("APP_FLAG", "flag{sql1_1nj3ct10n_never_g3ts_0ld}")


def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, is_admin INTEGER)"
    )
    conn.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("alice", "alicepw123", 0),
    )
    conn.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("bob", "bobpassword", 0),
    )
    # The admin's real password is long and random -- not guessable/brute-forceable.
    conn.execute(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("admin", "Xk9$mQ2!vR7pL4nZ8wJ1", 1),
    )
    conn.commit()
    conn.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # VULNERABLE: query built via string formatting instead of parameters.
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        cur.execute(query)
        row = cur.fetchone()
    except sqlite3.Error as e:
        conn.close()
        return jsonify({"error": f"database error: {e}"}), 400
    conn.close()

    if row is None:
        return jsonify({"error": "invalid credentials"}), 401

    resp = {"username": row["username"], "is_admin": bool(row["is_admin"])}
    if row["is_admin"]:
        resp["flag"] = FLAG
    return jsonify(resp)


@app.route("/")
def index():
    return jsonify({
        "service": "sqli-login",
        "routes": {"POST /login": "body {username, password} -- log in as admin to get the flag"},
    })


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5001)
