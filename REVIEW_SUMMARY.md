# Review summary (rating-free)

All review was internal and AI-assisted; none of it is external peer review.

**Round 1 (31 October 2026).** Six reviews of the 28 October draft: methodology and devil's-advocate reviews (Claude subagent), editor, domain and perspective reviews (OpenAI Codex, gpt-6-astra), and an adversarial correctness review (OpenAI gpt-5.6-sol). A clean replay of every shipped script from a fresh extraction of the research bundle reproduced all recorded outputs bit for bit, and a separate direct simulation of the full chain agreed with the headline estimate.

**Findings.** No review found a mathematical error or counterexample to the main theorems; the methodology reviewer reproduced the scheduled-removal identity to 3e-16, Kendall's formula against a master-equation solution, and the headline probability by an independent simulation. The criticisms were:
- rigour of presentation: the time change and conditional construction, measurability in the successful-immigrant argument, compressed localisation and regeneration steps, and broken typesetting;
- framing: the source paper's Observation 3.7 and its remark that no feedback loop occurs without inflow should be engaged directly; the companion Evidence Press release should be cited; classical components should be attributed where used;
- significance: with substrate-keeping kernels compartmentalisation is equivalent to a bulk export transition, so the genuinely compartmental content needed to be isolated; molecule-blind division is not covered;
- presentation: internal-process material, REF references and the draft author line had to go, and the opening needed to explain the mechanism first.

**Revision.** One round, recorded in [REVISION_RESPONSE.md](REVISION_RESPONSE.md): a new LaTeX manuscript; rewritten proofs; six extensions (single-lineage reduction; comparison with well-mixed degradation for both families; monotonicity and continuity at threshold; bounded substrate leakage; enclosure of the example probability).

**Verification.** A re-review and proof audit of the revision (OpenAI Codex, gpt-6-astra) found no counterexample to the phase boundaries but seven repairable defects: the kernel in the general reduction, conditioning on the inhibitor path without event labels, the absorption point and death driver in the time-change lemma, a measurable-version formula, a convention when lambda=0, an invalid individual-level coupling in the leakage proposition, and an unproved rounding argument in the enclosure. All were repaired (the enclosure code was rewritten with exact dyadic steps, decimal exponentials and an explicit error budget on a restricted input domain). Four further targeted audits (same route) checked the repairs and the rounding argument until no open correctness issue remained; see REVISION_RESPONSE.md.

**Remaining limitations.** Bounded priority search; molecule-blind kernels open; no catalytic tail bound; estimator error control only where Delta>0; enclosure rounding argument not machine-checked.
