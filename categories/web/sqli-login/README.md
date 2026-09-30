# sqli-login

**Category:** Web
**Difficulty:** Easy

A minimal login API backed by SQLite. There's an `admin` account with the
flag, but the password is long, random, and not guessable. Find another
way in.

## Running it

```
pip install flask
python3 app.py
```

The app listens on `http://127.0.0.1:5001` and seeds its own SQLite DB on
startup (`app.db`, safe to delete/regenerate).

## Routes

- `POST /login` — body `{"username": ..., "password": ...}` → logs in; admin login returns the flag

## Hint

What happens if your username contains a SQL comment?
