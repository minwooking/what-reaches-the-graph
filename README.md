# What Reaches the Graph Decides Held-Out Question Answering in Knowledge Graph Construction

Replication package and manuscript for the paper:
**"What Reaches the Graph Decides Held-Out Question Answering in Knowledge Graph Construction"**

Target Venue: **IEEE Transactions on Knowledge and Data Engineering (TKDE)**

## Overview

This repository contains the complete LaTeX source, figures, references, and human audit protocols for the manuscript.
The paper investigates the mechanisms of competency questions (CQs) and relation vocabulary in knowledge graph construction, showing that relation lists steer single-pass extraction to match complex multi-pass CQ pipelines at a fraction of the computational cost.

## Repository Structure

- `main_tkde.tex`: IEEE TKDE format manuscript (14 pages, `journal,compsoc` format).
- `main.tex`: Original working manuscript format.
- `sections/`: LaTeX section source files (`abstract.tex`, `introduction.tex`, `related.tex`, `pipeline.tex`, `design.tex`, `results.tex`, `discussion.tex`, `conclusion.tex`, `appendix.tex`).
- `figures/`: Vector figures and figure reproduction scripts.
- `references.bib`: Bibliography entries.
- `human_audit/`: Blind multi-rater audit sheets, guidelines, and adjudication scripts.
- `LEDGER.md`: Experimental registry, preregistered hypothesis tests, and B1–B30 robustness evaluation records.

## Building the Manuscript

Prerequisites: TeX Live (with `pdflatex`, `bibtex`, and standard IEEEtran dependencies).

```bash
latexmk -pdf main_tkde.tex
```

The resulting `main_tkde.pdf` strictly conforms to the IEEE TKDE standard 14-page limit.
