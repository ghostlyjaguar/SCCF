# Intelligence requirements v0.1.0 (draft)

**Parent:** [Founding Charter v1.0.0](../FOUNDATION.md). These requirements operationalize the charter for future defensive reasoning systems that consume SCCF. They do not amend the charter, redefine the classification unit, or turn the catalog into a SIEM or response platform. The normative machine-readable companion is [intelligence-requirements.json](intelligence-requirements.json). MUST denotes a requirement for an implementation claiming conformance to this specification; no such conformance has yet been demonstrated.

## IR-01 — Objective-centric intelligence

Understanding adversarial activity requires distinguishing what is observed, what strategic function its relationships actually perform, and what objective might explain them. An inferred objective is a hypothesis, not an observation.

- MUST distinguish observations, functional effects, causal relationships, attribution and inferred objectives; give each claim its own evidence and assessment.
- MUST generate candidate strategic compositions and competing explanations, including independent or benign events and insufficient evidence; do not force classification.
- MUST distinguish known class matches from novel candidate compositions; a novel hypothesis is not an accepted catalog entry.

## IR-02 — Probabilistic validation

Events consistent with a composition do not establish that it exists. The system must evaluate competing explanations instead of rewarding agreement or alert volume.

- MUST update hypotheses as supporting, contradictory or missing evidence changes; allow abstention, revision and rejection.
- MUST track evidence provenance and dependencies across sensors, agents and locations; do not count duplicated, derived or correlated observations or model agreement as independent corroboration.
- MUST account for base rates, coverage gaps, multiple testing and asymmetric costs of false positives and false negatives; do not equate concurrency with coordination.
- MUST report numerical probabilities only with a defined target, appropriate calibration evidence, evaluation scope and uncertainty; otherwise report qualitative uncertainty or unknown.
- MUST evaluate discrimination, calibration, abstention, errors and time to defensible assessment on representative held-out data with documented limitations.

Confidence concerns a specified claim (for example, whether a functional relationship exists), not the general severity of an incident. A calibrated probability describes expected frequency under stated conditions; model self-confidence, consensus or a count of alerts is not calibration. If hypotheses are nonexclusive, do not force their probabilities to sum to one. Missing visibility is not evidence of absence unless the relevant detection coverage is justified. Where simultaneous evaluation across many locations increases the chance of false alarms, choose and validate an appropriate multiplicity-aware decision procedure rather than imposing a universal threshold. Retain an audit trail of evidence changes and reassessments.

## IR-03 — Risk-adjusted resource allocation

Confidence in a classification and the value of investigating it are distinct. A lower-probability, high-impact possibility may merit investigation before a higher-probability, low-impact event.

- MUST separate assessment confidence from investigation priority and response authorization.
- MUST prioritize investigative actions using expected defensive value, potential impact, urgency, expected information gain, cost and available capacity; document assumptions and trade-offs.
- MUST reassess priorities as evidence changes, coordinate across monitoring locations and avoid duplicated investigation; preserve baseline monitoring and escalation for high-impact uncertain cases.
- MUST require proportionate, authorized defensive actions; an inferred class or probability is not permission to intervene or to accept a taxonomy entry.

An implementation may use expected loss reduction or value of information as decision criteria, provided it documents estimates, uncertainty, constraints and trade-offs. No numerical loss function or probability threshold is prescribed by SCCF. Review outcomes and update estimates; avoid optimizing solely for alert counts, accuracy, or resource utilization at the expense of defensive harm.

## Decision loop

1. Observe and establish provenance.
2. Generate candidate strategic compositions and alternatives.
3. Evaluate relationships and uncertainty with supporting and opposing evidence.
4. Prioritize authorized investigation based on defensive value.
5. Collect additional evidence; revise assessments and priorities.
6. Where a genuinely distinct composition is suspected, submit a catalog proposal for independent review rather than automatically accepting it.

The loop is an architectural requirement, not a specific model or algorithm.

## Evaluation expectations

Report class- and claim-level precision/recall, false positive and false negative rates, calibration (for example, reliability diagrams and Brier score where applicable), coverage/abstention and time to assessment. Evaluate investigation cost and defensive outcomes separately, against an appropriate baseline, including high-impact missed events. Use representative held-out data, separate related incidents across splits to reduce leakage, document base rates and deployment differences, and disclose uncertainty. System-wide evaluation should account for duplicate evidence and simultaneous tests. These are candidate metrics, not a mandate for a universal threshold or an empirical performance claim.

The following are synthetic conformance scenarios, not real incidents or measured benchmarks:

| ID | Scenario | Required behavior |
|---|---|---|
| IR-C01 | Unrelated malicious activities overlap in time. | Do not assert a coordinated composition without independent evidence of the functional relationship. |
| IR-C02 | Multiple agents report the same underlying observation. | Preserve shared provenance; do not inflate certainty by treating the reports as independent. |
| IR-C03 | Coverage is incomplete and conflicting evidence arrives. | Represent uncertainty and contradictions, revise or abstain; do not manufacture a numeric probability. |
| IR-C04 | A lower-confidence high-impact hypothesis competes with a high-confidence low-impact event. | Do not rank solely by confidence; explain priority using risk, urgency, costs and information value. |
| IR-C05 | New evidence refutes a previously prioritized hypothesis. | Revise the assessment and priority, preserve history and reallocate resources without silently changing the taxonomy. |
| IR-C06 | The system evaluates many locations or candidate classes. | Account for multiplicity and common evidence; evaluate false alarms at the relevant system-wide level. |

## Boundaries

No AI model, statistical method, scoring scale, vendor or programming language is prescribed. Existing SCCF class statuses, acceptance review, ownership and licensing rules remain unchanged. No autonomous acceptance of taxonomy changes or unauthorized intervention. Independent evaluation and real-world validation remain future work.
