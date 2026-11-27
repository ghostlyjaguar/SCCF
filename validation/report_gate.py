"""Validate structured reporting claims against separately acquired evidence.

Evidence must be supplied by a trusted reader of authoritative records.
This module does not authenticate evidence or evaluate free-form AI prose.
"""
import argparse
import json
import math
from pathlib import Path

def numeric(value):
    return type(value) in (int, float) and math.isfinite(value)

def check_claim(claim, evidence):
    """Return rejection reasons; missing or inconsistent evidence fails closed."""
    if not isinstance(claim, dict) or not isinstance(evidence, dict):
        return ["invalid claim or evidence"]
    ref = claim.get("revision")
    if not isinstance(ref, str) or not ref or ref != evidence.get("revision"):
        return ["missing or mismatched revision"]
    kind = claim.get("kind")
    if kind == "committed":
        path = claim.get("path")
        files = evidence.get("files")
        if (not isinstance(path, str) or not path or not isinstance(files, dict)
                or not isinstance(claim.get("blob"), str) or not claim["blob"]
                or files.get(path) != claim["blob"]):
            return ["file or blob not verified"]
        return []
    if kind == "merged":
        pr = evidence.get("pull_request")
        if (not isinstance(pr, dict) or pr.get("head_revision") != ref
                or type(claim.get("number")) is not int
                or claim["number"] != pr.get("number") or pr.get("merged") is not True):
            return ["merge not verified"]
        return []
    if kind not in ("test_passed", "metric"):
        return ["unsupported claim type"]
    runs = evidence.get("runs")
    run_id = claim.get("run_id")
    if not isinstance(runs, dict) or not isinstance(run_id, str) or not run_id:
        return ["missing run evidence"]
    run = runs.get(run_id)
    if (not isinstance(run, dict) or run.get("revision") != ref
            or run.get("status") != "completed" or run.get("conclusion") != "success"
            or run.get("output_inspected") is not True):
        return ["successful completed run with inspected output not verified"]
    if kind == "metric":
        metrics = run.get("metrics")
        name = claim.get("name")
        if not isinstance(metrics, dict) or not isinstance(name, str):
            return ["missing metric evidence"]
        actual = metrics.get(name)
        if (not isinstance(actual, dict) or not numeric(actual.get("value"))
                or not numeric(claim.get("value")) or claim["value"] != actual["value"]
                or not isinstance(claim.get("unit"), str) or not claim["unit"]
                or claim["unit"] != actual.get("unit")):
            return ["metric value or unit not verified"]
    return []

def assess(claim, evidence):
    reasons = check_claim(claim, evidence)
    notes = evidence.get("warnings", []) if isinstance(evidence, dict) else []
    if not isinstance(notes, list) or not all(isinstance(x, str) for x in notes):
        reasons.append("invalid warnings record")
        notes = []
    return {"accepted": not reasons, "reasons": reasons, "warnings": notes}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("claim", type=Path)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    try:
        result = assess(json.loads(args.claim.read_text()), json.loads(args.evidence.read_text()))
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        result = {"accepted": False, "reasons": [str(exc)], "warnings": []}
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["accepted"] else 1)

if __name__ == "__main__":
    main()
