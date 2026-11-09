#!/usr/bin/env python3
"""Build the v2 human-audit packet. AI-GENERATED code: review and test before use.

(a) QA sheet: the 150 v1 items (same item ids, rows copied from ../labeling_sheet.csv) plus a new column
    human_predicate_ok (0/1/NA). Hidden key adds judge_predicate_ok from the study's own predicate check
    (b30_predicate_gc: gc_pred-style rules for choice items, open_pred for open items).
(b) Fact sheet: 200 facts = 40 each from Ours, U-ext+seed, L0+seed, L0, EDC (stored 2Wiki Exp8 graphs, state["facts"]).
    An arm whose facts lack resolvable chunk provenance (>5% unresolved) is replaced by iText2KG and this is reported.

No LLM calls, no network. Read-only on the harness and on the v1 packet; writes only into this folder.
Usage: python3 -B build_packet_v2.py [--harness PATH]   (default: ../../../access2026/harness relative to this folder)
"""
import argparse, csv, json, random, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE.parent
SEED = 20261107
PROV_MIN = 0.95           # arm kept only if >= 95% of its real facts resolve to a stored chunk
PER_ARM = 40
PER_UNIT_CAP = 2
sys.dont_write_bytecode = True

ap = argparse.ArgumentParser()
ap.add_argument("--harness", default=str(V1.parent.parent / "access2026" / "harness"))
H = Path(ap.parse_args().harness)
S27 = H / "study27_ours_final"
CHK = H / "study32_reviewer_checks"
sys.path.insert(0, str(CHK / "b30_predicate_gc" / "code"))
import b30_predicate_gc as P  # noqa: E402  read-only import (b30 -> b20 -> study27 scorer modules)
SS, SC = P.SS, P.sc


def rcsv(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def wcsv(p, cols, rows, bom=True):
    with open(p, "w", newline="", encoding="utf-8-sig" if bom else "utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


# ---------- chunks (same source as v1)
chunks = {}
for p in sorted((S27 / "harness_input").glob("main_shard*.chunks.jsonl")):
    for line in open(p, encoding="utf-8"):
        if line.strip():
            c = json.loads(line)
            chunks[c["chunk_id"]] = c


# ---------- (a) QA predicate check
def pair_only(g, tr):
    """DIAGNOSTIC only: choice items, predicate class + entity pair, WITHOUT the source-chunk-mentions-both-entities condition."""
    for e in g["evidences"]:
        want = SC.REL_CLASS.get(e["r"])
        gs = SC.GoldEntity(e["s"], e.get("s_aliases", ()), e.get("s_demonyms", ()))
        go = SC.GoldEntity(e["o"], e.get("o_aliases", ()), e.get("o_demonyms", ()))
        ok = any((not SC.is_generic_predicate(t["p"]))
                 and ((gs.matches(t["s"]) and go.matches(t["o"])) or (go.matches(t["s"]) and gs.matches(t["o"])))
                 and P.class_ok(SC.pred_class(t["p"], P.B.is_date(t)), want, False) for t in tr)
        if not ok:
            return 0
    return 1


def code_predicate(g, tr, grounded):
    """Code verdict for human_predicate_ok. NA when the code's grounded flag is 0 (same NA rule as the human sheet)."""
    if not grounded:
        return "NA"
    if g["type"] in P.B.OPEN:
        return str(int(P.open_pred(g, tr, False)))
    return str(int(P.choice_gc_class(g, tr, False)))


v1_sheet = rcsv(V1 / "labeling_sheet.csv")
v1_key = {r["item_id"]: r for r in rcsv(V1 / "judge_key_HIDDEN.csv")}
assert len(v1_sheet) == 150 and len(v1_key) == 150, (len(v1_sheet), len(v1_key))
pred_cache = {}


def preds(src):
    if src not in pred_cache:
        pred_cache[src] = json.load(open(H / src, encoding="utf-8"))["preds"]
    return pred_cache[src]


qa_sheet_cols = list(v1_sheet[0].keys())
i_grd = qa_sheet_cols.index("human_grounded")
qa_sheet_cols = qa_sheet_cols[:i_grd + 1] + ["human_predicate_ok"] + qa_sheet_cols[i_grd + 1:]
qa_key_cols = list(next(iter(v1_key.values())).keys()) + ["judge_predicate_ok", "judge_predicate_paironly_diag"]
qa_rows, qa_key_rows = [], []
qmis, qcount, pcount = 0, Counter(), Counter()
for r in v1_sheet:
    k = v1_key[r["item_id"]]
    qid = k["qid"]
    qa = preds(k["source_file"])[qid]["qa"]
    g = P.B.GOLD[qid]
    assert g["question"] == r["question"], r["item_id"]
    it = SS.primary_item(g, qa, chunks)
    if (int(it["correct"]), int(it["grounded"])) != (int(k["judge_correct"]), int(k["judge_grounded"])):
        qmis += 1  # recomputed scorer verdict must equal the v1 key
    tr = SS.as_triples(qa.get("retrieved", []))
    pv = code_predicate(g, tr, it["grounded"])
    pa = str(pair_only(g, tr)) if (it["grounded"] and g["type"] not in P.B.OPEN) else ("NA" if not it["grounded"] else "")
    pcount[(g["type"], pv)] += 1
    qa_rows.append({**r, "human_predicate_ok": ""})
    qa_key_rows.append({**k, "judge_predicate_ok": pv, "judge_predicate_paironly_diag": pa})
wcsv(HERE / "labeling_sheet.csv", qa_sheet_cols, qa_rows)
wcsv(HERE / "judge_key_HIDDEN.csv", qa_key_cols, qa_key_rows, bom=False)


# ---------- (b) fact sheet
ARMS = [  # (arm, state root, state file name)
    ("Ours", S27 / "states" / "main", "Ours.json"),
    ("U-ext+seed", S27 / "post_review" / "run" / "states" / "main", "U-extplusseed.json"),
    ("L0+seed", S27 / "states" / "main", "L0plusseed.json"),
    ("L0", S27 / "states" / "main", "L0.json"),
    ("EDC", CHK / "b12_external2" / "exp" / "run" / "states" / "main", "EDC.json"),
]
REPL = ("iText2KG", CHK / "b8_external" / "exp" / "run" / "states" / "main", "iText2KG.json")
VERDICT = {"Ours": ("Ours.json", CHK / "b2_b3" / "run" / "b2"),
           "U-ext+seed": ("U-extplusseed.json", CHK / "b2_b3" / "run" / "b2")}


def arm_pool(arm, root, fn):
    pool, n_real, n_prov, n_units = [], 0, 0, 0
    files = sorted(root.glob("main*/s*/" + fn))
    for f in files:
        st = json.load(open(f, encoding="utf-8"))
        unit = st["unit"]
        n_units += 1
        for x in st["state"]["facts"]:
            if x[2] == "__alias__":
                continue
            n_real += 1
            if x[0] in chunks:
                n_prov += 1
            pool.append((unit, tuple(x[:4]), str(f.relative_to(H))))
    return pool, {"arm": arm, "files": len(files), "units": n_units, "real_facts": n_real,
                  "prov_share": round(n_prov / n_real, 4) if n_real else 0.0}


arm_log, chosen = [], []
for arm, root, fn in ARMS:
    pool, info = arm_pool(arm, root, fn)
    replaced_from = ""
    if info["real_facts"] == 0 or info["prov_share"] < PROV_MIN:
        arm_log.append(f"{arm}: provenance share {info['prov_share']} < {PROV_MIN} -> replaced by {REPL[0]}")
        replaced_from = arm
        arm, root, fn = REPL
        pool, info = arm_pool(arm, root, fn)
        assert info["real_facts"] and info["prov_share"] >= PROV_MIN, "replacement arm also lacks provenance"
    chosen.append((arm, replaced_from, pool, info))

rng = random.Random(SEED)
sample = []
for arm, replaced_from, pool, info in chosen:
    uniq = sorted(set(pool))
    rng.shuffle(uniq)
    per_unit, pick = Counter(), []
    for unit, f, src in uniq:
        if per_unit[unit] >= PER_UNIT_CAP:
            continue
        pick.append((arm, replaced_from, unit, f, src))
        per_unit[unit] += 1
        if len(pick) == PER_ARM:
            break
    assert len(pick) == PER_ARM, (arm, len(pick))
    sample += pick

# stored Gemma verdicts (b2_b3), only where the same unit and fact tuple were judged
vcache = {}


def stored(arm, unit, f):
    if arm not in VERDICT:
        return None
    fn, root = VERDICT[arm]
    path = root.joinpath(*unit.split("/"), fn)
    if str(path) not in vcache:
        vcache[str(path)] = json.load(open(path, encoding="utf-8")) if path.exists() else None
    d = vcache[str(path)]
    if d is None:
        return None
    for x in d.get("facts", []):
        if tuple(x["f"][:4]) == f and isinstance(x.get("r1"), bool):
            return x["r1"], (x.get("r2") if isinstance(x.get("r2"), bool) else None), str(path.relative_to(H))
    return None


rng2 = random.Random(SEED)
rng2.shuffle(sample)
fact_cols = ["item_id", "subject", "property", "object", "source_chunk_title", "source_chunk_text", "human_supported", "note"]
key_cols = ["item_id", "arm", "unit", "chunk_id", "state_file", "replaced_from", "stored_judge_pass1", "stored_judge_pass2",
            "stored_verdict_file"]
fact_rows, fact_key = [], []
for i, (arm, rep, unit, f, src) in enumerate(sample, 1):
    iid = "F%03d" % i
    c = chunks[f[0]]
    fact_rows.append({"item_id": iid, "subject": f[1], "property": f[2], "object": f[3], "source_chunk_title": c["title"],
                      "source_chunk_text": c["text"], "human_supported": "", "note": ""})
    sv = stored(arm, unit, f)
    fact_key.append({"item_id": iid, "arm": arm, "unit": unit, "chunk_id": f[0], "state_file": src,
                     "replaced_from": rep,
                     "stored_judge_pass1": "" if sv is None else int(sv[0]),
                     "stored_judge_pass2": "" if sv is None or sv[1] is None else int(sv[1]),
                     "stored_verdict_file": "" if sv is None else sv[2]})
wcsv(HERE / "labeling_sheet_facts.csv", fact_cols, fact_rows)
wcsv(HERE / "facts_key_HIDDEN.csv", key_cols, fact_key, bom=False)

# ---------- report
print("QA: %d items; recomputed (correct, grounded) differs from v1 key on %d items" % (len(qa_rows), qmis))
print("QA code predicate verdicts (type, verdict):", sorted(pcount.items(), key=lambda t: (t[0][0], t[0][1])))
for arm, rep, pool, info in chosen:
    print("ARM %-11s replaced_from=%-4s units=%d files=%d real_facts=%d prov_share=%s" % (
        arm, rep or "-", info["units"], info["files"], info["real_facts"], info["prov_share"]))
for line in arm_log:
    print("NOTE " + line)
print("facts sheet rows:", len(fact_rows), "per arm:", Counter(k["arm"] for k in fact_key),
      "with stored verdict:", sum(1 for k in fact_key if k["stored_judge_pass1"] != ""))
