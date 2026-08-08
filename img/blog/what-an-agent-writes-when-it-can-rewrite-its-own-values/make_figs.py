"""Figure for "What an agent writes when it can rewrite its own values".

Size of the values block before and after each run, grouped by how much
permission the agent had to edit it. Log x-axis, because the radical runs
leave the others behind by more than an order of magnitude.

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


# --- data (verified): (label, runs, before range, after range, after colour)
GROUPS = [
    ("Frozen",  15, (15, 22), (15, 22),  GREY),
    ("Bounded", 11, (14, 16), (15, 26),  BLUE),
    ("Radical", 15, (15, 23), (96, 446), RED),
]
GUARDRAIL = 100

fig, ax = plt.subplots(figsize=(9.0, 4.4))

GAP, OFFSET = 1.0, 0.24
centres = []
for i, (label, runs, before, after, colour) in enumerate(GROUPS):
    y = (len(GROUPS) - 1 - i) * GAP
    centres.append((y, label, runs))

    # "before" range, drawn in grey above the centre line
    ax.plot(before, [y + OFFSET] * 2, color=GREY, lw=8, solid_capstyle="butt",
            zorder=3)
    # "after" range
    ax.plot(after, [y - OFFSET] * 2, color=colour, lw=8, solid_capstyle="butt",
            zorder=3)

    after_note = "  (unchanged)" if before == after else ""
    ax.text(before[1] * 1.13, y + OFFSET, "before  %d-%d" % before,
            va="center", ha="left", fontsize=10.5, color=MUTED, zorder=4)
    ax.text(after[1] * 1.13, y - OFFSET, "after  %d-%d%s" % (after + (after_note,)),
            va="center", ha="left",
            fontsize=10.5, color=colour if colour != GREY else MUTED,
            fontweight="bold" if colour == RED else "normal", zorder=4)

ax.set_xscale("log")
ax.set_xlim(9, 1600)
ax.set_xticks([10, 20, 50, 100, 200, 500, 1000])
ax.set_xticklabels(["10", "20", "50", "100", "200", "500", "1000"])
TOP = (len(GROUPS) - 1) * GAP
ax.set_ylim(-0.8, TOP + 1.0)

ax.set_yticks([c[0] for c in centres])
ax.set_yticklabels(["%s\n(%d runs)" % (c[1], c[2]) for c in centres])

# the guardrail the agent was told not to trip
ax.axvline(GUARDRAIL, color=INK, lw=1.4, ls="--", zorder=2)
ax.annotate("100 lines: the size the guardrail\nnames as the failure to avoid",
            xy=(GUARDRAIL, TOP + 0.60), xytext=(GUARDRAIL * 1.35, TOP + 0.72),
            ha="left", va="center", fontsize=10.5, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK, lw=0.9,
                            connectionstyle="arc3,rad=-0.25"))

ax.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=3, width=0.8)

ax.set_title("How far the agent rewrote its own values, by how much it was allowed to",
             loc="left", pad=14)
ax.set_xlabel("Lines in the values block  (log scale)", labelpad=8)

save(fig, "values-growth")
