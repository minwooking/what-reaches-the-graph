#!/usr/bin/env python3
"""Make a FAKE filled copy of the v2 sheets for testing compute_agreement_v2.py. AI-GENERATED code. The numbers it produces mean nothing.

Labels = hidden key value with random flips (QA 15% / 10% / 15%, facts 20% where a stored verdict exists, else Bernoulli(.75)).
Usage (from this folder): python3 -B make_fake_v2.py   -> writes FAKE_filled_sheet_v2.csv and FAKE_filled_facts_v2.csv here.
"""
import csv, random
from pathlib import Path

HERE = Path(__file__).resolve().parent
V2 = HERE.parent
rng = random.Random(1)


def rd(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def flip(x, p):
    return 1 - x if rng.random() < p else x


key = {r["item_id"]: r for r in rd(V2 / "judge_key_HIDDEN.csv")}
rows = rd(V2 / "labeling_sheet.csv")
cols = list(rows[0].keys())
for r in rows:
    k = key[r["item_id"]]
    hc = flip(int(k["judge_correct"]), .15)
    hg = flip(int(k["judge_grounded"]), .10)
    r["human_correct"], r["human_grounded"] = str(hc), str(hg)
    if hg == 0:
        r["human_predicate_ok"] = "NA"
    else:
        jp = k["judge_predicate_ok"]
        base = int(jp) if jp in ("0", "1") else rng.randint(0, 1)
        r["human_predicate_ok"] = str(flip(base, .15))
    r["note"] = "fake"
with open(HERE / "FAKE_filled_sheet_v2.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

fkey = {r["item_id"]: r for r in rd(V2 / "facts_key_HIDDEN.csv")}
frows = rd(V2 / "labeling_sheet_facts.csv")
fcols = list(frows[0].keys())
for r in frows:
    k = fkey[r["item_id"]]
    if k["stored_judge_pass1"] != "":
        hs = flip(int(k["stored_judge_pass1"]), .20)
    else:
        hs = 1 if rng.random() < .75 else 0
    r["human_supported"] = str(hs)
    r["note"] = "fake"
with open(HERE / "FAKE_filled_facts_v2.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=fcols)
    w.writeheader()
    w.writerows(frows)
print("wrote FAKE_filled_sheet_v2.csv (%d rows) and FAKE_filled_facts_v2.csv (%d rows)" % (len(rows), len(frows)))
