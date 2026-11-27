# SCCF specification v0.2.0 (draft)

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

## Structured graph (v0.2)
Every class has at least two distinct role nodes and one directed functional edge. Each edge has source and target role IDs, a relationship from the controlled vocabulary, and an independent temporal relation. Self-loops, missing endpoints, disconnected roles and duplicate directed relationship claims are invalid. The primary relationship must appear in the graph. The roles list is a readable projection of node roles. These graphs describe abstract class definitions, not actual attack instructions or observed incident events.

The strategic_property field states what emerges from the relationship. prior_art records existing work and the limited distinction claimed. review is null for unreviewed candidates; accepted entries require a public review record, a public counterexample and decision rationale. This is a schema requirement, not proof that review occurred.

## Separate incident assessment
Observed events, supported functional relationships, causal claims, attribution and intent must be separately substantiated. The synthetic fixtures in validation/fixtures.json specify expected assessment outcomes using analyst-supplied evidence labels. They do not constitute a detection algorithm, dataset of real attacks, proof of intent or calibrated confidence score. No class becomes accepted through fixture tests. The mission is governed by FOUNDATION.md.

## Intelligence and prioritization boundary
The subordinate [intelligence requirements](intelligence-requirements.md) govern future defensive reasoning implementations. Their claim-level uncertainty and risk-adjusted resource allocation requirements do not change class definitions, acceptance statuses or the founding charter.
