"""Cap-sweep figure from existing B43 results only (no model calls). Run: python3 make_capsweep.py (needs matplotlib; /usr/bin/python3 has it)
AI-generated: review before use."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
R = "paper/access2026/harness/study32_reviewer_checks/b43_factcap_sweep/results.json"
am = json.load(open(R))["arm_cap"]["2wiki"]
CAPS = ["30", "60", "120"]
plt.rcParams.update({"font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 8, "ytick.labelsize": 8,
                     "legend.fontsize": 8, "pdf.fonttype": 42, "font.family": "DejaVu Sans", "axes.linewidth": 0.7})
BLUE, ORANGE, GREY = "#0072B2", "#E69F00", "#444444"
# (JSON key, legend label, colour, marker, linestyle); all three are given the relation list
ARMS = [("LOOP+seed", "Repair loop", BLUE, "^", "-"),
        ("U-ext+seed", "Seeded extraction", GREY, "s", "--"),
        ("L0+seed", "CQ-guided single pass", ORANGE, "o", ":")]
fig, ax = plt.subplots(figsize=(3.5, 2.05))
dx = {a[0]: (i - 1) * 0.02 for i, a in enumerate(ARMS)}
xs = [int(c) for c in CAPS]
for k, lab, c, m, ls in ARMS:
    y = [100 * am[k][c]["gc"]["mean"] for c in CAPS]
    lo = [100 * am[k][c]["gc"]["ci95"][0] for c in CAPS]
    hi = [100 * am[k][c]["gc"]["ci95"][1] for c in CAPS]
    x = [v * (1 + dx[k]) for v in xs]
    ax.errorbar(x, y, yerr=[[a - b for a, b in zip(y, lo)], [b - a for a, b in zip(y, hi)]], color=c, marker=m, ls=ls,
                ms=6, lw=1.6, capsize=2, capthick=0.8, elinewidth=0.8, label=lab)
ax.set_xscale("log"); ax.set_xticks(xs); ax.set_xticklabels([str(v) for v in xs]); ax.minorticks_off()
ax.set_xlim(25, 150)
ax.set_xlabel("Facts shown at answer time (cap)"); ax.set_ylabel("Grounded QA (%)")
ax.set_title("2Wiki, graph only, with the list", fontsize=8, weight="bold", loc="left")
for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
ax.set_ylim(33, 88); ax.legend(loc="upper left", ncol=1, frameon=False, handlelength=3.0, borderaxespad=0.1)
fig.tight_layout(pad=0.4)
fig.savefig(os.path.join(HERE, "fig_capsweep.pdf")); plt.close(fig)
for k, *_ in ARMS:
    print(k, [round(100 * am[k][c]["gc"]["mean"], 1) for c in CAPS])
