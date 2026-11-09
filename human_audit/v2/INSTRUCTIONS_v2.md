> **AI-generated: review before use.** The definitions below are quoted from the code named in each section. Check them against that code before relying on the audit.

# Human audit v2: QA scorer incl. predicate fit, and fact precision on 200 facts over five arms (about 3 h 15 min)

Goal: label items independently of the judges, then run `compute_agreement_v2.py`. Do **not** open `judge_key_HIDDEN.csv` or `facts_key_HIDDEN.csv` until all labels are filled. Items that share a question across arms are judged on their own; do not copy a label from another row. v1 (`../INSTRUCTIONS.md`) is unchanged; v2 reuses its 150 QA items with the same ids.

## 1. What is audited
- **QA (150 items, same as v1)**: whether a person agrees with the deterministic string scorer on correctness and grounding (`gc`, `correct`, `grounded`), and, new in v2, whether a person agrees with the **predicate-fit** check. Predicate fit asks whether the retrieved facts state the gold relation, not only the right entities.
- **Facts (200 items, new in v2)**: whether a person agrees that a knowledge-graph fact is stated by its own source chunk. This gives a human precision per arm, including arms that v1 never measured (L0+seed, L0, EDC).

## 2. QA sheet: `labeling_sheet.csv` (150 items)
Columns to fill: `human_correct` (0/1), `human_grounded` (0/1), `human_predicate_ok` (0/1/NA), `note` (optional). Other columns: `question`, `gold_answer`, `gold_answer_aliases`, `model_answer`, `cited_facts` (all facts the answerer saw, numbered; `*` marks the ones it cited), `question_type`, `gold_evidence`.

### human_correct and human_grounded
Unchanged from v1 (see `../INSTRUCTIONS.md` section 2). Quoted from `study27_ours_final/s27_score.py` and `scorer_2wiki.py`: `answer_correct` returns 0 for empty, "unknown", "none", "n/a", "not available" or "no information"; yes/no gold needs the first word to match; a date gold needs the same literal date; otherwise the answer matches the gold entity or an alias/demonym. `primary_item` (MAIN_AMENDMENTS 5): choice-type questions (comparison, bridge_comparison) are grounded only if ALL gold evidence triples are in the retrieved set; open-answer questions (compositional, inference) need the answer string in a retrieved triple. Primary = correct AND grounded.

### human_predicate_ok (new)
Write 1 or 0, or NA when `human_grounded` = 0 (then leave it NA even if you think the predicate is fine).
- **choice-type** (comparison, bridge_comparison): 1 if, for **every** line of `gold_evidence`, at least one retrieved fact (in `cited_facts`) links that entity pair (either direction) with a predicate that expresses the gold relation. Synonyms are fine. Vague predicates such as "related to", "ledTo", "cameoAppearance" for a different relation do not count. One evidence line without such a fact -> 0.
- **open-type** (compositional, inference): 1 if a retrieved fact that holds the gold answer as subject or object has a predicate expressing the relation asked at the **last hop** (the last line of `gold_evidence`). Otherwise 0.
- Judge the predicate wording, not the entities alone (the entities are already checked by `human_grounded`).

The code's version (`b30_predicate_gc.py`, the notion the hidden key uses):
- `choice_gc_class(g, triples, lenient=False)`: "Per gold evidence: indices of triples that hit it (b20 ev_hit_sets rules: non-generic, pair either direction, cited chunk contains the evidence) AND whose pred_class matches REL_CLASS[e.r]". Predicate class = scorer `pred_class(predicate)`, so "expresses the relation" means the same coarse class in the scorer's relation table, not free synonymy.
- `open_pred(g, triples, lenient=False)`: "Some answer-holding triple has pred_class == REL_CLASS[last evidence relation]".
- **Known difference**: the code's choice rule also requires the fact's source chunk to mention both entities (the scorer's evidence-text condition). Your rule does not see the chunk. A disagreement on a choice item can come from that extra condition, not from the predicate. The hidden key therefore also carries `judge_predicate_paironly_diag` (predicate class + entity pair only). Report which of the two diagnostics matches your labels.

## 3. Facts sheet: `labeling_sheet_facts.csv` (200 items, Ours 40, U-ext+seed 40, L0+seed 40, L0 40, EDC 40)
Columns: `subject`, `property`, `object` (the KG fact), `source_chunk_title`, `source_chunk_text` (the chunk the fact cites), `human_supported` (0/1), `note`. The arm, unit and any stored verdict are in `facts_key_HIDDEN.csv` only.

Fill `human_supported` (0/1). Judge definition, quoted from `study32_reviewer_checks/b2_b3/code/s30_prec.py` (`SYS_PREC` and `p_prec`): "You are a strict fact checker for knowledge-graph facts." and "For each fact decide whether it is SUPPORTED by its source chunk text alone: the chunk states it (a paraphrase is fine). Use ONLY the chunk text; do not use any outside knowledge. A fact is NOT supported if the chunk does not state it, contradicts it, or the subject or object is not what the chunk says."

Use `source_chunk_text` only. Do not check the fact against your own knowledge. If the fact's subject or object is in the chunk but the property is not stated, 0.

## 4. Sampling (for reporting)
- **Facts**: seed 20261107. For each arm, the pool is every real fact (the `__alias__` rows excluded) in the 60 main units (30 shards x 2 seeds) of that arm's stored graph (`study27_ours_final/states/main/...`; U-ext+seed from `post_review/run/states/...`; EDC from `study32_reviewer_checks/b12_external2/exp/run/states/...`). The pool is shuffled with a seeded RNG and taken greedily with at most 2 facts per unit, until 40. This is uniform over facts within an arm except for the per-unit cap. Shuffle order is seeded again. IDs F001..F200 carry no arm information.
- **Provenance check**: an arm is kept only if at least 95% of its real facts resolve to a stored chunk. Otherwise the arm is replaced by iText2KG. **In this build all five arms resolved at 100% (no replacement).** The check tests that a chunk exists for the fact, not that the chunk states it; that is what the audit measures.
- **QA**: the 150 items are v1's items unchanged (seed 20261103, stratified; see `../INSTRUCTIONS.md` section 4).

## 5. Stored verdicts (hidden key only)
- `stored_judge_pass1` / `stored_judge_pass2` exist only for facts whose unit and fact tuple were judged in `study32_reviewer_checks/b2_b3/run/b2` (Gemma, Ours and U-ext+seed). **Only 3 of the 200 facts have one** (the b2 judge sampled 40 of about 1,400 facts per unit). The judge-vs-human agreement on facts therefore has n = 3 and is reported as such. It is not a real agreement estimate.
- The QA hidden key `judge_correct`, `judge_grounded`, `judge_gc` are the scorer's values (recomputed and matched to v1 on all 150 items).

## 6. Provenance and rebuild
- Predictions and graphs are read from `paper/access2026/harness/` (read-only). QA rows come from `../labeling_sheet.csv` and `../judge_key_HIDDEN.csv`.
- Rebuild: `python3 -B build_packet_v2.py` (about 12 s; no LLM calls, no network; writes only in this folder). It imports `b30_predicate_gc` read-only for the predicate check. It prints the recomputed-vs-v1 mismatch count (0 for this build).

## 7. Time estimate (not measured)
- QA: about 50 s per item (v1 about 40 s, plus the predicate question) x 150 items = about 125 min.
- Facts: about 20 s per item (the source chunk is read) x 200 items = about 67 min.
- Total: about 3 h 15 min for one labeller. Double-labelling a subset adds time.

## 8. After labelling
```
python3 -B compute_agreement_v2.py --sheet labeling_sheet.csv --key judge_key_HIDDEN.csv \
   --facts-sheet labeling_sheet_facts.csv --facts-key facts_key_HIDDEN.csv --out agreement_v2.md
```
Output: QA correct / grounded / gc (as v1) with 95% bootstrap CIs over items (B = 10,000); predicate-fit agreement and kappa (NA excluded on either side); per-arm human fact precision with 95% bootstrap CIs over facts (B = 10,000); fact judge agreement only where a stored verdict exists. `selftest_v2/` holds a FAKE filled copy and its output (made by `selftest_v2/make_fake_v2.py`). Its numbers mean nothing.

Review before use: these files were generated by AI. Check disagreements against `s27_score.py`, `scorer_2wiki.py`, `b30_predicate_gc.py` and `s30_prec.py` before calling the judge or the code wrong.
