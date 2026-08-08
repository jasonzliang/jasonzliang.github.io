"""Figure for "We ran it once and got a headline".

Cliff's delta for the tuned agent across three tests.

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
    "xtick.labelsize": 11, "ytick.labelsize": 12,
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
ROWS = [
    ("Games it tuned against", 0.80, "p = 0.001", BLUE),
    ("A harder tile-spawn", 0.60, "p = 0.024", BLUE),
    ("An unseen 5x5 board", -0.05, "p = 0.86", GREY),
]

fig, ax = plt.subplots(figsize=(8.0, 3.5))
ys = range(len(ROWS))

for y, (label, val, pval, colour) in zip(ys, ROWS):
    ax.barh(y, val, height=0.58, color=colour, zorder=3)
    if val >= 0:
        ax.text(val + 0.035, y, "+%.2f   %s" % (val, pval), va="center",
                ha="left", fontsize=11.5, color=INK, zorder=4)
    else:
        ax.text(val - 0.035, y, "%.2f   %s" % (val, pval), va="center",
                ha="right", fontsize=11.5, color=INK, zorder=4)

ax.set_yticks(list(ys))
ax.set_yticklabels([r[0] for r in ROWS])
ax.invert_yaxis()

ax.axvline(0, color=MUTED, lw=1.2, zorder=2)
ax.set_xlim(-1.0, 1.0)
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_xticklabels(["-1", "-0.5", "0", "+0.5", "+1"])
ax.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)

for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=3, width=0.8)

ax.set_title("Where the tuning helped, and where it vanished",
             loc="left", pad=14)
ax.set_xlabel(
    "Gap between the tuned runs and the baseline runs (Cliff's delta)\n"
    "+1 means every tuned run beat every baseline run;  0 means no difference",
    labelpad=10, fontsize=11, color=MUTED)

save(fig, "cliffs-delta")
