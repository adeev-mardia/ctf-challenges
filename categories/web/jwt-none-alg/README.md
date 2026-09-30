# jwt-none-alg

**Category:** Web
**Difficulty:** Easy

A tiny internal admin panel issues its own JWT-style tokens after login.
There's a `guest` demo account, but the flag is behind `/admin`, which
requires `admin: true` in your token. Can you get admin without knowing
any admin credentials?

## Running it

```
pip install flask
python3 app.py
```

The app listens on `http://127.0.0.1:5000`.

## Routes

- `POST /login` — body `{"username": "guest", "password": "guest123"}` → returns a Bearer token
- `GET /admin` — requires `Authorization: Bearer <token>` with `admin: true` in the payload → returns the flag

## Hint

Look closely at how the server decides whether to check the signature at
all. JWT headers are attacker-controlled...
