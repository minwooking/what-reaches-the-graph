"""Figures for cq_dissection from existing results only (no LLM calls). Run: python3 -I make_figs.py"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
H = "paper/access2026/harness"
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
fig, axs = plt.subplots(2, 1, figsize=(3.5, 2.35), gridspec_kw={"height_ratios": [4, 2.3]})
groups = [("orig", "Original list: grounded QA", BLUE, "o"), ("syn", "Synonym list: answer correctness", VERM, "D")]
ypos = []
for ax, (g, title, c, m) in zip(axs, groups):
    rs = [r for r in rows if r[0] == g]
    ax.axvline(0, color=GREY, lw=0.8, ls="--", zorder=0)
    for j, r in enumerate(rs):
        ax.errorbar(r[2], j, xerr=[[r[2]-r[3]], [r[4]-r[2]]], fmt=m, color=c, ms=5, lw=1.4, capsize=2.5, capthick=1)
        ax.text(round1(r[4])+0.8, j, f"{round1(r[2]):+.1f} [{round1(r[3]):.1f}, {round1(r[4]):.1f}]".replace("-", "−"), va="center", fontsize=8)
    ax.set_yticks(range(len(rs))); ax.set_yticklabels([{"L0": "CQ-guided\nsingle pass", "LOOP": "Repair loop", "combined": "Combined", "U-ext": "Extraction\nwithout CQs"}[r[1]] for r in rs]); ax.set_ylim(len(rs)-0.5, -0.5)
    ax.set_xlim(-6, 46)
    ax.set_title(title, fontsize=8, weight="bold", loc="left", color=c)
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
axs[0].set_xticklabels([])
axs[1].set_xlabel("Effect of the relation list (points)")
fig.tight_layout(pad=0.4, h_pad=0.8)
fig.savefig(os.path.join(HERE, "fig_seed_forest.pdf")); plt.close(fig)

# ---------- Figure B (r61: full-width, legend instead of inline labels, fonts >= 7 pt) ----------
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, NullFormatter
am = s27["arm_means"]
NOC, SP, LP, CB = "#777777", ORANGE, BLUE, "#000000"
two = [("U-ext", NOC, "s", False), ("U-ext+seed", NOC, "s", True),
       ("L0", SP, "o", False), ("L0+seed", SP, "o", True),
       ("LOOP", LP, "^", False), ("LOOP+seed", LP, "^", True),
       ("Ours", CB, "D", True), ("Ours-seed", CB, "D", False),
       ("Ours-passes", CB, "*", True)]
OFF = {"LOOP+seed": 1.10, "Ours": 0.90, "Ours-seed": 0.90, "LOOP": 1.0, "L0": 1.0, "U-ext": 0.93, "L0+seed": 1.07}  # small sideways shifts for overlapping points
def draw(ax, x, yv, c, m, filled, off=1.0):
    ax.scatter(x*off, yv, color=c, marker=m, s=60 if m != "*" else 110, zorder=3, edgecolor=c, linewidth=1.2,
               facecolor=c if filled else "white")
fig, axs = plt.subplots(1, 2, figsize=(7.16, 1.9))
ax = axs[0]
two_data = []
for k, c, m, f in two:
    x, yv = am[k]["tok_total"]["mean"], 100*am[k]["gc"]["mean"]
    two_data.append((k, k, x, yv)); draw(ax, x, yv, c, m, f, OFF.get(k, 1.0))
ax.set_xscale("log"); ax.set_xlim(7e4, 1.6e6)
ax.set_xlabel("Tokens per unit (log scale)"); ax.set_ylabel("Grounded QA (%)")
ax.set_ylim(35, 70)
# list-schema pass, 60 main-run units (study32 b73_listschema_full60/results.json arm_means['S0+seed'])
B73 = os.path.join(H, "study32_reviewer_checks", "b73_listschema_full60", "results.json")
ls_ = json.load(open(B73))["arm_means"]["S0+seed"]
xl, yl = ls_["tok_total"]["mean_units"], 100*ls_["gc"]["mean_units"]
GREEN = "#009E73"
ax.scatter(xl, yl, color=GREEN, marker="P", s=90, zorder=4, edgecolor=GREEN, linewidth=1.0)
xb, yb = am["Ours"]["tok_total"]["mean"], 100*am["Ours"]["gc"]["mean"]
assert 7 < xb/xl < 9 and 4 < yl-yb < 5
ax.annotate("", xy=(xl*1.08, yl), xytext=(xb*OFF["Ours"]*0.93, yb+0.4), arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9))
ax.text(xl*1.35, yl+1.2, "list-schema pass: +4.6 points at one eighth of the tokens", ha="left", va="bottom", fontsize=7.5)
ax.set_title("2WikiMultihopQA", fontsize=8, weight="bold", loc="left")
ax = axs[1]
trex = [("U-ext+seed", NOC, "s"), ("L0+seed", SP, "o"), ("LOOP+seed", LP, "^"), ("Ours", CB, "D")]
trex_data = []
for k, c, m in trex:
    a = b4["arms"][k]; x, yv = a["tok_total"]["mean"], 100*a["gc"]["mean"]
    trex_data.append((k, k, x, yv)); draw(ax, x, yv, c, m, True, {"LOOP+seed": 1.12, "Ours": 0.89}.get(k, 1.0))
ax.set_xscale("log"); ax.set_xlim(1.2e4, 6e5); ax.set_ylim(22, 48)
ax.set_xlabel("Tokens per unit (log scale)"); ax.set_ylabel("Grounded QA (%)")
ax.set_title("T-REx", fontsize=8, weight="bold", loc="left")
fmt = FuncFormatter(lambda v, p: f"{v/1e6:g}M" if v >= 1e6 else f"{v/1e3:g}k")
axs[0].set_xticks([1e5, 2e5, 5e5, 1e6]); axs[1].set_xticks([2e4, 5e4, 1e5, 2e5, 5e5])
for a_ in axs:
    a_.xaxis.set_major_formatter(fmt); a_.xaxis.set_minor_formatter(NullFormatter())
    for s_ in ("top", "right"): a_.spines[s_].set_visible(False)
def H_(c, m, lab, f=True):
    return Line2D([], [], color=c, marker=m, ls="", ms=(60 if m != "*" else 110)**0.5, markerfacecolor=c if f else "white", markeredgewidth=1.2, label=lab)
handles = [H_(NOC, "s", "plain extraction"), H_(SP, "o", "single pass"), H_(LP, "^", "repair loop"), H_(CB, "D", "combined"),
           H_(GREY, "s", "filled: list"), H_(GREY, "s", "open: no list", False), H_(CB, "*", "first pass only"), H_(GREEN, "P", "list-schema pass")]
fig.legend(handles=handles, loc="lower center", ncol=8, fontsize=7, frameon=False, columnspacing=0.6, handletextpad=0.3)
fig.tight_layout(pad=0.5, w_pad=1.5, rect=(0, 0.12, 1, 1))
fig.savefig(os.path.join(HERE, "fig_cost_quality.pdf")); plt.close(fig)

# ---------- FIGURE_DATA.md ----------
L = ["# Figure data (generated by make_figs.py; existing results only)", "",
     "## fig_seed_forest.pdf (pp = percentage points; 95% intervals)", "",
     "| group | pipeline | metric | delta | 95% CI | source and key |", "|---|---|---|---|---|---|"]
for r in rows:
    L.append(f"| {'original seed' if r[0]=='orig' else 'synonym seed'} | {r[1]} | "
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
