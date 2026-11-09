"""Figures for cq_dissection from existing results only (no LLM calls). Run: python3 -I make_figs.py"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.abspath(os.path.join(HERE, "..", "..", "access2026", "harness"))
S27 = os.path.join(H, "study27_ours_final", "post_review", "results_postreview.json")
B1 = os.path.join(H, "study32_reviewer_checks", "b1_b4", "b1", "results.json")
B4 = os.path.join(H, "study32_reviewer_checks", "b1_b4", "b4", "results.json")
s27 = json.load(open(S27)); b1 = json.load(open(B1)); b4 = json.load(open(B4))

plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
                     "legend.fontsize": 7, "pdf.fonttype": 42, "font.family": "DejaVu Sans",
                     "axes.linewidth": 0.6})
BLUE, ORANGE, GREEN, VERM, GREY = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#666666"

def round1(x):
    """Round half up to one decimal so printed bounds match the tables (11.25 -> 11.3)."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(x)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

# ---------- Figure A ----------
con = s27["contrasts"]
rows = []  # (group, label, delta_pp, lo, hi, source)
for lab, key in [("L0", "L0+seed − L0"), ("LOOP", "LOOP+seed − LOOP"),
                 ("combined", "Ours − Ours−seed (seed)"), ("U-ext", "U-ext+seed − U-ext (seed effect on U-ext)")]:
    g = con[key]["gc"]
    rows.append(("orig", lab, 100*g["delta"], 100*g["ci95"][0], 100*g["ci95"][1],
                 f"{S27} contrasts['{key}'].gc.{{delta,ci95}}"))
for lab, k in [("L0", "H1"), ("U-ext", "H2")]:
    g = b1["primary"][k]["correct"]
    rows.append(("syn", lab, 100*g["delta"], 100*g["ci95"][0], 100*g["ci95"][1],
                 f"{B1} primary.{k}.correct.{{delta,ci95}}"))
ypos, y = [], 0.0
for i, r in enumerate(rows):
    if i == 4: y += 0.6
    ypos.append(y); y += 1
fig, ax = plt.subplots(figsize=(3.5, 2.6))
ax.axvline(0, color=GREY, lw=0.7, ls="--", zorder=0)
for r, yy in zip(rows, ypos):
    c, m = (BLUE, "o") if r[0] == "orig" else (VERM, "D")
    ax.errorbar(r[2], yy, xerr=[[r[2]-r[3]], [r[4]-r[2]]], fmt=m, color=c, ms=4, lw=1.2, capsize=2, capthick=1)
    ax.text(round1(r[4])+0.6, yy, f"{round1(r[2]):+.1f} [{round1(r[3]):.1f}, {round1(r[4]):.1f}]".replace("-", "−"), va="center", fontsize=6.5)
ax.set_yticks(ypos); ax.set_yticklabels([r[1] for r in rows]); ax.invert_yaxis()
ax.set_xlim(-6, 33)
ax.set_xlabel("Effect of the relation list (points); metrics differ by group", fontsize=6.5)
mid = ypos[3] + 0.3  # r61: divider kept clear of the synonym-seed label
ax.axhline(mid, color="#bbbbbb", lw=0.5)
ax.text(-5.8, ypos[0]-0.55, "original list: grounded QA (descriptive)", fontsize=6.5, color=BLUE, va="bottom")
ax.text(-5.8, ypos[4]-0.55, "synonym list: answer correctness (registered)", fontsize=6.5, color=VERM, va="bottom")
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.tight_layout(pad=0.4)
fig.savefig(os.path.join(HERE, "fig_seed_forest_r62.pdf")); plt.close(fig)

# ---------- Figure B (r61: full-width, legend instead of inline labels, fonts >= 7 pt) ----------
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, NullFormatter
am = s27["arm_means"]
two = [("U-ext", GREEN, "o"), ("U-ext+seed", GREEN, "s"),
       ("L0", ORANGE, "o"), ("L0+seed", ORANGE, "s"),
       ("LOOP", BLUE, "o"), ("LOOP+seed", BLUE, "s"),
       ("Ours", VERM, "s"), ("Ours-seed", VERM, "o"),
       ("Ours-passes", VERM, "^")]
def draw(ax, k, x, yv, c, m):
    ax.scatter(x, yv, color=c, marker=m, s=26, zorder=3, edgecolor=c if m != "o" else c, linewidth=0.9,
               facecolor="white" if m == "o" else c)
fig, axs = plt.subplots(1, 2, figsize=(7.16, 2.5))
ax = axs[0]
two_data = []
for k, c, m in two:
    x, yv = am[k]["tok_total"]["mean"], 100*am[k]["gc"]["mean"]
    two_data.append((k, k, x, yv)); draw(ax, k, x, yv, c, m)
ax.set_xscale("log"); ax.set_xlim(7e4, 1.6e6)
ax.set_xlabel("Tokens per unit (log scale)"); ax.set_ylabel("Grounded QA (%)")
ax.set_ylim(35, 66)
ax.set_title("2WikiMultihopQA", fontsize=8, weight="bold", loc="left")
ax = axs[1]
trex = [("U-ext+seed", GREEN), ("L0+seed", ORANGE), ("LOOP+seed", BLUE), ("Ours", VERM)]
trex_data = []
for k, c in trex:
    a = b4["arms"][k]; x, yv = a["tok_total"]["mean"], 100*a["gc"]["mean"]
    trex_data.append((k, k, x, yv)); draw(ax, k, x, yv, c, "s")
ax.set_xscale("log"); ax.set_xlim(1.2e4, 6e5); ax.set_ylim(22, 46)
ax.set_xlabel("Tokens per unit (log scale)"); ax.set_ylabel("Grounded QA (%)")
ax.set_title("T-REx", fontsize=8, weight="bold", loc="left")
fmt = FuncFormatter(lambda v, p: f"{v/1e6:g}M" if v >= 1e6 else f"{v/1e3:g}k")
axs[0].set_xticks([1e5, 2e5, 5e5, 1e6]); axs[1].set_xticks([2e4, 5e4, 1e5, 2e5, 5e5])
for a_ in axs:
    a_.xaxis.set_major_formatter(fmt); a_.xaxis.set_minor_formatter(NullFormatter())
    for s_ in ("top", "right"): a_.spines[s_].set_visible(False)
def H_(c, m, lab):
    return Line2D([], [], color=c, marker=m, ls="", ms=26**0.5, markerfacecolor="white" if m == "o" else c, markeredgewidth=0.9, label=lab)
handles = [H_(GREEN, "s", "no CQs"), H_(ORANGE, "s", "single pass"), H_(BLUE, "s", "loop"), H_(VERM, "s", "combined"),
           H_(GREY, "s", "filled: with relation list"), H_(GREY, "o", "open circle: without list"), H_(VERM, "^", "combined, first pass only")]
fig.legend(handles=handles, loc="lower center", ncol=4, fontsize=7, frameon=False, columnspacing=1.4, handletextpad=0.3)
fig.tight_layout(pad=0.5, w_pad=1.5, rect=(0, 0.21, 1, 1))
fig.savefig(os.path.join(HERE, "fig_cost_quality_r64.pdf")); plt.close(fig)

# ---------- FIGURE_DATA.md ----------
L = ["# Figure data (generated by make_figs.py; existing results only)", "",
     "## fig_seed_forest.pdf (pp = percentage points; 95% intervals)", "",
     "| group | pipeline | metric | delta | 95% CI | source and key |", "|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {'original seed (descriptive)' if r[0]=='orig' else 'synonym seed (registered)'} | {r[1]} | "
             f"{'grounded QA (gc)' if r[0]=='orig' else 'answer correct'} | {r[2]:+.2f} | [{r[3]:.2f}, {r[4]:.2f}] | {r[5]} |")
L += ["", "All four original-seed intervals are present in results_postreview.json (LEDGER line 118); none missing.",
      "", "## fig_cost_quality.pdf", "", "Left panel, 2Wiki (Exp8), source "+S27+" `arm_means.<arm>.{gc.mean,tok_total.mean}`:", "",
      "| arm key | label | tokens/unit | grounded QA (%) |", "|---|---|---|---|"]
for k, lab, x, yv in two_data: L.append(f"| {k} | {lab} | {x:,.0f} | {yv:.2f} |")
L += ["", "Right panel, T-REx, source "+B4+" `arms.<arm>.{gc.mean,tok_total.mean}` (only the four seeded arms exist in B4):", "",
      "| arm key | label | tokens/unit | grounded QA (%) |", "|---|---|---|---|"]
for k, lab, x, yv in trex_data: L.append(f"| {k} | {lab} | {x:,.0f} | {yv:.2f} |")
L += ["", "Not plotted: Ours-expand (2Wiki arm_means exists; omitted for clarity). No error bars in Figure B (arm-mean CIs exist in the JSON, not drawn).", ""]
open(os.path.join(HERE, "FIGURE_DATA.md"), "w").write("\n".join(L))
