"""Figure for "23 people, 112 head-to-heads".

A modest human preference next to a decisive machine verdict, on the same
comparison.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import stats  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
INK, MUTED = "#1a202c", "#4a5568"
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.labelsize": 11.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "legend.frameon": False, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join("/tmp", "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# --- data (verified) -------------------------------------------------------
WINS, N = 63, 112
DELTA = 0.76  # automated evaluation, on the same comparison

pct = 100.0 * WINS / N
lo, hi = stats.binomtest(WINS, N, 0.5).proportion_ci(
    confidence_level=0.95, method="exact")
lo, hi = lo * 100, hi * 100
print("share %.2f%%  95%% CI %.1f-%.1f" % (pct, lo, hi))

fig, (axl, axr) = plt.subplots(
    1, 2, figsize=(11.0, 3.9), gridspec_kw={"width_ratios": [1.35, 1.0],
                                            "wspace": 0.24})

# ---- left: what the people preferred
axl.axvline(50, color=INK, lw=1.5, ls="--", zorder=2)
axl.text(49.2, 0.60, "a coin flip", ha="right", va="bottom", fontsize=11,
         color=INK)

axl.plot([lo, hi], [0, 0], color=BLUE, lw=3.5, solid_capstyle="round", zorder=3)
for x in (lo, hi):
    axl.plot([x, x], [-0.11, 0.11], color=BLUE, lw=2.2, zorder=3)
axl.plot([pct], [0], "o", ms=13, color=BLUE, zorder=4)

axl.text(pct, 0.20, "%.2f%%" % pct, ha="center", va="bottom", fontsize=14,
         fontweight="bold", color=BLUE)
axl.text(pct - 3.0, -0.26,
         "63 of 112 comparisons.\nThe interval still includes a coin flip.",
         ha="left", va="top", fontsize=10.5, color=MUTED)
axl.text(hi + 1.2, 0, "95%% confidence:\n%.0f%% to %.0f%%" % (lo, hi),
         ha="left", va="center", fontsize=10.5, color=MUTED)

axl.set_xlim(35, 78)
axl.set_xticks([40, 50, 60, 70])
axl.set_xticklabels(["40%", "50%", "60%", "70%"])
axl.set_ylim(-0.75, 0.85)
axl.set_yticks([])
axl.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axl.set_axisbelow(True)
for s in ("top", "right", "left"):
    axl.spines[s].set_visible(False)
axl.tick_params(axis="x", length=3, width=0.8)
axl.set_title("What 23 people preferred", loc="left", pad=12)
axl.set_xlabel("Share of head-to-heads won by the system", labelpad=8)

# ---- right: what the automated evaluation said
axr.barh([0], [DELTA], height=0.34, color=ORANGE, zorder=3)
axr.axvline(0, color=INK, lw=1.5, zorder=4)
axr.text(DELTA + 0.03, 0, u"\u2265 %.2f" % DELTA, ha="left", va="center",
         fontsize=14, fontweight="bold", color=ORANGE)
axr.text(0.035, -0.26, "on the same comparison", ha="left", va="top",
         fontsize=10.5, color=MUTED)

axr.set_xlim(0, 1.08)
axr.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
axr.set_xticklabels(["0", "0.25", "0.5", "0.75", "+1"])
axr.set_ylim(-0.75, 0.85)
axr.set_yticks([])
axr.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axr.set_axisbelow(True)
for s in ("top", "right", "left"):
    axr.spines[s].set_visible(False)
axr.tick_params(axis="x", length=3, width=0.8)
axr.set_title("What the automated scorer concluded", loc="left", pad=12)
axr.set_xlabel("Cliff's delta:  +1 means the system won every comparison",
               labelpad=8)

save(fig, "human-vs-machine")
