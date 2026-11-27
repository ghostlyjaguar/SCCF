# Phase 2 — robustness of probabilistic investigation

## Question
Can a resource allocation policy still prioritize evidence about a potential strategic composition when its assumptions are wrong? Simulated positive labels stand for an analyst-review-worthy composition; negative labels stand for independent or otherwise nonqualifying activity. These are abstract outcomes, not simulated attacks, causal graphs, or proof of intent.

## Protocol
Compare fixed order, risk ranking, expected value of two readings (VOI), and the same VOI allocation with source-aware deduplication. Each receives 100 evidence requests (two attempted observation slots each) per 1,000 cases. Missing observations still consume capacity. All policies see the same cases, and allocation uses only prior estimates and missed-case weights. Source identity and readings become visible only after requesting evidence. Deduplication assumes correct source identifiers; it cannot identify unknown dependencies.

The nominal inference model assumes sensitivity 0.8 and false-positive probability 0.15. Stress conditions vary the actual base rate, evidence reliability, missingness, duplication, disagreement, and combined shifts. All numerical settings are illustrative, not empirical estimates. The true label is used only for scoring. Thirty fixed seeds (2000–2029) are distinct from phase 1; they are reproducible evaluation fixtures, not independent empirical held-out data. Do not tune against these and later describe them as unseen. Any further tuning requires newly declared evaluation seeds and conditions.

## Interpretation
Primary metric: weighted decision loss (one unit per false positive, two/five/ten units per missed case). Report false positives, false negatives, Brier score (overall probabilistic accuracy, not pure calibration), and paired seed-level loss differences. Report every scenario and all policies, including failure cases. No policy is accepted on the basis of this experiment. A candidate is descriptively better in a scenario only when total decision loss is lower; any increase in misses or worse results under other scenarios must be disclosed. Seed minima and maxima are not confidence intervals. No universal superiority threshold or real-world acceptance is claimed.

## Limits and next steps
This intentionally tests simple distribution shifts rather than estimating real-world performance. It does not represent multi-hypothesis causality, all forms of evidence dependence, learned probabilities, or actual AI models. Source disagreement is modeled with a weak contradictory second observation, not operational attack methods. Next, preregister externally grounded scenarios and obtain independently annotated, legally reusable defensive evidence with clear distinction between coincidence and supported functional relationships. Use separate development and evaluation data. No change to taxonomy acceptance or foundational principles.

Run: `python3 research/robustness.py`. Results are written to research-results/robustness.json and robustness.md.
