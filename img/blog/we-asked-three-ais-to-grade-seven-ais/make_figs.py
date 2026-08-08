"""Figure for "We asked three AIs to grade seven AIs".

How much each judge favoured its own answers, broken out by the format the
answer was written in. The sign flips with format, which is the point.

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
    "xtick.labelsize": 12.5, "ytick.labelsize": 11,
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


# --- data (verified): judge -> bias by answer format
JUDGES = ["Gemini", "Claude", "GPT"]
FORMATS = [
    ("Full answer", [1.35, 0.98, -0.82], BLUE),
    ("Explain-like-I'm-five", [-0.12, -0.20, -0.75], ORANGE),
    ("450-word answer", [-0.29, -0.22, 0.97], GREY),
]

fig, ax = plt.subplots(figsize=(9.4, 4.8))

W = 0.26
for k, (fmt, vals, colour) in enumerate(FORMATS):
    offs = (k - 1) * (W + 0.02)
    xs = [i + offs for i in range(len(JUDGES))]
    ax.bar(xs, vals, width=W, color=colour, label=fmt, zorder=3)
    for x, v in zip(xs, vals):
        pad = 0.06 if v >= 0 else -0.06
        ax.text(x, v + pad, "%+.2f" % v, ha="center",
                va="bottom" if v >= 0 else "top", fontsize=10.5, color=INK,
                zorder=4)

ax.axhline(0, color=INK, lw=1.3, zorder=4)
ax.set_xticks(range(len(JUDGES)))
ax.set_xticklabels(JUDGES)
ax.set_xlim(-0.62, len(JUDGES) - 0.38)
ax.set_ylim(-1.25, 1.75)
ax.set_yticks([-1, -0.5, 0, 0.5, 1, 1.5])
ax.set_yticklabels(["-1", "-0.5", "0", "+0.5", "+1", "+1.5"])
ax.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="x", length=0, pad=8)
ax.tick_params(axis="y", length=3, width=0.8)

ax.set_ylabel("Points a judge gave its own answers,\nabove or below what other judges gave them")
ax.set_title("Whether a judge favours itself flips with the answer format",
             loc="left", pad=14)

ax.text(-0.58, 1.60, "above the line = marked itself up", fontsize=10.5,
        color=MUTED, va="center")
ax.text(-0.58, -1.13, "below the line = marked itself down", fontsize=10.5,
        color=MUTED, va="center")

ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=3,
          handlelength=1.2, handleheight=1.0, columnspacing=2.0)

save(fig, "judge-bias")
