# Founding charter — v1.0.0

**Mission:** Classify the emergent strategic functions of relationships among cyberattack activities, rather than merely listing their individual technical mechanisms, to enable evidence-based defensive reasoning by humans and AI systems.

The motivating example is SCCF-0001, DDoS as a Smokescreen: the same denial-of-service mechanism can represent a different strategic function depending on its relationship to another malicious activity. Neither concurrency nor an inferred motive alone establishes that relationship.

## Non-negotiable principles

- **F-01:** The primary classification unit is a repeatable strategic composition of at least two distinct adversarial activities; an isolated technique, vulnerability, alert or indicator is not a composition.
- **F-02:** A composition class identifies the functional relationship and emergent strategic property, not merely a sequence, simultaneous events, or a list of techniques.
- **F-03:** Temporal association, functional effect, causal dependency, actor attribution and strategic intent are separate claims. Timing alone never establishes coordination or intent.
- **F-04:** Classify with public evidence, explicit uncertainty, alternative explanations, exclusion criteria and independent review. Novelty is a hypothesis until checked against prior art.
- **F-05:** Provide persistent identifiers, versioned definitions, public machine-readable representations and traceable evidence. Preserve history and distinguish proposed classes from accepted classes.
- **F-06:** Enable humans and AI to read, challenge and propose revisions; no autonomous acceptance or governance changes. The repository owner retains final authority.
- **F-07:** Remain a defensive classification knowledge base complementing existing standards. Detection engines, websites, APIs and integrations are subordinate to the taxonomy; no offensive operational guidance.

## Change control

No ordinary change may alter this charter or foundational invariants. A separate public amendment proposal, explicit repository-owner approval and documented rationale are required. Preserve all prior versions; no AI agent may approve an amendment.

The canonical machine-readable charter is [foundation/charter.json](foundation/charter.json). Review every proposed change against all seven principles. A new class, relation type, data format or integration may evolve without changing the mission, provided it meets these principles. A change that only catalogs techniques, lists stages or aggregates alerts is outside scope.

**Enforcement limit:** A Git repository is not immutable. Technical enforcement depends on repository-owner rulesets, required checks and review. No check establishes scientific truth or prevents an administrator from intentionally altering the project. Archive charter versions and record amendments in the changelog.
