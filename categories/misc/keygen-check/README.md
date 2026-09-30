# keygen-check

**Category:** Misc / Reversing
**Difficulty:** Medium

An old license checker was found on a file share. Figure out a serial
number that makes it accept, and it'll print the flag.

## Files

- `check.py` — the license checker (`python3 check.py YOUR-SERIAL`)

## Hint

Read the per-character check carefully. It's a simple arithmetic formula
applied to each character independently — can you invert it algebraically
instead of guessing?
