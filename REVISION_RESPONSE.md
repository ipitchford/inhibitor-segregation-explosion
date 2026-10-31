# Revision response (31 October 2026)

The 28 October draft was reviewed by six internal AI-assisted reviews: methodology and devil's-advocate reviews (Claude subagent), editor, domain and perspective reviews (Astra via codex-companion-once), and an adversarial review (OpenAI gpt-5.6-sol). A clean replay of the bundled scripts reproduced every recorded output. No review found a mathematical error or counterexample; the issues concerned rigour of presentation, framing, attribution and significance. They were merged into one fix list and handled in one revision. Most were resolved; the items not done are listed at the end.

## Correctness and rigour

| Issue | Source | Disposition |
|---|---|---|
| Joint measurability and stationarity of the successful-immigrant probability (A.7) | Sol A1, Methodology W2(d) | Lemma 3.7 now defines the probability as a measurable shift functional, proves positivity by conditional Paley-Zygmund, and uses Birkhoff's ergodic theorem. |
| Pre/post-catastrophe normalisation in the second moment | Sol A2 | Stated explicitly (post-division value, right-continuous mean). |
| Empty daughters admissible and counted? | Sol A3/B4 | Checked in the source text (state space includes the zero vector; kernels need only conserve mass). Section 2.1 states this. Proposition 2.2 also shows the phase boundary does not depend on counting silent divisions. |
| Compensator/localisation argument compressed | Sol A4, Methodology W2(b) | Written out in Section 3.5. |
| Time change and conditional construction asserted, not stated | Sol B1, Methodology W1 | New Lemma 2.4 (graphical construction and random time change, citing Ethier-Kurtz). |
| Forward equation only almost everywhere | Sol B2 | Stated in Section 4.3. |
| Uniformised chain is not the jump chain; attempt-block exponential moments | Sol B3, Methodology W2(c) | Lemma 4.2 rewritten with the uniform dominated-convergence step. |
| Lyapunov step for p = 0 needs localisation | Methodology W2(a) | Added (Dynkin with stopping and Fatou). |
| Random-Q second moment needs Q > 0 | Methodology | Stated: gamma >= b forces E log Q > -infinity. |
| Critical random walk: nonnegativity of the stopped martingale | Sol C2 | One argument, valid for fixed and random retention, with the bounded-overshoot reason stated. |
| Labelled coupling for E log Q = -infinity | Sol C3 | Written as an explicit labelled graphical construction. |
| C.2 "every step follows" | Sol C4 | Changes listed, including positive cycle variance. |
| Estimator error control only for Delta > 0 | Methodology W4 | Stated in Section 7.2. |
| Catalytic numerics converge slowly | Methodology W5, DA m7 | Remark 4.3. |
| Broken typesetting, numbering | Methodology W3, EIC, Perspective | Manuscript rewritten in LaTeX with theorem environments and cross-references. |

## Framing, attribution and readability

- Observation 3.7 of the source is quoted and the result is framed as its reverse side: compartments slow every multi-reactant reaction, which destabilises when the slowed reaction is inhibitory (DA M2, EIC E1, Domain D1). The rate inequality itself is not disputed.
- Companion release (DOI 10.5281/zenodo.23505123) cited and compared (EIC E2, Domain D4, Perspective P4).
- Classical components cited at the point of use: Kaplan-Sudbury-Nilsen, Hermann-Pfaffelhuber, Bansaye-Pardo-Smadi, Gallo-Roldan-Correa, Brockwell-Gani-Resnick, Cogburn-Torrez, Pakes, Braun, published version of Leskela-Robert-Simatos (DA M5, Methodology W7, Domain D2). The Poisson-binomial identity is presented as an elementary lemma without priority claim (Domain D3, Sol II.2).
- "Restricted-class classification" replaced by "sharp classification within each of the two families" (DA M4).
- Internal-process material, the author line and the REF references removed (Methodology W6, DA m6, EIC E3). AI-assistance statement consolidated in one footnote.
- New first pages: question, meaning of explosion, example, results table, mechanism, contribution map, reading guide, notation table, and a plain-language summary at the start of each section (Perspective P1-P3).
- Molecule-blind kernels stated as open; fragile versus robust nonexplosion discussed (DA M3, m3).

## Extensions added

1. Proposition 2.2: single-lineage reduction for any chemistry whose reactions all need the substrate, under any substrate-keeping kernel (DA E1).
2. Theorem 6.1 and Corollary 6.2: conversion chemistry with an added well-mixed degradation reaction; exact threshold d - delta + lambda E log Q < b. Bulk export at division is strictly more destabilising than well-mixed removal at the same mean rate; the gap is the purely compartmental effect (DA M1, Domain D-X1).
3. Proposition 6.3: for catalytic inhibition, bulk and well-mixed removal give the same threshold.
4. Proposition 6.4: monotonicity in retention and division rate, and continuity of the explosion probability at both thresholds (Methodology ext. 3, DA E5, Perspective P-X2).
5. Proposition 6.5: explosion persists when each division leaks a bounded number of substrate molecules (EIC E-X1).
6. Section 7.1: two-sided enclosure of the headline explosion probability, [0.79744, 0.79751], plus s0 = 2 and 4, with written truncation and rounding control (Methodology ext. 1, DA E3).

## Verification round

A re-review and proof audit of the revision (Astra via codex-companion-once, OpenAI gpt-6-astra) found no counterexample to either phase boundary and seven repairable defects. All were fixed. Four further targeted audits (same route) checked the repairs; they confirmed the mathematical repairs and found further gaps in the enclosure's rounding argument (domain of validity, underflow, cancellation in Delta, decimal context), which were fixed in turn until the last audit reported no open correctness issue:

| Finding | Fix |
|---|---|
| Proposition 2.2 used the designated daughter's law instead of the substrate daughter's | Pushforward kernel ψ̂(x,z) = ψ(x,z) + ψ(x,x−z). |
| Conditioning on the unmarked inhibitor path does not determine the conversion times | Marked environment E (inhibitor path with event types) introduced in Lemma 2.4; all conversion conditional laws use it. |
| Lemma 2.4 confused Z = 0 with S = 0 and lacked a catalytic death driver | Time change stated up to the hitting of Z = 0, with separate handling afterwards; independent death random measure added. |
| Lemma 3.7 measurable version used probabilities that can fail at atoms | Replaced by limits of E[min{1, k M(n)}]. |
| Theorem 6.1 undefined when λ = 0 and E log Q = −∞ | Convention λ E log Q = 0 when λ = 0. |
| Proposition 6.5 individual-level coupling impossible | Ordered count coupling (x−K)+ ≤ (y−ℓ)+, killed variable, and inhibitor thinning sampled before leakage for schedule independence. |
| Enclosure rounding argument unproved; unstable mean formula; underflow; p = 1 crash; cancellation in Delta; ambient decimal context | Code rewritten: stable mean formula, exact rational Delta, dyadic steps, private 50-digit decimal context for exponentials, weights and payoffs with conservative conversion that never goes below 0, relative and absolute (underflow) allowances, explicit error budget, and refusal of inputs outside the covered domain (p = 0, rates in [1/16, 16], z ≤ 10, N ≤ 2000, U ≤ 64, steps ≤ 1/64, exact binary64 inputs, at most 80 Poisson terms). |
| Wording: "slows down every reaction", "only because d > b", "decided early", "on every explosion path", "independent of Z", leakage and bulk-removal scope | Corrected throughout. |

## Not done

- Molecule-blind (fair) allocation (DA E2): open, discussed in Section 8.
- General robust-versus-fragile dichotomy (DA E4): discussed, not proved.
- Capped regularisations (Perspective P-X1), finite-level hitting probabilities (EIC E-X2), rare alternative allocations (Domain D-X2), whole-region estimator error control and certified catalytic numerics: not attempted.
- A division diagram (Perspective P1) and the Berzunza Ojeda–Pardo comparison (Domain D2): not added.
- Yoo's full preprint could not be inspected; no first-disproof claim is made.
