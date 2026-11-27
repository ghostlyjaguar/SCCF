"""Synthetic defensive decision-allocation experiment; not an attack detector."""
import argparse
import json
import random
from pathlib import Path

def posterior(p, positive, sensitivity, false_positive):
    a, b = (sensitivity, false_positive) if positive else (1-sensitivity, 1-false_positive)
    return p*a/(p*a+(1-p)*b)

def loss(p, impact, fp_cost=1):
    return min(p*impact, (1-p)*fp_cost)

def value(p, impact, sensitivity=.8, false_positive=.15):
    q = p*sensitivity+(1-p)*false_positive
    return max(0, loss(p, impact)-q*loss(posterior(p, True, sensitivity, false_positive), impact)
               -(1-q)*loss(posterior(p, False, sensitivity, false_positive), impact))

def scenario(seed, n=1000):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        p = rng.choice([.01, .05, .15, .35])
        impact = rng.choice([2, 5, 10])
        truth = rng.random() < p
        # One independent, simulated additional observation per case.
        evidence = rng.random() < (.8 if truth else .15)
        rows.append((p, impact, truth, evidence))
    return rows

def evaluate(rows, budget, policy):
    if policy == "risk":
        key = lambda r: r[0]*r[1]
    elif policy == "voi":
        key = lambda r: value(r[0], r[1])
    elif policy == "fixed":
        key = lambda r: 0
    else:
        raise ValueError("unknown policy")
    chosen = set(sorted(range(len(rows)), key=lambda i: key(rows[i]), reverse=True)[:budget])
    fp = fn = tp = tn = 0
    brier = realized_loss = 0.0
    for i, (p, impact, truth, evidence) in enumerate(rows):
        if i in chosen:
            p = posterior(p, evidence, .8, .15)
        # A positive decision means escalate for review, not automatic intervention.
        escalate = p*impact > 1-p
        fp += int(escalate and not truth)
        fn += int(not escalate and truth)
        tp += int(escalate and truth)
        tn += int(not escalate and not truth)
        brier += (p-int(truth))**2
        realized_loss += int(escalate and not truth)+impact*int(not escalate and truth)
    return {"fp":fp,"fn":fn,"tp":tp,"tn":tn,"brier_sum":brier,
            "decision_loss":realized_loss,"observations_purchased":len(chosen),"cases":len(rows)}

def run(seeds=range(100,120), budget=100, n=1000):
    output = {}
    for policy in ("fixed","risk","voi"):
        totals = {}
        for seed in seeds:
            for k,v in evaluate(scenario(seed,n),budget,policy).items():
                totals[k] = totals.get(k,0)+v
        totals["brier"] = totals.pop("brier_sum")/totals["cases"]
        totals["false_positive_rate"] = totals["fp"]/(totals["fp"]+totals["tn"])
        totals["false_negative_rate"] = totals["fn"]/(totals["fn"]+totals["tp"])
        output[policy] = totals
    return {"scope":"synthetic; known generative probabilities; no real-world efficacy claim",
            "seeds":list(seeds),"budget_per_seed":budget,"results":output}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",default="research-results")
    args=parser.parse_args()
    result=run()
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    (out/"metrics.json").write_text(json.dumps(result,indent=2)+"\n")
    lines=["# SCCF synthetic research report","",result["scope"],"",
           "| Policy | Cases | Evidence budget used | False positives | False negatives | Decision loss | Brier score |",
           "|---|---:|---:|---:|---:|---:|---:|"]
    for name,m in result["results"].items():
        lines.append(f"| {name} | {m['cases']} | {m['observations_purchased']} | {m['fp']} | {m['fn']} | {m['decision_loss']:.1f} | {m['brier']:.4f} |")
    lines += ["","Repeated fixed-seed runs are reproducibility checks, not new scientific findings.",
              "No LLMs, live telemetry, paid APIs or automatic interventions were used."]
    (out/"report.md").write_text("\n".join(lines)+"\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
