# SCCF specification v0.1.0 (draft)

## Unit of classification
A strategic composition class describes a repeatable functional relationship among two or more adversarial activities. A class is separate from an incident instance, an individual technique, and an inferred attacker objective.

Represent activities as nodes, functional relationships as directed edges, and temporal relationships independently. A temporal overlap is not sufficient to establish a functional relationship, causal dependency, common actor, or intent.

Initial relationship vocabulary: `diverts` (redirects defensive attention), `conceals` (reduces visibility of another activity), `enables` (establishes a prerequisite), `suppresses` (reduces defensive effectiveness), `amplifies` (increases impact), `deceives` (induces incorrect interpretation). These are provisional, nonexclusive labels; their separability and coverage must be tested.

## Inclusion criteria
A candidate class must specify a definition, constituent roles, functional relation, temporal constraints where applicable, evidence requirements, exclusion criteria, references and defensive significance. Prefer established terminology; new names require a documented distinction from prior art. Do not assume all classes are disjoint.

## Evidence and lifecycle
Class status: `proposed`, `reviewed`, `accepted`, `deprecated`. Accepted means accepted by this project's governance process, not an external standard. Keep class maturity separate from incident assessment. For an incident, report `insufficient_evidence`, `hypothesis`, `supported` or `contradicted`; record supporting and counterevidence, source quality and unresolved alternatives. Never infer intent or actor linkage solely from concurrency. Do not invent numerical confidence scores. Require documented independent review and a counterexample before acceptance. Preserve identifiers and track revisions; never silently reuse IDs.

## Interoperability
Map constituent activities to ATT&CK where supported, without equating a strategic class with an ATT&CK technique. Evaluate Attack Flow and STIX interoperability in a future version; this draft is not a STIX extension.
