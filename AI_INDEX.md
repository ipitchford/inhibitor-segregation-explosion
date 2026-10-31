# Agent navigation

## Identity

- Release slug: `inhibitor-segregation-explosion`. Version `1.0.0-candidate`, tag `v1.0.0-candidate`. DOI 10.5281/zenodo.23837953; concept DOI 10.5281/zenodo.23837952.
- Repository: https://github.com/ipitchford/inhibitor-segregation-explosion. Release page: https://evidencepress.org/releases/inhibitor-segregation-explosion/
- Scholarly creator: Anonymous. Status: unrefereed candidate ([STATUS.md](STATUS.md)).
- Manuscript: [PDF](manuscript/inhibitor_segregation.pdf) and its self-contained [LaTeX source](manuscript/inhibitor_segregation.tex); figure [phase_diagram.pdf](manuscript/phase_diagram.pdf) drawn by [phase_figure.py](manuscript/phase_figure.py).
- Machine-readable claims: [CLAIMS.json](CLAIMS.json). Human overview: [README.md](README.md).
- Assurance limits: [ASSURANCE.md](ASSURANCE.md). Review record: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md), [REVISION_RESPONSE.md](REVISION_RESPONSE.md).
- Prior art and sources: [PRIOR_ART.md](PRIOR_ART.md), [RESEARCH_GATES.json](RESEARCH_GATES.json), [SOURCES.md](SOURCES.md), [CITATION_AUDIT.md](CITATION_AUDIT.md). Provenance: [PROVENANCE.md](PROVENANCE.md).
- Citation: [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json). Licences: [LICENSES.md](LICENSES.md).

## Scientific map

Object: the compartment model of Anderson, Howells and Rojas La Luz (2026) with no inflow, exit or coagulation; division at rate lambda*s; a substrate-keeping kernel retaining each inhibitor with probability Q (fresh at each division). Question: can a nonexplosive chemistry explode once compartmentalised without inflow reactions?

- Proposition 2.2: single-lineage reduction for substrate-keeping kernels. Lemma 2.4: marked environment and random time change.
- Theorem 3.1: conversion inhibition (2S->3S, S->S+I, S+I->2I; d>b): explosion with positive probability iff d+lambda log p<b; equality nonexplosive; exact Poisson-binomial conditional law. Theorem 3.2: P(explosion)>=1-K/(s0-1); 1/2 for the example. Theorem 3.3: blow-up asymptotics.
- Lemma 3.4 (scheduled removals), Lemma 3.6 (upper growth), Lemma 3.7 (successful immigrant).
- Theorem 4.1: catalytic inhibition (I+2S->I+S): threshold b lambda(1-p)>dc; Kendall conditional law; Lemma 4.2 regeneration.
- Theorems 5.1-5.2: random retention (E log Q versus E Q); Example 5.3: same mean, different phase.
- Theorem 6.1, Corollary 6.2, Proposition 6.3: comparison with well-mixed degradation S+I->S. Proposition 6.4: monotonicity and continuity at threshold. Proposition 6.5: bounded substrate leakage.
- Section 7.1: enclosure P in [0.79744, 0.79751] for b=c=1, d=2, lambda=3, p=0, (S,I)=(3,0). Section 7.2: estimator. Section 8: scope and open questions.

## Evidence and replay

- Runner: [run_checks.py](run_checks.py) (default: standard library, exact comparison; `--numpy`; `--full`).
- Exact checks: [verification/checks.py](verification/checks.py) -> [verification/results.json](verification/results.json).
- Estimator: [verification/estimate_explosion.py](verification/estimate_explosion.py) -> [verification/explosion_estimate.json](verification/explosion_estimate.json).
- Enclosure: [enclosure/enclose_core.py](enclosure/enclose_core.py), [enclosure/enclose_explosion.py](enclosure/enclose_explosion.py) -> [enclosure/enclosure_results.json](enclosure/enclosure_results.json) (full) and [enclosure/enclosure_quick.json](enclosure/enclosure_quick.json) (quick).
- Semantic negative controls: [negative_controls.py](negative_controls.py) (4 corruptions). Environment: [pyproject.toml](pyproject.toml), [uv.lock](uv.lock), [ENVIRONMENT.txt](ENVIRONMENT.txt). CI: [.github/workflows/replay.yml](.github/workflows/replay.yml). Replay record: [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md). Integrity: [SHA256SUMS](SHA256SUMS).

## Trust boundary

All review was internal and AI-assisted. There was no peer review, no independent reproduction and no formal verification. Finite checks audit algebra, constants and one numerical value; they do not prove the infinite-time theorems. The enclosure's rounding argument is written out but not machine-checked. Priority holds only within a bounded search; Yoo (2026) already reported a counterexample to the unrestricted conjecture using inflow and fusion. Molecule-blind division kernels are not covered.
