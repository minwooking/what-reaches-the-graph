#!/usr/bin/env python3
"""Agreement v2 (AI-GENERATED code: review and test before use).

Adds to v1: (1) predicate agreement (human_predicate_ok vs judge_predicate_ok, NA excluded on either side);
(2) per-arm human fact precision with a 95% percentile bootstrap CI over facts (B = 10,000);
(3) judge (Gemma, pass 1) agreement on facts only where a stored verdict exists.
QA correct / grounded / gc tables are computed as in v1. Kappa, bootstrap and row helpers are imported read-only from ../compute_agreement.py.

python3 -B compute_agreement_v2.py --sheet labeling_sheet.csv --key judge_key_HIDDEN.csv \
   --facts-sheet labeling_sheet_facts.csv --facts-key facts_key_HIDDEN.csv --out agreement_v2.md [--B 10000] [--seed 20261107]
"""
import argparse, random, sys
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import compute_agreement as v1  # noqa: E402  (read-only reuse of v1 helpers)


def prec_ci(h, B, rng):
    n = len(h)
    if n == 0:
        return float("nan"), (float("nan"), float("nan"))
    means = []
    for _ in range(B):
        s = 0
        for _ in range(n):
            s += h[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    return sum(h) / n, (means[int(.025 * B)], means[min(B - 1, int(.975 * B))])


HEAD = ["| group | n | raw agreement [95% CI] | Cohen's kappa [95% CI] | pos. rate judge / human | judge FP / FN |",
        "|---|---:|---|---|---|---|"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--key", required=True)
    ap.add_argument("--facts-sheet", required=True)
    ap.add_argument("--facts-key", required=True)
    ap.add_argument("--out", default="agreement_v2.md")
    ap.add_argument("--B", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20261107)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    out = ["# Judge vs human agreement, v2 (AI-generated; review before use)", ""]

    # ---- QA
    key = {r["item_id"]: r for r in v1.read(a.key)}
    sheet = v1.read(a.sheet)
    by = defaultdict(lambda: defaultdict(lambda: ([], [])))
    pred = defaultdict(lambda: ([], []))
    skipped, pred_skipped, na_bad, na_missing = [], 0, 0, 0
    for r in sheet:
        k = key.get(r["item_id"])
        hc, hg = v1.b(r.get("human_correct")), v1.b(r.get("human_grounded"))
        hp = v1.b(r.get("human_predicate_ok"))
        if k is None or hc is None or hg is None:
            skipped.append(r["item_id"])
        else:
            for arm in (k["arm"], "ALL arms"):
                for m, hv, jv in (("correct", hc, int(k["judge_correct"])), ("grounded", hg, int(k["judge_grounded"])),
                                  ("gc (correct AND grounded)", int(hc and hg), int(k["judge_gc"]))):
                    by[m][arm][0].append(hv)
                    by[m][arm][1].append(jv)
        if hg == 0 and (r.get("human_predicate_ok") or "").strip().upper() not in ("", "NA"):
            na_bad += 1  # human gave a predicate value although grounded = 0 (rule says NA)
        if hg == 1 and (r.get("human_predicate_ok") or "").strip() == "":
            na_missing += 1
        jp = None if k is None else v1.b(k.get("judge_predicate_ok"))
        if k is None or hp is None or jp is None:
            pred_skipped += 1
            continue
        for arm in (k["arm"], "ALL arms"):
            pred[arm][0].append(hp)
            pred[arm][1].append(jp)
    out.append("QA items labelled: %d of %d (skipped for QA measures: %d %s). Predicate pairs used: %d; not used (NA on either side or "
               "missing): %d. Human predicate values present while human_grounded = 0: %d. Grounded = 1 but predicate blank: %d."
               % (len(sheet) - len(skipped), len(sheet), len(skipped), skipped[:10],
                  sum(len(v[0]) for k2, v in pred.items() if k2 == "ALL arms"), pred_skipped, na_bad, na_missing))
    for m in ("gc (correct AND grounded)", "correct", "grounded"):
        out += ["", "## QA verdict: " + m, ""] + HEAD
        for arm in sorted(by[m], key=lambda x: (x == "ALL arms", x)):
            out.append(v1.row(arm, *by[m][arm], a.B, rng))
    out += ["", "## Predicate fit: human_predicate_ok vs code (gc_pred-style predicate check)", ""] + HEAD
    for arm in sorted(pred, key=lambda x: (x == "ALL arms", x)):
        out.append(v1.row(arm, *pred[arm], a.B, rng))

    # ---- facts
    fk = {r["item_id"]: r for r in v1.read(a.facts_key)}
    fsheet = v1.read(a.facts_sheet)
    prec = defaultdict(list)
    judged = defaultdict(lambda: ([], []))
    sk, repl = 0, Counter()
    for r in fsheet:
        k = fk.get(r["item_id"])
        hs = v1.b(r.get("human_supported"))
        if k is None or hs is None:
            sk += 1
            continue
        for arm in (k["arm"], "ALL arms"):
            prec[arm].append(hs)
        if k["replaced_from"]:
            repl[k["replaced_from"]] += 1
        if k["stored_judge_pass1"] != "":
            for arm in (k["arm"], "ALL arms"):
                judged[arm][0].append(hs)
                judged[arm][1].append(int(k["stored_judge_pass1"]))
    out += ["", f"## Fact precision: human 'supported' rate per arm (95% percentile bootstrap over facts, B = {a.B})", "",
            "skipped facts: %d; replaced arms: %s" % (sk, dict(repl) or "none"), "",
            "| arm | n facts | human precision [95% CI] |", "|---|---:|---|"]
    for arm in sorted(prec, key=lambda x: (x == "ALL arms", x)):
        p, (lo, hi) = prec_ci(prec[arm], a.B, rng)
        out.append("| %s | %d | %.3f [%.3f, %.3f] |" % (arm, len(prec[arm]), p, lo, hi))
    out += ["", "## Fact judge agreement (Gemma pass 1 vs human), only where a stored verdict exists", ""]
    if judged:
        out += HEAD
        for arm in sorted(judged, key=lambda x: (x == "ALL arms", x)):
            out.append(v1.row(arm, *judged[arm], a.B, rng))
    else:
        out.append("No fact has a stored verdict.")
    out += ["", "Notes: QA and fact samples are not prevalence-matched (QA balanced on judge gc; facts on the sampled set). Predicate "
            "pairs with NA on either side are excluded. Judge FP = judge says 1, human says 0; FN = the reverse."]
    open(a.out, "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
