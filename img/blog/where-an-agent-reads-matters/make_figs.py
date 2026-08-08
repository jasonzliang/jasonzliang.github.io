"""Figure for "Where an agent reads matters".

Answers built from hub pages vs answers built from leaf pages, scored on
three dimensions and in total.

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


# --- data (verified): dimension -> (hub, leaf)
DIMS = [("New", 8.35, 7.32), ("Useful", 7.80, 7.21), ("Surprising", 8.28, 7.35)]
TOTAL = ("Total", 24.43, 21.88)

# Total sits on a 0-30 scale while the dimensions sit on 0-10, so it gets its
# own panel rather than flattening the three that matter.
fig, (axl, axr) = plt.subplots(
    1, 2, figsize=(10.4, 4.5),
    gridspec_kw={"width_ratios": [3.1, 1.0], "wspace": 0.30})

W = 0.34


def draw(ax, rows, ymax, yticks):
    xs = range(len(rows))
    for i, (lab, hub, leaf) in enumerate(rows):
        ax.bar(i - W / 2 - 0.015, hub, width=W, color=BLUE, zorder=3,
               label="Hub pages" if i == 0 else None)
        ax.bar(i + W / 2 + 0.015, leaf, width=W, color=ORANGE, zorder=3,
               label="Leaf pages" if i == 0 else None)
        ax.text(i - W / 2 - 0.015, hub + ymax * 0.018, "%.2f" % hub,
                ha="center", va="bottom", fontsize=11, color=INK, zorder=4)
        ax.text(i + W / 2 + 0.015, leaf + ymax * 0.018, "%.2f" % leaf,
                ha="center", va="bottom", fontsize=11, color=INK, zorder=4)
    ax.set_xticks(list(xs))
    ax.set_xticklabels([r[0] for r in rows])
    ax.set_ylim(0, ymax)
    ax.set_yticks(yticks)
    ax.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=3, width=0.8)
    ax.set_xlim(-0.6, len(rows) - 0.4)


draw(axl, DIMS, 10.6, [0, 2, 4, 6, 8, 10])
draw(axr, [TOTAL], 30.5, [0, 10, 20, 30])

axl.set_ylabel("Average rating (out of 10)")
axr.set_ylabel("Sum of the three (out of 30)")

fig.text(0.045, 1.025, "Answers built from hub pages scored higher on every measure",
         ha="left", va="bottom", fontsize=16, fontweight="bold", color=INK)
fig.text(0.045, 0.955,
         "Cliff's delta = 1.00 - every hub answer scored above every leaf answer.",
         ha="left", va="bottom", fontsize=12, color=MUTED)

axl.legend(loc="upper left", bbox_to_anchor=(0.0, -0.13), ncol=2,
           handlelength=1.2, handleheight=1.0, columnspacing=1.8)

save(fig, "hub-vs-leaf")
