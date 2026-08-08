"""Figure for "We told an agent to overfit on purpose".

Left: score on the tuned games. Right: the same anti-guardrail runs on an
unseen 5x5 board, against random play.

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
TUNED = [
    ("anti\nself-modifying", 82400, RED),
    ("anti\nfrozen", 78989, RED),
    ("expansive", 76625, BLUE),
    ("cautious", 70413, BLUE),
]
HELDOUT = [("Run 1", 5510), ("Run 2", 5092), ("Run 3", 4802)]
RANDOM_PLAY = 8196

fig, (axl, axr) = plt.subplots(
    1, 2, figsize=(11.0, 4.6), gridspec_kw={"width_ratios": [4, 3], "wspace": 0.28})

# ---- left: score on the tuned games
xs = range(len(TUNED))
axl.bar(xs, [t[1] for t in TUNED], width=0.62,
        color=[t[2] for t in TUNED], zorder=3)
for x, (lab, v, _c) in zip(xs, TUNED):
    axl.text(x, v + 1400, "{:,}".format(v), ha="center", va="bottom",
             fontsize=11.5, color=INK, zorder=4)
axl.set_xticks(list(xs))
axl.set_xticklabels([t[0] for t in TUNED])
axl.set_ylim(0, 95000)
axl.set_yticks([0, 20000, 40000, 60000, 80000])
axl.set_yticklabels(["0", "20k", "40k", "60k", "80k"])
axl.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axl.set_axisbelow(True)
for s in ("top", "right"):
    axl.spines[s].set_visible(False)
axl.tick_params(length=3, width=0.8)
axl.set_title("Score on the games it tuned against", loc="left", pad=12)
axl.set_ylabel("Score")
axl.text(0.0, -0.30, "red = runs told to defeat a guardrail",
         transform=axl.transAxes, fontsize=10.5, color=MUTED)

# ---- right: the unseen 5x5 board
xs2 = range(len(HELDOUT))
axr.bar(xs2, [h[1] for h in HELDOUT], width=0.55, color=RED, zorder=3)
for x, (lab, v) in zip(xs2, HELDOUT):
    axr.text(x, v + 160, "{:,}".format(v), ha="center", va="bottom",
             fontsize=11.5, color=INK, zorder=4)
axr.axhline(RANDOM_PLAY, color=INK, lw=1.6, ls="--", zorder=4)
axr.text(len(HELDOUT) - 0.5, RANDOM_PLAY + 260,
         "random play  {:,}".format(RANDOM_PLAY), ha="right", va="bottom",
         fontsize=11, color=INK, zorder=5)
axr.set_xticks(list(xs2))
axr.set_xticklabels([h[0] for h in HELDOUT])
axr.set_ylim(0, 10500)
axr.set_yticks([0, 2000, 4000, 6000, 8000, 10000])
axr.set_yticklabels(["0", "2k", "4k", "6k", "8k", "10k"])
axr.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axr.set_axisbelow(True)
for s in ("top", "right"):
    axr.spines[s].set_visible(False)
axr.tick_params(length=3, width=0.8)
axr.set_title("Score on a board one square wider", loc="left", pad=12)
axr.text(0.0, -0.30, "the three anti-guardrail runs, on a board never seen",
         transform=axr.transAxes, fontsize=10.5, color=MUTED)

save(fig, "tuned-vs-heldout")
