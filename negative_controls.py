#!/usr/bin/env python3
"""Semantic negative controls: claim-relevant corruptions must be rejected.

1. A corrupted retained exact-check result (wrong number of exact comparisons) must fail run_checks.py.
2. A corrupted retained headline constant (the analytic lower bound 1/2 replaced by 2/3) must fail.
3. A shifted published enclosure claim must be rejected by the enclosure script (quick mode).
4. A corrupted model parameter (division coefficient 2.5 instead of 3) must give an enclosure
   outside the published claim (checked inside the enclosure script, quick mode).
Controls 3 and 4 need NumPy and are skipped, with a message, if it is unavailable.
Exit status is nonzero if any corruption is accepted. No assert statements.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def copy_pkg(d):
    tmp = Path(d) / "pkg"
    for name in ("verification", "enclosure"):
        shutil.copytree(ROOT / name, tmp / name)
    shutil.copy(ROOT / "run_checks.py", tmp / "run_checks.py")
    return tmp

def rejected(cmd, cwd):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True).returncode != 0

def main():
    results = {}
    with tempfile.TemporaryDirectory() as d:
        tmp = copy_pkg(d)
        p = tmp / "verification" / "results.json"; r = json.loads(p.read_text())
        r["exact_checks"] = r["exact_checks"] + 1; p.write_text(json.dumps(r, indent=2) + "\n")
        results["wrong_exact_check_count"] = rejected([sys.executable, "-B", "run_checks.py"], tmp)
    with tempfile.TemporaryDirectory() as d:
        tmp = copy_pkg(d)
        p = tmp / "verification" / "results.json"; txt = p.read_text()
        if '"1/2"' not in txt:
            print("baseline constant 1/2 not found in results.json"); sys.exit(1)
        p.write_text(txt.replace('"1/2"', '"2/3"', 1))
        results["wrong_headline_bound"] = rejected([sys.executable, "-B", "run_checks.py"], tmp)
    try:
        import numpy  # noqa: F401
        have_numpy = True
    except ImportError:
        have_numpy = False
    if have_numpy:
        with tempfile.TemporaryDirectory() as d:
            tmp = copy_pkg(d)
            s = tmp / "enclosure" / "enclose_explosion.py"; txt = s.read_text()
            s.write_text(txt.replace("CLAIM_QUICK = {2: (0.7965, 0.7985)}", "CLAIM_QUICK = {2: (0.7900, 0.7960)}"))
            results["shifted_enclosure_claim"] = rejected([sys.executable, "-B", str(s), "--quick"], tmp)
        with tempfile.TemporaryDirectory() as d:
            tmp = copy_pkg(d)
            s = tmp / "enclosure" / "enclose_explosion.py"; txt = s.read_text()
            s.write_text(txt.replace("EXAMPLE = dict(b=1.0, c=1.0, d=2.0, lam=3.0,", "EXAMPLE = dict(b=1.0, c=1.0, d=2.0, lam=2.5,"))
            results["wrong_division_coefficient"] = rejected([sys.executable, "-B", str(s), "--quick"], tmp)
    else:
        print("NumPy unavailable: enclosure controls skipped")
    print(json.dumps(results, indent=2))
    if not all(results.values()):
        print("A CORRUPTION WAS ACCEPTED"); sys.exit(1)
    print(f"all {len(results)} corruptions rejected")

if __name__ == "__main__":
    main()
