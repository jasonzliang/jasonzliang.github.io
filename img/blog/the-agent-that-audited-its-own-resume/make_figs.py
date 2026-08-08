"""Figure for "The agent that audited its own resume".

Eight claimed "I built on X" links, checked one by one against the git
history. Two survived.

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
    "xtick.labelsize": 11.5, "ytick.labelsize": 13,
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
CLAIMED = 8
SEGMENTS = [
    ("Verified", 2, BLUE, "found in the git history"),
    ("Unsupported", 3, GREY, "no evidence either way"),
    ("Phantom", 3, RED, "the work was never there"),
]

fig, ax = plt.subplots(figsize=(9.6, 3.6))

BAR_H = 0.46

# top bar: what the agent claimed
ax.barh(1, CLAIMED, height=BAR_H, color=ORANGE, zorder=3)
ax.text(CLAIMED / 2.0, 1, "8 claims", ha="center", va="center",
        fontsize=15, fontweight="bold", color="white", zorder=4)

# bottom bar: what survived the check, stacked
left = 0.0
for label, n, colour, _sub in SEGMENTS:
    ax.barh(0, n, left=left, height=BAR_H, color=colour, zorder=3,
            edgecolor="white", linewidth=1.6)
    ax.text(left + n / 2.0, 0, str(n), ha="center", va="center",
            fontsize=15, fontweight="bold", color="white", zorder=4)
    ax.text(left + n / 2.0, -0.40, label, ha="center", va="top",
            fontsize=12, fontweight="bold", color=colour, zorder=4)
    ax.text(left + n / 2.0, -0.60, _sub, ha="center", va="top",
            fontsize=10.5, color=MUTED, zorder=4)
    left += n

ax.set_yticks([1, 0])
ax.set_yticklabels(["It said\nit built on", "The git\nhistory says"])
ax.set_ylim(-0.95, 1.45)
ax.set_xlim(0, 8.35)
ax.set_xticks(range(0, 9))
for s in ("top", "right", "left", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="both", length=0, pad=8)
ax.set_xticklabels([])

ax.set_title("Eight claimed influences. Two survived a check against the record.",
             loc="left", pad=14)

save(fig, "claimed-vs-verified")
