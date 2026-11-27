# Strategic Cyberattack Composition Framework (SCCF)

**Status: working draft v0.2.0 — independent research proposal, not an industry standard.**

SCCF classifies the emergent strategic functions of relationships among adversarial activities for defensive threat analysis. The [founding charter](FOUNDATION.md) fixes the project's mission and scope. It complements MITRE ATT&CK and Attack Flow; it does not claim to replace them or establish novelty.

Start with the [founding charter](FOUNDATION.md), [the specification](specification/ontology.md), [the candidate catalog](taxonomy/compositions/SCCF-0001.json), and [contribution rules](CONTRIBUTING.md). AI agents should consult [AGENTS.md](AGENTS.md).

## Validate

Install Python 3.10+ and `jsonschema` (`python -m pip install jsonschema`), then run `python validation/validate.py` from the repository root. Then run `python -m unittest discover -s validation -p 'test_*.py'`. These checks validate structure and synthetic decision-policy examples, not the accuracy of real incidents.

## AI and research feedback

Use the [machine-readable charter](foundation/charter.json) and [composition schema](schemas/composition.schema.json). Submit evidence-backed feedback through [issues](https://github.com/ghostlyjaguar/SCCF/issues) or a pull request. Proposed classes are not accepted by automation. Public visibility does not guarantee AI adoption.

## Research and reuse

The repository is intended for public defensive research. Licensing is pending the maintainer's approval; no open-source license is yet granted. External sources retain their respective rights. Do not submit confidential telemetry, personal information, credentials, operational offensive instructions, or unredacted incident records.

## Research operations and funding

The [research operations pilot](research/README.md) evaluates bounded evidence allocation using reproducible synthetic experiments. See [workflow runs](https://github.com/ghostlyjaguar/SCCF/actions) for reports after activation and [funding policy](FUNDING.md) for voluntary support and financial safeguards. No scientific acceptance or real-world efficacy is inferred from the pilot.

## Related work

- MITRE ATT&CK T1498: https://attack.mitre.org/techniques/T1498/
- MITRE Center for Threat-Informed Defense, Attack Flow: https://ctid.mitre.org/projects/attack-flow/
- Ricks, Thuraisingham and Tague (2018), *Lifting the Smokescreen: Detecting Underlying Anomalies During a DDoS Attack*: https://mews.sv.cmu.edu/papers/isi-18.pdf
