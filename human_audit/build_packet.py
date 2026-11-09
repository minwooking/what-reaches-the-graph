#!/usr/bin/env python3
"""Build the human-audit packet. AI-generated code: review before use. No LLM calls; read-only on the harness.

Usage: python3 -B build_packet.py [--harness PATH]   (default: ../../access2026/harness relative to this file)
Seed 20261103. QA verdicts (correct / grounded / gc) are recomputed with the study's own deterministic scorer
(study27 s27_score.primary_item) from the stored predictions + private gold; fact-precision verdicts are the stored
cross-family LLM judge outputs (study32 b2_b3).
"""
import argparse, csv, json, os, random, sys
from pathlib import Path

SEED = 20261103
HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--harness", default=str(HERE.parent.parent / "access2026" / "harness"))
args = ap.parse_args()
H = Path(args.harness)
S27 = H / "study27_ours_final"
CHK = H / "study32_reviewer_checks"
sys.dont_write_bytecode = True
sys.path.insert(0, str(S27))
import scorer_2wiki as sc  # noqa: E402
import s27_score as SS  # noqa: E402


def rj(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


gold = {}
for role in ("dev", "test"):
    for g in rj(S27 / "gold_private" / role / ("gold_main_%s.jsonl" % role)):
        gold[g["qid"]] = g
chunks = {}
for p in sorted((S27 / "harness_input").glob("main_shard*.chunks.jsonl")):
    for c in rj(p):
        chunks[c["chunk_id"]] = c

# arm -> (directory of predictions/main, file name)
ARMS = {
    "Ours": (S27 / "predictions" / "main", "Ours.json"),
    "U-ext+seed": (S27 / "post_review" / "run" / "predictions" / "main", "U-extplusseed.json"),
    "L0": (S27 / "predictions" / "main", "L0.json"),
    "iText2KG": (CHK / "b8_external" / "exp" / "run" / "predictions" / "main", "iText2KG.json"),
    "EDC": (CHK / "b12_external2" / "exp" / "run" / "predictions" / "main", "EDC.json"),
}
REPORTED = {"Ours": (.6062, .655), "U-ext+seed": (.6031, .678), "L0": (.3937, .433), "iText2KG": (.430, .549), "EDC": (.445, .629)}

pool = {}
check = {}
for arm, (root, fn) in ARMS.items():
    rows = []
    for f in sorted(root.glob("main*/s*/" + fn)):
        shard, seed = f.parent.parent.name, f.parent.name
        d = json.load(open(f, encoding="utf-8"))
        for qid, p in d["preds"].items():
            g = gold.get(qid)
            if g is None:
                continue
            it = SS.primary_item(g, p["qa"], chunks)
            rows.append(dict(arm=arm, shard=shard, run_seed=seed, qid=qid, qa=p["qa"], g=g, it=it,
                             src=str(f.relative_to(H))))
    pool[arm] = rows
    n = len(rows)
    check[arm] = (n, sum(r["it"]["gc"] for r in rows) / n, sum(r["it"]["correct"] for r in rows) / n)

rng = random.Random(SEED)
sample = []
N_PER_STRATUM = 15
for arm in ARMS:
    rows = sorted(pool[arm], key=lambda r: (r["shard"], r["run_seed"], r["qid"]))
    seen_q = set()
    def take(cands, k):
        cands = [r for r in cands if r["qid"] not in seen_q]
        rng.shuffle(cands)
        out = []
        for r in cands:
            if r["qid"] in seen_q:
                continue
            seen_q.add(r["qid"]); out.append(r)
            if len(out) == k:
                break
        return out
    pos = take([r for r in rows if r["it"]["gc"]], N_PER_STRATUM)
    cg = take([r for r in rows if r["it"]["correct"] and not r["it"]["grounded"]], 5)  # correct but ungrounded
    rest = take([r for r in rows if not r["it"]["gc"]], N_PER_STRATUM - len(cg))
    sample += pos + cg + rest

rng.shuffle(sample)


def fmt_fact(i, f, cited):
    return "%s[%d] %s | %s | %s" % ("*" if cited else " ", i + 1, f[1], f[2], f[3])


def facts_cell(qa):
    ret = qa.get("retrieved", [])
    cited = set(qa.get("support", []))
    lines = [fmt_fact(i, f, (i + 1) in cited) for i, f in enumerate(ret)]
    head = "RETRIEVED %d facts shown to the answerer; '*' = cited by the answerer\n" % len(ret)
    return head + "\n".join(lines) if lines else "(no facts retrieved)"


def ev_cell(g):
    return "\n".join("%s | %s | %s" % (e["s"], e["r"], e["o"]) for e in g["evidences"])


def aliases(g):
    a = list(g.get("answer_aliases", ()) or []) + list(g.get("answer_demonyms", ()) or [])
    return "; ".join(map(str, a))


OUT = HERE
cols = ["item_id", "question", "gold_answer", "model_answer", "cited_facts", "human_correct", "human_grounded", "note",
        "question_type", "gold_evidence", "gold_answer_aliases"]
kcols = ["item_id", "arm", "shard", "run_seed", "qid", "question_type", "judge_correct", "judge_grounded", "judge_gc",
         "n_retrieved", "source_file"]
with open(OUT / "labeling_sheet.csv", "w", newline="", encoding="utf-8-sig") as fs, \
     open(OUT / "judge_key_HIDDEN.csv", "w", newline="", encoding="utf-8") as fk:
    ws, wk = csv.writer(fs), csv.writer(fk)
    ws.writerow(cols); wk.writerow(kcols)
    for i, r in enumerate(sample, 1):
        iid = "Q%03d" % i
        g, qa, it = r["g"], r["qa"], r["it"]
        ws.writerow([iid, g["question"], g["answer"], qa.get("answer", ""), facts_cell(qa), "", "", "",
                     g["type"], ev_cell(g), aliases(g)])
        wk.writerow([iid, r["arm"], r["shard"], r["run_seed"], r["qid"], g["type"], int(it["correct"]), int(it["grounded"]),
                     int(it["gc"]), len(qa.get("retrieved", [])), r["src"]])

# ---- fact precision (stored Gemma judge, pass 1 = registered verdict r1; r2 = reversed-order pass)
FARMS = {"Ours": "Ours.json", "U-ext+seed": "U-extplusseed.json"}
fpool = {a: [] for a in FARMS}
for a, fn in FARMS.items():
    for f in sorted((CHK / "b2_b3" / "run" / "b2").glob("main*/s*/" + fn)):
        d = json.load(open(f, encoding="utf-8"))
        for x in d.get("facts", []):
            if isinstance(x.get("r1"), bool):
                fpool[a].append((f, d["unit"], x))
frng = random.Random(SEED + 1)
fs_sample = []
for a in FARMS:
    for flag in (True, False):
        c = [t for t in fpool[a] if t[2]["r1"] is flag]
        c.sort(key=lambda t: (t[1], json.dumps(t[2]["f"])))
        frng.shuffle(c)
        fs_sample += [(a, t) for t in c[:10]]
frng.shuffle(fs_sample)
with open(OUT / "labeling_sheet_facts.csv", "w", newline="", encoding="utf-8-sig") as fs, \
     open(OUT / "judge_key_facts_HIDDEN.csv", "w", newline="", encoding="utf-8") as fk:
    ws, wk = csv.writer(fs), csv.writer(fk)
    ws.writerow(["item_id", "subject", "property", "object", "source_chunk_title", "source_chunk_text", "human_supported", "note"])
    wk.writerow(["item_id", "arm", "unit", "judge_supported_pass1", "judge_supported_pass2", "chunk_id", "source_file"])
    for i, (a, (f, unit, x)) in enumerate(fs_sample, 1):
        iid = "F%03d" % i
        cid, s, p, o = x["f"][:4]
        c = chunks.get(cid, {})
        ws.writerow([iid, s, p, o, c.get("title", ""), c.get("text", ""), "", ""])
        wk.writerow([iid, a, unit, int(x["r1"]), int(bool(x.get("r2"))), cid, str(f.relative_to(H))])

print("recomputed arm means vs reported (n, gc, correct | reported gc, correct):")
for a, (n, gc, co) in check.items():
    print("  %-11s n=%d gc=%.4f correct=%.4f | %.4f %.3f" % (a, n, gc, co, *REPORTED[a]))
from collections import Counter
print("sample:", len(sample), Counter((r["arm"], int(r["it"]["gc"])) for r in sample))
print("type:", Counter(r["g"]["type"] for r in sample))
print("correct&!grounded:", Counter(r["arm"] for r in sample if r["it"]["correct"] and not r["it"]["grounded"]))
print("retrieved size max/median:", max(len(r["qa"].get("retrieved", [])) for r in sample),
      sorted(len(r["qa"].get("retrieved", [])) for r in sample)[len(sample) // 2])
print("facts sample:", len(fs_sample), Counter((a, int(t[2]["r1"])) for a, t in fs_sample))
