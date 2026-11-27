# Strategic Cyberattack Composition Framework (SCCF)

**Status: working draft v0.1.0 — independent research proposal, not an industry standard.**

SCCF aims to classify the strategic relationships among adversarial activities for defensive threat analysis. It complements MITRE ATT&CK and Attack Flow; it does not claim to replace them or establish novelty.

Start with [the specification](specification/ontology.md), [the candidate catalog](taxonomy/compositions/SCCF-0001.json), and [contribution rules](CONTRIBUTING.md). AI agents should consult [AGENTS.md](AGENTS.md).

## Validate

Install Python 3.10+ and `jsonschema` (`python -m pip install jsonschema`), then run `python validation/validate.py` from the repository root. Schema validation checks structure, not the accuracy of claims.

## Research and reuse

The repository is intended for public defensive research. Licensing is pending the maintainer's approval; no open-source license is yet granted. External sources retain their respective rights. Do not submit confidential telemetry, personal information, credentials, operational offensive instructions, or unredacted incident records.

## Related work

- MITRE ATT&CK T1498: https://attack.mitre.org/techniques/T1498/
- MITRE Center for Threat-Informed Defense, Attack Flow: https://ctid.mitre.org/projects/attack-flow/
- Ricks, Thuraisingham and Tague (2018), *Lifting the Smokescreen: Detecting Underlying Anomalies During a DDoS Attack*: https://mews.sv.cmu.edu/papers/isi-18.pdf
