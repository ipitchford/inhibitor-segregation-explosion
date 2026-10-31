# Inhibitor segregation can make a nonexplosive reaction network explode

**Version 1.0.0-candidate (31 October 2026).** DOI [10.5281/zenodo.23837953](https://doi.org/10.5281/zenodo.23837953) (concept DOI 10.5281/zenodo.23837952). Release page: <https://evidencepress.org/releases/inhibitor-segregation-explosion/>.

**Status:** unrefereed, AI-assisted research candidate. Internal AI-assisted review only; not peer reviewed, independently reproduced or formally verified. Creator: Anonymous. Text and data CC0-1.0, code MIT.

## The result in brief

A stochastic chemical system *explodes* when infinitely many reaction events happen in a finite time. Anderson, Howells and Rojas La Luz (Bull. Math. Biol. 88, 106, 2026) conjectured that a nonexplosive chemistry stays nonexplosive inside dividing compartments, and suggested that inflow reactions are the main danger. Yoo (2026) has already reported a counterexample using inflow and compartment fusion; no first-disproof claim is made here.

This package shows that removing every inflow reaction, and all fusion and exit, does **not** prevent compartment-induced explosion. Two two-species chemistries are nonexplosive alone, yet explode with positive probability when compartments divide at rate λs, every division keeps all substrate S in one daughter, and each inhibitor I stays with it with (random) probability Q:

| | Conversion inhibition | Catalytic inhibition |
|---|---|---|
| Reactions (propensities) | 2S→3S (bs(s−1)), S→S+I (cs), S+I→2I (dsi), d>b | 2S→3S, S→S+I, I+2S→I+S (dis(s−1)) |
| Explosion with positive probability iff | d + λ E[log Q] < b | bλ(1 − E Q) > dc |
| Boundary | nonexplosive | nonexplosive |
| Well-mixed removal at the same mean rate | b + λ(1 − E Q) > d (strictly smaller region) | same threshold |

Also proved: an exact conditional (Poisson-binomial or Kendall) explosion law, blow-up asymptotics, monotonicity and continuity of the explosion probability at the thresholds, robustness to bounded substrate leakage, and an analytic bound P(explosion) ≥ 1/2 for b=c=1, d=2, λ=3, Q≡0 from (S,I)=(3,0). A validated computation encloses that probability in [0.79744, 0.79751].

The probabilistic ingredients (branching with catastrophes, Yule processes with scheduled removals, linear birth–death processes in random environments, random time change) are classical and cited. The contribution is the chemical construction, its exact reduction and the sharp classification within the two families.

## Contents

| Path | What it is |
|---|---|
| `manuscript/inhibitor_segregation.pdf`, `.tex` | The paper (24 pages) and its LaTeX source; `phase_diagram.*` and `phase_figure.py` draw Figure 1 |
| `verification/checks.py`, `results.json` | 4,311 exact rational checks (standard library), with four built-in rejected corruptions |
| `verification/estimate_explosion.py`, `explosion_estimate.json` | Environment-only Monte Carlo estimator with truncation and Hoeffding bounds (NumPy) |
| `enclosure/` | Validated two-sided enclosure of the example probability (NumPy); `enclosure_results.json` (full), `enclosure_quick.json` (quick) |
| `run_checks.py` | Replays the checks in a temporary copy and compares with the retained outputs |
| `negative_controls.py` | Four claim-relevant corruptions that must be rejected |
| `CLAIMS.json`, `AI_INDEX.md` | Machine-readable claims and an agent index |
| `STATUS.md`, `ASSURANCE.md`, `PROVENANCE.md`, `REVIEW_SUMMARY.md`, `REVISION_RESPONSE.md` | Status, assurance boundary, provenance, rating-free review summary and responses |
| `PRIOR_ART.md`, `SOURCES.md`, `CITATION_AUDIT.md`, `RESEARCH_GATES.json` | Prior-art scope and reference audit |
| `LICENSE`, `LICENSE-MIT.txt`, `LICENSES.md`, `PUBLIC_DOMAIN.md` | Licences |
| `SHA256SUMS` | Checksums of every other file |

## Reproduce

With Python 3.11 or later, from the package root:

```sh
shasum -a 256 -c SHA256SUMS
python3 run_checks.py                      # exact checks, standard library only
python3 -O run_checks.py                   # identical: no assert statements are used
pip install numpy==2.3.5
python3 run_checks.py --numpy              # adds the estimator and the quick enclosure
python3 run_checks.py --full               # adds the full enclosure (about two minutes)
python3 negative_controls.py               # every corruption must be rejected
```

`pyproject.toml` and `uv.lock` pin NumPy 2.3.5 and Matplotlib 3.10.8 (`uv run python3 run_checks.py --full`). The checks verify algebra, constants and one numerical value; the infinite-time theorems rest on the written proofs.

## Cite

Anonymous (2026). *Inhibitor segregation can make a nonexplosive reaction network explode.* Version 1.0.0-candidate. Evidence Press. https://doi.org/10.5281/zenodo.23837953
