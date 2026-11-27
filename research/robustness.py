"""Phase 2: stress-test defensive review decisions, not attack detection."""
import argparse
import json
import random
from itertools import product
from pathlib import Path
from statistics import mean
from benchmark import posterior, loss

# (true prior odds multiplier, sensitivity, false-positive rate,
# missing probability, duplicate probability, second-source conflict)
SCENARIOS = {
    "nominal": (1, .8, .15, 0, 0, False),
    "rarer_compositions": (.2, .8, .15, 0, 0, False),
    "more_compositions": (3, .8, .15, 0, 0, False),
    "weak_evidence": (1, .6, .35, 0, 0, False),
    "missing_evidence": (1, .8, .15, .55, 0, False),
    "duplicate_evidence": (1, .8, .15, 0, .85, False),
    "conflicting_sources": (1, .8, .15, 0, 0, True),
    "combined_shift": (.3, .6, .35, .3, .6, True),
}
POLICIES = ("fixed", "risk", "voi", "voi_deduplicated")
SEEDS = tuple(range(2000, 2030))

def shift(p, multiplier):
    return p*multiplier/(1-p+p*multiplier)

def generate(seed, scenario, n=1000):
    rng = random.Random(seed)
    drift, sens, fpr, missing, dup, conflict = SCENARIOS[scenario]
    public, hidden = [], []
    for _ in range(n):
        p = rng.choice([.01, .05, .15, .35])
        impact = rng.choice([2, 5, 10])
        truth = rng.random() < shift(p, drift)
        first = rng.random() < (sens if truth else fpr)
        duplicate = rng.random() < dup
        second = first if duplicate else rng.random() < (
            (.4 if truth else .6) if conflict else (sens if truth else fpr))
        observations = (
            (None if rng.random() < missing else first, "A"),
            (None if rng.random() < missing else second, "A" if duplicate else "B"),
        )
        public.append((p, impact))
        hidden.append((truth, observations))
    return public, hidden

def update(p, observations, deduplicate=False):
    seen = set()
    for reading, source in observations:
        if reading is None or (deduplicate and source in seen):
            continue
        p = posterior(p, reading, .8, .15)
        seen.add(source)
    return p

def two_reading_value(p, impact):
    expected = 0.0
    for a, b in product((False, True), repeat=2):
        positive_count = int(a)+int(b)
        mass = p*.8**positive_count*.2**(2-positive_count)
        mass += (1-p)*.15**positive_count*.85**(2-positive_count)
        q = update(p, ((a, "A"), (b, "B")))
        expected += mass*loss(q, impact)
    return max(0.0, loss(p, impact)-expected)

def select(public, budget, policy):
    if not 0 <= budget <= len(public):
        raise ValueError("invalid case budget")
    if policy not in POLICIES:
        raise ValueError("unknown policy")
    def priority(i):
        p, impact = public[i]
        if policy == "fixed":
            return 0
        if policy == "risk":
            return p*impact
        return two_reading_value(p, impact)
    return set(sorted(range(len(public)), key=priority, reverse=True)[:budget])

def evaluate(public, hidden, budget, policy):
    # Allocation receives neither hidden truth, source IDs nor readings.
    selected = select(public, budget, policy)
    result = dict(fp=0, fn=0, tp=0, tn=0, decision_loss=0, brier_sum=0.,
                  attempted_slots=2*len(selected), available_slots=0, cases=len(public))
    for i, ((p, impact), (truth, evidence)) in enumerate(zip(public, hidden)):
        if i in selected:
            result["available_slots"] += sum(x is not None for x, _ in evidence)
            p = update(p, evidence, policy == "voi_deduplicated")
        escalate = p*impact > 1-p
        result["tp" if truth and escalate else "fn" if truth else "fp" if escalate else "tn"] += 1
        result["decision_loss"] += int(escalate and not truth)+impact*int(not escalate and truth)
        result["brier_sum"] += (p-int(truth))**2
    return result

def run(seeds=SEEDS, n=1000, budget=100):
    seeds = tuple(seeds)
    all_results = {}
    for name in SCENARIOS:
        per_policy = {p: [] for p in POLICIES}
        for seed in seeds:
            public, hidden = generate(seed, name, n)
            for policy in POLICIES:
                per_policy[policy].append(evaluate(public, hidden, budget, policy))
        summary = {}
        for policy, rows in per_policy.items():
            totals = {k: sum(r[k] for r in rows) for k in rows[0]}
            totals["brier"] = totals.pop("brier_sum")/totals["cases"]
            positives = totals["tp"]+totals["fn"]
            negatives = totals["tn"]+totals["fp"]
            totals["false_negative_rate"] = totals["fn"]/positives if positives else None
            totals["false_positive_rate"] = totals["fp"]/negatives if negatives else None
            deltas = [a["decision_loss"]-b["decision_loss"]
                      for a,b in zip(rows, per_policy["fixed"])]
            totals["paired_loss_delta_vs_fixed"] = {
                "mean":mean(deltas), "min":min(deltas), "max":max(deltas),
                "seeds_better":sum(d<0 for d in deltas),
                "seeds_worse":sum(d>0 for d in deltas)}
            summary[policy] = totals
        all_results[name] = summary
    return {"scope":"synthetic sensitivity analysis, no actual incident or model evaluation",
            "seeds":list(seeds), "n_per_seed":n, "case_budget":budget,
            "scenario_parameters":SCENARIOS, "results":all_results}

def report(result):
    lines = ["# SCCF phase 2 robustness report", "", result["scope"], "",
             "| Scenario | Policy | FP | FN | Weighted loss | Brier | Seeds better / worse vs fixed |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for name, policies in result["results"].items():
        for policy, m in policies.items():
            d = m["paired_loss_delta_vs_fixed"]
            lines.append(f"| {name} | {policy} | {m['fp']} | {m['fn']} | {m['decision_loss']} | {m['brier']:.4f} | {d['seeds_better']} / {d['seeds_worse']} |")
    lines += ["", "Lower loss and Brier are better; false positives and missed cases can trade off.",
              "The same generated cases and attempted evidence budgets are used for each policy.",
              "Seed ranges are descriptive variation, not confidence intervals. Negative results are retained.",
              "No causal discovery, live telemetry, actual AI evaluation or automatic intervention."]
    return "\n".join(lines)+"\n"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="research-results")
    args = parser.parse_args()
    result = run()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out/"robustness.json").write_text(json.dumps(result, indent=2)+"\n")
    (out/"robustness.md").write_text(report(result))
    print(report(result))

if __name__ == "__main__":
    main()
