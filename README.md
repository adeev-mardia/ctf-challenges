# ctf-challenges

An original, fully self-contained CTF challenge set: 8 real, solvable
challenges spanning crypto, web, forensics, and misc/reversing — each with
a genuine vulnerability or puzzle, a real flag, a player-facing prompt, a
full writeup, and a working solve script. Everything runs locally; no
external services or network access required.

Every challenge's flag is proven recoverable by an automated integration
test (`verify_all.py`) that runs each `solve.py` end-to-end and checks the
returned flag against the known-correct answer — this isn't a set of
"trust me" writeups, it's verified working.

## Challenge index

| Category  | Name              | Difficulty | Description                                                        |
|-----------|-------------------|:----------:|----------------------------------------------------------------------|
| Crypto    | cube-root-rsa     | Easy       | RSA with e=3 and no padding — recover the plaintext without the key |
| Crypto    | repeating-xor     | Easy       | Break a repeating-key XOR "cipher" with no known key                |
| Web       | jwt-none-alg      | Easy       | Forge an admin JWT by exploiting the `alg: none` trust bug           |
| Web       | sqli-login        | Easy       | Bypass a login form via classic SQL injection                       |
| Forensics | lsb-stego         | Easy       | Extract a flag hidden in a PNG's pixel LSBs                         |
| Forensics | weak-zip          | Easy       | Crack a weakly-password-protected zip via dictionary attack         |
| Misc      | encoding-layers   | Easy       | Peel back a chain of five different encodings                       |
| Misc      | keygen-check      | Medium     | Reverse-engineer and algebraically invert a serial-number checksum  |

No spoilers above — see each challenge's own `README.md` for the exact
player-facing prompt, and `writeup.md` for the full solve walkthrough.

## Repository layout

```
categories/<category>/<challenge-name>/
    README.md      # player-facing prompt (no spoilers)
    writeup.md      # full solve walkthrough
    solve.py        # automated end-to-end solver, prints the flag
    generate.py      # (where applicable) reproducible generator for challenge artifacts
    <challenge files> # the actual runnable/openable challenge (app.py, ciphertext, image, zip, ...)

solutions/<category>/<challenge-name>/flag.txt   # ground-truth flag, kept out of the public challenge dirs

verify_all.py     # integration test: runs every solve.py, checks the flag
requirements.txt
LICENSE
```

## Setup

```bash
git clone https://github.com/adeev-mardia/ctf-challenges.git
cd ctf-challenges
pip install -r requirements.txt
```

Some forensics challenges' `generate.py` shells out to the system `zip`
CLI to build a genuinely ZipCrypto-encrypted archive (`apt-get install
zip` / `brew install zip` if you don't already have it) — this is only
needed if you want to regenerate challenge artifacts; the pre-built
artifacts are already committed and don't require it to solve.

## Running a challenge

Each challenge directory is self-contained. Read its `README.md` for the
prompt, then:

- **Crypto / Forensics / Misc** challenges are static files — just open
  them (`public.txt`, `cover.png`, `secret.zip`, `message.txt`,
  `check.py`) with whatever tools you like.
- **Web** challenges are small Flask apps — run them directly:

  ```bash
  cd categories/web/jwt-none-alg
  python3 app.py
  # in another terminal:
  curl -X POST http://127.0.0.1:5000/login -H 'Content-Type: application/json' \
       -d '{"username":"guest","password":"guest123"}'
  ```

To see (or automate) the actual solve for any challenge:

```bash
cd categories/<category>/<challenge-name>
python3 solve.py
```

Web challenges' `solve.py` scripts boot their own Flask app as a
subprocess, attack it over HTTP, and tear it down — no manual server
startup needed to reproduce the solve.

## Verifying the whole set

```bash
python3 verify_all.py
```

This discovers every challenge under `categories/`, runs its `solve.py`,
and asserts the flag it prints matches `solutions/<category>/<name>/flag.txt`.
Expected output:

```
Discovered 8 challenge(s).

[crypto/cube-root-rsa]                  PASS  OK (0.0s) -> flag{...}
[crypto/repeating-xor]                  PASS  OK (0.2s) -> flag{...}
[forensics/lsb-stego]                   PASS  OK (0.1s) -> flag{...}
[forensics/weak-zip]                    PASS  OK (0.0s) -> flag{...}
[misc/encoding-layers]                  PASS  OK (0.0s) -> flag{...}
[misc/keygen-check]                     PASS  OK (0.1s) -> flag{...}
[web/jwt-none-alg]                      PASS  OK (0.4s) -> flag{...}
[web/sqli-login]                        PASS  OK (0.4s) -> flag{...}

Result: 8/8 challenges verified.
All challenges are genuinely solvable via their own solve.py.
```

## Difficulty / scoring guide

| Difficulty | Suggested points | Meaning                                                          |
|------------|:-----------------:|-------------------------------------------------------------------|
| Easy       | 100                | One core insight, straightforward to script once you see it       |
| Medium     | 250                | Requires combining a couple of steps or careful algebraic/manual reasoning |
| Hard       | 400+               | Not used in this set yet — a good place to extend it              |

## License

MIT — see [LICENSE](LICENSE).
