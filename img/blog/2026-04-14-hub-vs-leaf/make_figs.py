"""Figure for "Where an agent reads matters".

Notes harvested at hub pages vs notes harvested at leaf pages, scored on the
three NUS dimensions.

What was judged: NOT written answers. caesar/analysis/transfer_configs.py:313
concatenates the raw `insights` strings of the top-10 hub and bottom-10 leaf
nodes of each exploration graph into two files, and those files are what the
judges score. Each opens with the literal string "Insights:".

Source of every number:
  rome/caesar/query_result/
    "4_3_caesar_insight_analysis (multi-hop hub vs leaf)"/full_answers/
    judge_analysis.txt, TABLE 2:
      answer_cat_hubs    8.35  7.80  8.28  ->  24.43   (75 scorings)
      answer_cat_leaves  7.32  7.21  7.35  ->  21.88   (75 scorings)
  75 scorings = 3 judges x 5 trials x 5 challenges, over 5 texts a side.

Cliff's delta depends on the unit, and both values below are recomputed from
judge_csv.txt in that directory:
  - over the 5 per-challenge means (the paper's unit, Table 1 caption):
    delta = 1.00, strict dominance, hub min 23.67 > leaf max 23.47.
        hub  25.07 23.93 25.07 24.40 23.67
        leaf 20.87 21.33 22.27 21.47 23.47
  - over the 75 x 75 individual scorings: delta = 0.54. Hub wins 4122
    pairings, leaf 1072 (19.1%), 431 ties. Hub range 18-29, leaf 15-28.
  So 1.00 does NOT mean "every hub item beat every leaf item". The p10-p90
  whiskers below are the visual form of that: they overlap on all three
  dimensions. Percentiles recomputed from judge_csv.txt (linear interp).

Confounds to keep on the face of the figure. Graph position is NOT the only
thing that differs between the two piles:
  1. Not blind. caesar/analysis/llm_as_judge.py:143 injects the filename
     into the judge prompt; the two files are answer_cat_hubs.txt and
     answer_cat_leaves.txt, placed in the same prompt. The rubric
     (config/llm_as_judge/llm_prompts/nus_rubric_10pt_api.txt, rule 3)
     tells the judge the agent is "indicated by the file name".
  2. Revisits. transfer_configs.py:302,307 selects hubs on visit_count > 1
     and leaves on visit_count == 1. Hub visits run 3-45.
  3. Failed fetches. 16 of the 50 leaf entries are notes written on
     Cloudflare interstitials / redirects / access gates (9/10 on
     constrained_creativity, 6/10 on counterfactual_reasoning) against
     1 of 50 on the hub side. A blocked page yields no links and is never
     returned to, so the "fewest neighbours, visited once" rule selects
     for them mechanically.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
INK, MUTED = "#1a202c", "#4a5568"
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 15, "axes.titleweight": "bold",
    "axes.labelsize": 11.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 11.5, "ytick.labelsize": 11,
    "legend.frameon": False, "legend.fontsize": 11.5,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join("/tmp", "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# --- data (verified): dimension -> (hub mean, leaf mean, hub p10, hub p90,
#     leaf p10, leaf p90) over the 75 individual scorings a side
DIMS = [
    ("New",        8.35, 7.32, 7.0, 9.0, 6.0, 9.0),
    ("Useful",     7.80, 7.21, 7.0, 9.0, 6.0, 8.0),
    ("Surprising", 8.28, 7.35, 7.0, 9.0, 6.0, 9.0),
]
HUB_TOTAL, LEAF_TOTAL = 24.43, 21.88   # == the sums of the means above

# One panel. The total is just the sum of these three, so it is stated as text
# rather than given a second axis on a different 0-30 scale. Whiskers carry the
# spread, because the means alone read as a cleaner separation than there is.
fig, ax = plt.subplots(figsize=(9.6, 4.1))

W = 0.32
YMAX = 10.9
for i, (lab, hub, leaf, hlo, hhi, llo, lhi) in enumerate(DIMS):
    xh, xl = i - W / 2 - 0.015, i + W / 2 + 0.015
    ax.bar(xh, hub, width=W, color=BLUE, zorder=3,
           label="Notes taken at hub pages" if i == 0 else None)
    ax.bar(xl, leaf, width=W, color=ORANGE, zorder=3,
           label="Notes taken at leaf pages" if i == 0 else None)
    for x, lo, hi in ((xh, hlo, hhi), (xl, llo, lhi)):
        ax.plot([x, x], [lo, hi], color=INK, lw=1.4, zorder=5,
                solid_capstyle="butt")
        for y in (lo, hi):
            ax.plot([x - 0.055, x + 0.055], [y, y], color=INK, lw=1.4,
                    zorder=5)
    ax.text(xh, hhi + 0.22, "%.2f" % hub,
            ha="center", va="bottom", fontsize=11.5, color=INK, zorder=6)
    ax.text(xl, lhi + 0.22, "%.2f" % leaf,
            ha="center", va="bottom", fontsize=11.5, color=INK, zorder=6)

ax.set_xticks(range(len(DIMS)))
ax.set_xticklabels([r[0] for r in DIMS])
ax.set_xlim(-0.55, len(DIMS) - 0.45)
ax.set_ylim(0, YMAX)
ax.set_yticks([0, 2, 4, 6, 8, 10])
ax.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.tick_params(length=3, width=0.8)
ax.set_ylabel("Average rating out of 10")

fig.text(0.015, 1.045,
         "Notes taken at hub pages scored higher on all three measures",
         ha="left", va="bottom", fontsize=16, fontweight="bold", color=INK)
fig.text(0.015, 0.968,
         "Bars are group means. Whiskers span the 10th to 90th percentile of "
         "the individual scorings, which overlap on all three.",
         ha="left", va="bottom", fontsize=12, color=MUTED)

leg = ax.legend(loc="upper left", bbox_to_anchor=(-0.005, -0.11), ncol=2,
                handlelength=1.2, handleheight=1.0, columnspacing=1.8)
fig.text(0.015, -0.115,
         "Totals out of 30: %.2f for hub notes against %.2f for leaf notes, "
         "over 75 scorings a side (3 judges x 5 trials x 5 challenges,\n"
         "5 texts a side). Graph position is not the only difference between "
         "the piles: the judges saw both files, named, in one prompt, hub\n"
         "pages were also revisited more, and 16 of the 50 leaf notes were "
         "written on pages the crawler was blocked from reading."
         % (HUB_TOTAL, LEAF_TOTAL),
         ha="left", va="top", fontsize=11, color=MUTED)

save(fig, "hub-vs-leaf")
