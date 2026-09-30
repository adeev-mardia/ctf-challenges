#!/usr/bin/env python3
"""
Integration test for the whole CTF set.

For every challenge directory under categories/<category>/<name>/, this:
  1. Runs its solve.py as a subprocess (so each solve script is exercised
     exactly the way a player/grader would run it, with the challenge's
     own directory as the working directory).
  2. Reads the expected flag from solutions/<category>/<name>/flag.txt.
  3. Asserts the solve script's output contains the expected flag.

Run with:  python3 verify_all.py
Exits non-zero if any challenge fails to produce its correct flag.
"""
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
CATEGORIES_DIR = os.path.join(ROOT, "categories")
SOLUTIONS_DIR = os.path.join(ROOT, "solutions")


def discover_challenges():
    challenges = []
    if not os.path.isdir(CATEGORIES_DIR):
        return challenges
    for category in sorted(os.listdir(CATEGORIES_DIR)):
        cat_path = os.path.join(CATEGORIES_DIR, category)
        if not os.path.isdir(cat_path):
            continue
        for name in sorted(os.listdir(cat_path)):
            chal_path = os.path.join(cat_path, name)
            solve_path = os.path.join(chal_path, "solve.py")
            if os.path.isdir(chal_path) and os.path.isfile(solve_path):
                challenges.append((category, name, chal_path, solve_path))
    return challenges


def expected_flag(category, name):
    flag_path = os.path.join(SOLUTIONS_DIR, category, name, "flag.txt")
    if not os.path.isfile(flag_path):
        return None
    with open(flag_path) as f:
        return f.read().strip()


def run_challenge(category, name, chal_path, solve_path, timeout=60):
    expected = expected_flag(category, name)
    if expected is None:
        return False, f"no solutions/{category}/{name}/flag.txt found"

    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "solve.py"],
            cwd=chal_path,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, f"solve.py timed out after {timeout}s"

    elapsed = time.time() - start
    output = result.stdout

    if result.returncode != 0:
        return False, (
            f"solve.py exited with code {result.returncode} "
            f"(after {elapsed:.1f}s)\nstdout:\n{output}\nstderr:\n{result.stderr}"
        )

    if expected not in output:
        return False, (
            f"expected flag {expected!r} not found in solve.py output "
            f"(after {elapsed:.1f}s)\nstdout:\n{output}\nstderr:\n{result.stderr}"
        )

    return True, f"OK ({elapsed:.1f}s) -> {expected}"


def main():
    challenges = discover_challenges()
    if not challenges:
        print("No challenges found under categories/. Nothing to verify.")
        sys.exit(1)

    print(f"Discovered {len(challenges)} challenge(s).\n")

    failures = []
    for category, name, chal_path, solve_path in challenges:
        label = f"[{category}/{name}]"
        print(f"{label:<40}", end="", flush=True)
        ok, message = run_challenge(category, name, chal_path, solve_path)
        if ok:
            print(f"PASS  {message}")
        else:
            print("FAIL")
            print(f"  -> {message}")
            failures.append((category, name, message))

    print()
    total = len(challenges)
    passed = total - len(failures)
    print(f"Result: {passed}/{total} challenges verified.")

    if failures:
        print("\nFailed challenges:")
        for category, name, message in failures:
            print(f"  - {category}/{name}")
        sys.exit(1)

    print("All challenges are genuinely solvable via their own solve.py.")
    sys.exit(0)


if __name__ == "__main__":
    main()
