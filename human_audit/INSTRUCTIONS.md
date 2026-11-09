> **AI-generated: review before use.** Check the definitions below against the scorer code and judge prompt cited in section 6 before relying on the audit.

# Human audit of the QA and fact-precision judges (about 2 hours)

Goal: label items independently of the judge, then compare with `compute_agreement.py`. Do **not** open `judge_key_HIDDEN.csv` or `judge_key_facts_HIDDEN.csv` until all labels are filled. Several items share a question across arms; judge each item on its own, do not copy a label from another row.

## 1. What is being audited (read this first)
- `gc` and `correct` in the paper are **not** produced by an LLM judge. The paper says "all QA measures are scored by code against gold" (design section, Metrics). The stored per-question verdicts come from the deterministic scorer `study27_ours_final/s27_score.py` (`primary_item`, `answer_correct`, `answer_present`, `ev_hits`) with alias/demonym matching from `scorer_2wiki.py`. Recomputing it over the stored predictions reproduced every arm mean in the paper (Ours .606/.655, U-ext+seed .603/.678, L0 .394/.433, iText2KG .430/.549, EDC .445/.629 for gc/correct). So the audit asks: does a person agree with the **string-matching scorer**?
- The only per-item **LLM judge** output with a stored verdict is fact precision (Gemma, `study32_reviewer_checks/b2_b3`). That is `labeling_sheet_facts.csv` (section 5).

## 2. QA sheet: `labeling_sheet.csv` (150 items = 5 arms x 30; arm names are hidden)
Columns to fill: `human_correct` (0/1), `human_grounded` (0/1), `note` (optional). Other columns: `question`, `gold_answer`, `gold_answer_aliases`, `model_answer`, `cited_facts` (all facts the answerer saw, numbered; `*` marks the ones it cited), `question_type`, `gold_evidence`.
Model: the answerer got the question and the retrieved facts only, and had to give a short answer or "unknown".

### human_correct = 1 when
The `model_answer` names the same entity / date / place / yes-no as `gold_answer` (or one of `gold_answer_aliases`, including demonyms and obvious spelling or punctuation variants). Scorer definition (`s27_score.answer_correct`):
- empty, "unknown", "none", "n/a", "not available", "no information" -> **0**;
- gold is yes/no -> the first word of the answer must equal it;
- gold is a date -> the same date (use the literal date match; a different day/year is 0);
- otherwise the answer must match the gold entity or an alias/demonym (primary matcher).
Correctness is judged against the gold answer only. It does **not** depend on the facts, and a correct answer that is not supported by the facts is still `human_correct = 1`.

### human_grounded = 1 when
Quoted from the scorer docstring (`s27_score.primary_item`, MAIN_AMENDMENTS 5): "choice-type questions (comparison, bridge_comparison; answer in the question or yes/no) are grounded only if ALL gold evidence triples are in the retrieved set; open-answer questions (compositional, inference) need the answer string in a retrieved triple. Primary = correct AND grounded." The paper (Metrics, grounded QA) says the same: "For comparison questions every gold evidence triple must be among the retrieved facts, and for open questions the answer string must appear in a retrieved fact."
How to apply it to the sheet:
- `question_type` = `compositional` or `inference` (open): 1 if the **gold answer** (or an alias/demonym) appears as the subject or object of at least one retrieved fact in `cited_facts` (any of the listed facts, cited or not). Note this tests the gold answer string, not the model answer.
- `question_type` = `comparison` or `bridge_comparison` (choice): 1 only if **every** line of `gold_evidence` is represented in the retrieved facts, meaning a fact links the same two entities (subject and object, either direction, any specific predicate; vague predicates such as "related to" do not count). One missing evidence line -> 0.
- Predicate wording does not matter for the scorer; judge entity pairs, not relation names. If an entity is clearly the same under an alias, count it.
- `human_grounded` is independent of the model answer; fill it even when the answer is wrong.
- Then `gc` = correct AND grounded; the script derives it.

Write 1/0 only. If an item is genuinely unclear, choose the better guess and put "unclear" in `note` (these will be reviewed, not dropped).

## 3. Suggested pace
About 40 seconds per QA item (about 100 minutes) plus about 15 minutes for the 40 fact items. Split the sheet between two people for a double-labelled subset if time allows (copy the sheet, compute agreement for each person separately, and compare the two humans with the same script by using one human sheet as a pseudo key).

## 4. Sampling (for reporting)
Seed 20261103. Stratified by arm (Ours, U-ext+seed, L0, iText2KG, EDC) x judge gc verdict: 15 gc=1 and 15 gc=0 per arm, one item per question within an arm, drawn from the 960 scored (question x run seed) items of each arm. Within gc=0, up to 5 per arm are "correct but not grounded" (`build_packet.py`; actual counts in the key: EDC 8, Ours 8, others 5, because remaining gc=0 draws can also fall in that group). Because the sample is balanced on the judge verdict, agreement and kappa are not prevalence-matched to the full arms; the script reports the positive rates and FP/FN counts so the reader can see this. Order is shuffled; ids Q001..Q150 carry no arm information.

## 5. Fact sheet: `labeling_sheet_facts.csv` (40 items: Ours 20, U-ext+seed 20; half judged supported)
Fill `human_supported` (0/1). Judge definition, quoted from the prompt `s30_prec.p_prec` (system: "You are a strict fact checker for knowledge-graph facts"): "For each fact decide whether it is SUPPORTED by its source chunk text alone: the chunk states it (a paraphrase is fine). Use ONLY the chunk text; do not use any outside knowledge. A fact is NOT supported if the chunk does not state it, contradicts it, or the subject or object is not what the chunk says." Use the `source_chunk_text` column only. The judge verdict compared is pass 1 (the registered precision; pass 2 used reversed order).

## 6. Provenance of the stored verdicts (paths under `paper/access2026/harness/`)
- Ours, L0: `study27_ours_final/predictions/main/main*/s*/{Ours,L0}.json`; U-ext+seed: `study27_ours_final/post_review/run/predictions/main/...U-extplusseed.json`; iText2KG: `study32_reviewer_checks/b8_external/exp/run/predictions/main/...iText2KG.json`; EDC: `study32_reviewer_checks/b12_external2/exp/run/predictions/main/...EDC.json`. Gold: `study27_ours_final/gold_private/{dev,test}`; scorer: `study27_ours_final/s27_score.py`, `scorer_2wiki.py`. Fact verdicts: `study32_reviewer_checks/b2_b3/run/b2/main*/s*/{Ours,U-extplusseed}.json`.
- Rebuild: `python3 -B build_packet.py` (no LLM calls, read-only on the harness).

## 7. After labelling
```
python3 -B compute_agreement.py --sheet labeling_sheet.csv --key judge_key_HIDDEN.csv \
   --facts-sheet labeling_sheet_facts.csv --facts-key judge_key_facts_HIDDEN.csv --out agreement.md
```
Output: per arm and pooled raw agreement and Cohen's kappa for correct, grounded and gc, with 95% percentile bootstrap CIs over items (B = 10,000), plus the judge's FP/FN counts. A kappa CI is not defined when a rater is constant in an arm. `selftest/` holds a fake, randomly perturbed filled copy used only to test the script; its numbers mean nothing.
Review before use: the files were generated by AI; the scorer description in section 2 is a summary, so check disagreements against `s27_score.py` / `scorer_2wiki.py` before calling the judge wrong.
