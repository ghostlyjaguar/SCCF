# Research operations — phase 1

This is a subordinate experimental layer under F-01 through F-07, not a new charter or automated taxonomy acceptance mechanism.

## First experiment
Compare equal-budget fixed ordering, expected-risk ordering and expected value of information (VOI) for deciding which hypothetical composition candidates warrant further evidence collection. Each simulated location has a prior, a missed-threat cost, a hidden label, and one potential independent observation. Allocation never sees the hidden label or observation before choosing. A positive verdict means review, not intervention. The false-positive cost is one unit; the missed-threat cost varies. The simulator assumes known, calibrated priors and likelihoods: that optimistic assumption is deliberately disclosed. It does not model real DDoS data, causal discovery, correlated evidence, unknown priors, adversarial evasion, or actual LLM performance.

Run `python3 -m unittest discover -s research -p 'test_*.py' -v` and `python3 research/benchmark.py` from the repository root. Results report errors, Brier score, decision loss and evidence count. Twenty fixed seeds support reproducibility only; no statistical significance or generalized benefit is asserted. Next: independent datasets, misspecified likelihoods, dependence, base-rate drift, uncertainty intervals, held-out model evaluations, and preregistered acceptance criteria.

## Phase 2 — robustness testing
See the [robustness protocol](ROBUSTNESS.md) for stress tests under inaccurate priors, missing, duplicate and conflicting evidence. The original phase 1 baseline remains unchanged.

## Mobile operations
The proposed workflow runs weekly on the default branch after merge, manually on demand, and on relevant pull requests. Review the Actions job summary from GitHub Mobile or a browser; artifacts expire after 30 days. Failure requires investigation, not an automatic fix or acceptance. Scheduled runs can stop after inactivity. The workflow uses synthetic data and standard GitHub-hosted runners. It requires no external APIs, secrets, production telemetry, automated commits or live scans. The workflow is bounded to five minutes and one concurrent run per ref.

## Research roadmap
1. Establish repeatable synthetic baseline and independent review.
2. Add public, legally reusable defensive datasets with documented provenance and leakage checks.
3. Evaluate model-specific performance with explicit budgets, independent scoring, negative results and no secret data.
4. Evaluate generalizability, reproducibility and practical defensive utility.
5. Propose improvements through reviewable PRs; retain owner control of publishing and taxonomy acceptance.

Do not present recurring reruns as new discoveries. Do not claim empirical effectiveness without evidence.
