"""Figure for "I took my own result apart, pair by pair".

Eight offline bin-packing runs. The score the agent optimized during the run
(in-run capability) against the score its finished solver got on held-out
Falkenauer-T instances it never saw.

Source of every number: the SI-v2 values-hypothesis findings deck
(documentation/self_improvement/slides/si-v2_values_hypothesis_findings.py,
2026-07-26), slide "Held-out ranking - offline (all 8 runs)":

    values (arm . version)   run     in-run    held-out score   held-out gap
    nietzsche sm-v4          07-24   0.9955    0.991            0.009
    control   v3             07-24   0.9905    0.990            0.010
    nietzsche sm-v5          v4v5    0.9931    0.985            0.015
    control   sm-v5          v4v5    0.9927    0.980            0.020
    control   sm-v4          v4v5    0.9918    0.980            0.020
    control   sm-v4          07-24   0.9950    0.841            0.159
    nietzsche sm-v4          v4v5    0.9948    0.837            0.163
    nietzsche v3             07-24   0.9916    0.756            0.244

Cross-checked against the committed run reports:
  reports/offline-binpack/2026-07-24_offline-binpack_2x2-v3-vs-v4sm.pdf
    Table 1 finals 0.9905 / 0.9916 / 0.9950 / 0.9955 ("tuned spread 0.0050");
    held-out Falkenauer-T n=2001 gaps, %: control-v3 0.96, nietzsche-v3 24.40,
    control-sm-v4 15.87, nietzsche-sm-v4 0.91; BFD / FFD floor 16.32.
  reports/offline-binpack/2026-07-25_offline-binpack_2x2-v4sm-vs-v5sm.pdf
    finals 0.9918-0.9948, "tuned spread 0.0029".

Held-out score = 1 - gap, so the BFD/FFD baseline line sits at 1 - 0.163 =
0.837. The 07-24 runs are labelled by their date; the v4v5 replication cohort
re-ran two of the same cells and is labelled "(re-run)".

Run from this directory, NOT from /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
INK, MUTED, GRID = "#1a202c", "#4a5568", "#e2e8f0"
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
    png = os.path.join(OUT, "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality,
                                        method=6)
    os.remove(png)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# label, in-run capability, held-out score, arm colour
ROWS = [
    ("nietzsche  sm-v4",            0.9955, 0.991, ORANGE),
    ("control  v3",                 0.9905, 0.990, BLUE),
    ("nietzsche  sm-v5",            0.9931, 0.985, ORANGE),
    ("control  sm-v5",              0.9927, 0.980, BLUE),
    ("control  sm-v4  (re-run)",    0.9918, 0.980, BLUE),
    ("control  sm-v4",              0.9950, 0.841, BLUE),
    ("nietzsche  sm-v4  (re-run)",  0.9948, 0.837, ORANGE),
    ("nietzsche  v3",               0.9916, 0.756, ORANGE),
]
BASELINE = 0.837          # BFD / FFD floor, 16.3% above the known optimum

fig, ax = plt.subplots(figsize=(9.9, 5.0))

ax.axvline(BASELINE, ls="--", lw=1.1, color=RED, zorder=2)
ax.text(BASELINE - 0.004, -0.72,
        "BFD/FFD baseline 0.837",
        ha="right", va="center", fontsize=10.5, color=RED)

for i, (lab, inrun, held, colour) in enumerate(ROWS):
    ax.plot([held, inrun], [i, i], color=GRID, lw=3.0, zorder=1,
            solid_capstyle="round")
    ax.plot([inrun], [i], marker="o", ms=8.5, mfc="white", mec=GREY,
            mew=2.0, zorder=3,
            label="score during the run" if i == 0 else None)
    ax.plot([held], [i], marker="o", ms=9.5, color=colour, zorder=4)

ax.set_yticks(range(len(ROWS)))
ax.set_yticklabels([r[0] for r in ROWS], fontsize=11.5, color=INK)
ax.set_ylim(len(ROWS) - 0.35, -1.05)
ax.set_xlim(0.735, 1.001)
ax.set_xticks([0.75, 0.80, 0.85, 0.90, 0.95, 1.00])
ax.set_xlabel("Score  (1.00 = a known-optimal packing)")
ax.xaxis.grid(True, color="#f0f3f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=3, width=0.8)

# numeric columns, hung off the right-hand edge
tr = ax.get_yaxis_transform()
for x, head in ((1.045, "in-run"), (1.155, "held-out")):
    ax.text(x, -1.02, head, transform=tr, ha="center", va="center",
            fontsize=10.5, color=MUTED, fontweight="bold", clip_on=False)
for i, (lab, inrun, held, colour) in enumerate(ROWS):
    ax.text(1.045, i, "%.4f" % inrun, transform=tr, ha="center", va="center",
            fontsize=11, color=MUTED, clip_on=False)
    ax.text(1.155, i, "%.3f" % held, transform=tr, ha="center", va="center",
            fontsize=11, color=colour, clip_on=False)

fig.text(0.012, 1.115,
         "Near-identical training scores, held-out scores from 0.76 to 0.99",
         ha="left", va="bottom", fontsize=16, fontweight="bold", color=INK)
fig.text(0.012, 0.977,
         "Eight offline bin-packing runs, one run per cell; the sm-v4 cells "
         "were run twice, in two cohorts.\nHollow circle: the score the agent "
         "optimised. Filled circle: the same solver on instances it never "
         "saw.\nOrange is the expansive disposition, blue the cautious one.",
         ha="left", va="bottom", fontsize=11.5, color=MUTED)

leg = ax.legend(loc="upper left", bbox_to_anchor=(-0.005, -0.135),
                handlelength=1.0, handletextpad=0.5)
fig.text(0.012, -0.175,
         "In-run scores span 0.9905 to 0.9955, a range of 0.005. Held-out "
         "scores span 0.756 to 0.991. Within one matched pair the held-out\n"
         "gap to the optimum differs 24-fold, and both dispositions appear "
         "in the top three rows and in the bottom three.",
         ha="left", va="top", fontsize=10.5, color=MUTED)

save(fig, "offline-inrun-vs-heldout")
