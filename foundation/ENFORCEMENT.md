# Owner-only enforcement checklist

The founding charter is anchored at commit 1d47df7b1a8188b23b9e9c2fbc3111e3804e3874. The SCCF validation workflow rejects ordinary changes to either charter file relative to that baseline, and checks the founding ID still exists. A legitimate charter amendment requires an explicitly approved new baseline. Do not bypass a failing baseline check as part of a routine change.

## GitHub settings (repository owner)

Configure a branch ruleset targeting main, with enforcement active. Block force pushes and deletion, require pull requests, and require the SCCF validation / foundation status check after its first successful run. Configure review requirements appropriate to the number of independent maintainers: do not require the sole owner to approve their own PR, because GitHub disallows self-approval. Once a second trusted human reviewer is available, require an independent approval and code-owner review where applicable. Keep bypass privileges restricted and documented. Review ruleset applicability and test with an ordinary PR.

CODEOWNERS and policy files alone do not enable these restrictions. An administrator may still change settings or intentionally approve a charter amendment; no technical mechanism provides absolute immutability. This repository's owner must verify the settings separately.

## Scientific gates

CI validates structure and synthetic examples, not real-world causal claims. Independent review and the owner's acceptance decision are mandatory regardless of CI results. No new class may be accepted automatically.
