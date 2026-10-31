#!/usr/bin/env python3
"""Replay the package's finite checks in an isolated temporary copy and compare with retained outputs.

Default (standard library only): verification/checks.py, compared exactly with verification/results.json.
--numpy: also verification/estimate_explosion.py (compared with tolerance) and the quick enclosure
         (enclosure/enclose_explosion.py --quick, compared with tolerance and its own claim checks).
--full:  also the full enclosure (about two minutes), compared with enclosure/enclosure_results.json.
Retained outputs are never overwritten. Exit status is nonzero on any failure; no assert statements.
These finite checks do not prove the infinite-time theorems, which rest on the written proofs.
"""
import argparse, json, math, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IGNORE = {"numpy_version"}
REL, ABS = 1e-9, 1e-12

def norm(v):
    if isinstance(v, dict):
        return {k: norm(x) for k, x in v.items() if k not in IGNORE}
    if isinstance(v, list):
        return [norm(x) for x in v]
    return v

def close(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b if isinstance(a, int) and isinstance(b, int) else math.isclose(a, b, rel_tol=REL, abs_tol=ABS)
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(close(a[k], b[k]) for k in a)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    return a == b

def run(tmp, script, args, out, exact):
    expected = json.loads((ROOT / out).read_text())
    cmd = [sys.executable, "-B", str(tmp / script)] + args
    proc = subprocess.run(cmd, cwd=str(tmp), capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stdout[-2000:], proc.stderr[-2000:])
        return False, f"{script} exited with {proc.returncode}"
    got = json.loads((tmp / out).read_text())
    ok = norm(got) == norm(expected) if exact else close(norm(got), norm(expected))
    return ok, f"{script} {' '.join(args)}: {'match' if ok else 'MISMATCH'} ({'exact' if exact else 'tolerance'})"

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--numpy", action="store_true")
    ap.add_argument("--full", action="store_true")
    a = ap.parse_args()
    jobs = [("verification/checks.py", [], "verification/results.json", True)]
    if a.numpy or a.full:
        jobs += [("verification/estimate_explosion.py", [], "verification/explosion_estimate.json", False),
                 ("enclosure/enclose_explosion.py", ["--quick"], "enclosure/enclosure_quick.json", False)]
    if a.full:
        jobs += [("enclosure/enclose_explosion.py", [], "enclosure/enclosure_results.json", False)]
    failures = 0
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / "pkg"
        shutil.copytree(ROOT / "verification", tmp / "verification")
        shutil.copytree(ROOT / "enclosure", tmp / "enclosure")
        for script, args, out, exact in jobs:
            ok, msg = run(tmp, script, args, out, exact)
            print(("PASS " if ok else "FAIL ") + msg)
            failures += not ok
    print("ALL PASS" if failures == 0 else f"{failures} FAILURE(S)")
    sys.exit(1 if failures else 0)

if __name__ == "__main__":
    main()
