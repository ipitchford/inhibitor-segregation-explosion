#!/usr/bin/env python3
"""Validated enclosure of the explosion probability for the worked example
(b=c=1, d=2, lambda=3, p=0, initial (S,I)=(s0,0)), from the exact identity
P(T<inf) = E[P(K_inf < s0-1 | inhibitor environment)].

Usage:  python enclosure/enclose_explosion.py           # full run (about 2 minutes)
        python enclosure/enclose_explosion.py --quick   # coarse run (seconds)
Writes enclosure/enclosure_results.json (full) or enclosure_quick.json (quick).
Requires NumPy.  Fails with a nonzero exit status (RuntimeError) on any check failure;
no assert statements are used, so the checks also run under python -O.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from enclose_core import enclose, fail   # noqa: E402

HERE = Path(__file__).resolve().parent
EXAMPLE = dict(b=1.0, c=1.0, d=2.0, lam=3.0, p=0.0, i0=0)
FULL = dict(N=800, U=18.0, h0=5e-5, hmax=0.01)
QUICK = dict(N=150, U=16.0, h0=2e-3, hmax=2 ** -6)
# Published claims (outward-rounded); the computed enclosure must lie inside them.
CLAIM_FULL = {1: (0.58865, 0.58870), 2: (0.79744, 0.79751), 3: (0.88702, 0.88709)}
CLAIM_QUICK = {2: (0.7965, 0.7985)}

def main():
    quick = "--quick" in sys.argv
    grid = QUICK if quick else FULL
    claims = CLAIM_QUICK if quick else CLAIM_FULL
    zs = [2] if quick else [1, 2, 3]
    out = {"model": EXAMPLE, "grid": grid, "results": {}, "checks": {}}
    for z in zs:
        lo, hi, steps = enclose(z=z, **EXAMPLE, **grid)
        if not (0.0 <= lo <= hi <= 1.0):
            fail(f"invalid enclosure for z={z}: {lo}, {hi}")
        out["results"][f"s0={z+1}"] = {"lower": lo, "upper": hi, "width": hi - lo, "time_steps": steps}
    for z in zs:
        r = out["results"][f"s0={z+1}"]
        a, b = claims[z]
        if not (a <= r["lower"] and r["upper"] <= b):
            fail(f"enclosure for s0={z+1} not inside claimed [{a},{b}]")
    out["checks"]["inside_published_claims"] = {f"s0={z+1}": list(claims[z]) for z in zs}
    lo, hi = out["results"]["s0=3"]["lower"], out["results"]["s0=3"]["upper"]
    a, b = claims[2]
    if not lo >= 0.5:
        fail("enclosure contradicts the analytic lower bound 1/2")
    out["checks"]["above_analytic_bound_one_half"] = True
    mc = (0.7936688713706909, 0.7998332837881452)   # Hoeffding interval of the bundled estimator
    if hi < mc[0] or lo > mc[1]:
        fail("enclosure disjoint from the Monte Carlo interval")
    out["checks"]["meets_monte_carlo_interval"] = list(mc)
    if not quick:
        p1, p2, p3 = (out["results"][k] for k in ("s0=2", "s0=3", "s0=4"))
        if not (p1["upper"] < p2["lower"] and p2["upper"] < p3["lower"]):
            fail("explosion probability should increase with the initial substrate")
        out["checks"]["increasing_in_s0"] = True
    # Negative controls: corrupted inputs must be rejected by the same comparisons.
    neg = {}
    lo2, hi2, _ = enclose(z=2, **{**EXAMPLE, "lam": 2.5}, **QUICK)
    neg["division_rate_2.5_rejected"] = not (a <= lo2 and hi2 <= b)
    lo3, hi3, _ = enclose(z=2, **{**EXAMPLE, "d": 2.25}, **QUICK)
    neg["conversion_rate_2.25_rejected"] = not (a <= lo3 and hi3 <= b)
    neg["shifted_claim_rejected"] = not (0.7960 <= lo and hi <= 0.7970)
    if not all(neg.values()):
        fail(f"a negative control was not rejected: {neg}")
    out["negative_controls"] = neg
    out["status"] = "PASS"
    out["claim_limit"] = ("Two-sided bounds from monotone comparisons, uniformisation with an added Poisson tail, exact dyadic "
                          "time steps, decimal (50-digit) exponentials, weights and payoffs with conservative conversion, and an "
                          "outward relative factor 1e-13 per floating-point operator step; the rounding argument (enclose_core.py "
                          "docstring and manuscript Section 7.1) covers p = 0, N <= 2000, steps <= 1/64 and assumes IEEE-754 binary64 "
                          "arithmetic with correctly rounded basic operations. Written out, not machine-checked.")
    target = HERE / ("enclosure_quick.json" if quick else "enclosure_results.json")
    target.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
