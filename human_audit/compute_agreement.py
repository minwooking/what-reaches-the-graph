#!/usr/bin/env python3
"""Agreement between the automatic judge and a human labeller. AI-generated code: review and test before use.

python3 -B compute_agreement.py --sheet labeling_sheet.csv --key judge_key_HIDDEN.csv [--facts-sheet labeling_sheet_facts.csv
        --facts-key judge_key_facts_HIDDEN.csv] [--out agreement.md] [--B 10000] [--seed 20261103]

Per arm and pooled: raw agreement and Cohen's kappa for correct, grounded and gc (= correct AND grounded), with a
percentile bootstrap 95% CI over items (resampling items within an arm). Kappa is undefined (NaN) when either rater is constant.
The sample is balanced on the judge's gc verdict, so kappa and raw agreement are NOT prevalence-matched to the full 960-item arms;
the report also gives the judge-positive and human-positive rates and the false-positive / false-negative counts of the judge.
"""
import argparse, csv, math, random
from collections import defaultdict


def read(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def b(x):
    x = (x or "").strip().lower()
    return {"1": 1, "0": 0, "yes": 1, "no": 0, "y": 1, "n": 0, "true": 1, "false": 0}.get(x)


def kappa(h, j):
    n = len(h)
    if n == 0:
        return float("nan")
    po = sum(a == c for a, c in zip(h, j)) / n
    ph, pj = sum(h) / n, sum(j) / n
    pe = ph * pj + (1 - ph) * (1 - pj)
    return float("nan") if pe >= 1 else (po - pe) / (1 - pe)


def agree(h, j):
    return sum(a == c for a, c in zip(h, j)) / len(h) if h else float("nan")


def boot(h, j, B, rng):
    n = len(h)
    ks, ag = [], []
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        hh, jj = [h[i] for i in idx], [j[i] for i in idx]
        ag.append(agree(hh, jj))
        k = kappa(hh, jj)
        if not math.isnan(k):
            ks.append(k)
    q = lambda v, p: sorted(v)[min(len(v) - 1, int(p * len(v)))] if v else float("nan")
    return (q(ag, .025), q(ag, .975)), (q(ks, .025), q(ks, .975), len(ks) / B)


def row(label, h, j, B, rng):
    (alo, ahi), (klo, khi, kfrac) = boot(h, j, B, rng)
    fp = sum(1 for a, c in zip(h, j) if c == 1 and a == 0)  # judge positive, human negative
    fn = sum(1 for a, c in zip(h, j) if c == 0 and a == 1)
    k = kappa(h, j)
    f = lambda x: "n/a" if math.isnan(x) else "%.3f" % x
    note = "" if kfrac > .99 else " (kappa CI from %.0f%% of resamples)" % (100 * kfrac)
    return "| %s | %d | %s [%s, %s] | %s [%s, %s]%s | %.2f / %.2f | %d / %d |" % (
        label, len(h), f(agree(h, j)), f(alo), f(ahi), f(k), f(klo), f(khi), note, sum(j) / len(j), sum(h) / len(h), fp, fn)


HEAD = ["| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |",
        "|---|---:|---|---|---|---|"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", required=True); ap.add_argument("--key", required=True)
    ap.add_argument("--facts-sheet"); ap.add_argument("--facts-key")
    ap.add_argument("--out", default="agreement.md")
    ap.add_argument("--B", type=int, default=10000); ap.add_argument("--seed", type=int, default=20261103)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    out = ["# Judge vs human agreement (AI-generated; review before use)", ""]

    key = {r["item_id"]: r for r in read(a.key)}
    sheet = read(a.sheet)
    by = defaultdict(lambda: defaultdict(lambda: ([], [])))  # arm -> measure -> (human, judge)
    skipped = []
    for r in sheet:
        k = key.get(r["item_id"])
        hc, hg = b(r.get("human_correct")), b(r.get("human_grounded"))
        if k is None or hc is None or hg is None:
            skipped.append(r["item_id"]); continue
        for arm in (k["arm"], "ALL arms"):
            for m, hv, jv in (("correct", hc, int(k["judge_correct"])), ("grounded", hg, int(k["judge_grounded"])),
                              ("gc (correct AND grounded)", int(hc and hg), int(k["judge_gc"]))):
                by[m][arm][0].append(hv); by[m][arm][1].append(jv)
    out.append("Items labelled: %d of %d; skipped (missing/invalid label or unknown id): %d %s" % (
        len(sheet) - len(skipped), len(sheet), len(skipped), skipped[:20]))
    for m in ("gc (correct AND grounded)", "correct", "grounded"):
        out += ["", "## QA verdict: " + m, ""] + HEAD
        arms = sorted(by[m], key=lambda x: (x == "ALL arms", x))
        for arm in arms:
            h, j = by[m][arm]
            out.append(row(arm, h, j, a.B, rng))

    if a.facts_sheet and a.facts_key:
        fk = {r["item_id"]: r for r in read(a.facts_key)}
        g = defaultdict(lambda: ([], []))
        sk = 0
        for r in read(a.facts_sheet):
            k = fk.get(r["item_id"]); hs = b(r.get("human_supported"))
            if k is None or hs is None:
                sk += 1; continue
            for arm in (k["arm"], "ALL arms"):
                g[arm][0].append(hs); g[arm][1].append(int(k["judge_supported_pass1"]))
        out += ["", "## Fact precision (Gemma judge, pass 1) vs human 'supported'", "", "skipped: %d" % sk, ""] + HEAD
        for arm in sorted(g, key=lambda x: (x == "ALL arms", x)):
            out.append(row(arm, *g[arm], a.B, rng))
    out += ["", "Notes: sample is balanced on judge gc (QA) or judge verdict (facts); rates above are sample rates, not arm means.",
            "Judge FP = judge says 1, human says 0; FN = judge says 0, human says 1."]
    open(a.out, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
