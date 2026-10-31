# Assurance boundary

## What was done

1. **Written proofs** of every theorem, proposition, corollary and lemma in [manuscript/inhibitor_segregation.tex](manuscript/inhibitor_segregation.tex).
2. **Exact checks.** `verification/checks.py` makes 4,311 exact rational comparisons (generators in physical and operational time, allocation kernel normalisation and conservation, factorial moments, the branching generating-function equation, 100 scheduled-removal distributions by two independent methods, the constants of Theorem 3.2) and rejects four built-in corruptions.
3. **Validated numerics.** `enclosure/enclose_explosion.py` encloses the explosion probability of the worked example by monotone comparison, uniformisation with a Poisson tail bound and an outward rounding allowance; it rejects two corrupted parameters and a shifted claim.
4. **Simulation.** An environment-only estimator with a proved truncation bound and Hoeffding interval, and two separate direct simulations of the full chain made during review, agree with the enclosure.
5. **Internal AI-assisted review.** Round 1: editor, methodology, domain, perspective and devil's-advocate reviews and an outside-model adversarial review, plus a clean replay of every shipped script from a fresh extraction of the research bundle. One revision round with six extensions. Verification: a re-review of all changes and a proof audit of the new and rewritten proofs, followed by four targeted audits of the repairs and of the enclosure rounding argument, the last reporting no open correctness issue. A rating-free summary is in [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md); responses in [REVISION_RESPONSE.md](REVISION_RESPONSE.md).
6. **Replay.** From a fresh extraction of the frozen archive, `run_checks.py --full` and `negative_controls.py` were run in normal mode and with `-O -B`; see [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md). CI repeats the standard-library and NumPy quick checks on Linux.
7. **Citations.** Every DOI in the bibliography was checked against its Crossref or DataCite record, and arXiv entries against arXiv ([CITATION_AUDIT.md](CITATION_AUDIT.md)).

## What was not done

- No human specialist or journal peer review, no independent reproduction by an unaffiliated party, no proof-assistant formalisation.
- Priority is bounded ([PRIOR_ART.md](PRIOR_ART.md)); Yoo's full preprint could not be inspected.
- The kernels keep all substrate in one daughter (a bounded leak is allowed for the explosive direction). Molecule-blind division is not covered.
- Agreement between AI reviewers is not independent evidence.
