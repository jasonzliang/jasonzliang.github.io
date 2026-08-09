"""Figure for "We asked three AIs to grade seven AIs".

The gap between what each judge gave the two baseline systems from its own
model family and what the other two judges gave those same answers, broken out
by answer format. The sign changes with format, which is the point.

This is a RAW difference of means. It is not adjusted for how strict a judge
was overall, so it does not isolate self-preference: see the footnote drawn
under the legend, and the post body.

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


# --- data (verified): judge -> gap on own family, by answer format
# Source: caesar/paper/caesar.pdf, Table 2 (left), "Judge Bias and Robustness
# Analysis". Columns FULL / ELI5 / 450W. Values are points on the 30-point
# New+Useful+Surprising total.
#
# The "own family" group is the two baselines carrying that judge's model name
# (e.g. Gemini 3 Deep + Gemini 3 Shallow); Caesar is NOT in the GPT group even
# though it runs on GPT-5.2. Confirmed two ways: the family match in
# caesar/analysis/judge_analysis.py:446-456 is a name-substring test that
# Caesar's codename misses, and folding Caesar into the GPT group would make
# the 450W entry +0.67 rather than the published +0.97.
JUDGES = ["Gemini", "Claude", "GPT"]
FORMATS = [
    ("Full answer", [1.35, 0.98, -0.82], BLUE),
    ("Explain-like-I'm-five", [-0.12, -0.20, -0.75], ORANGE),
    ("450-word answer", [-0.29, -0.22, 0.97], GREY),
]

fig, ax = plt.subplots(figsize=(9.6, 4.7))

W = 0.26
for k, (fmt, vals, colour) in enumerate(FORMATS):
    offs = (k - 1) * (W + 0.02)
    xs = [i + offs for i in range(len(JUDGES))]
    ax.bar(xs, vals, width=W, color=colour, label=fmt, zorder=3)
    for x, v in zip(xs, vals):
        pad = 0.06 if v >= 0 else -0.06
        ax.text(x, v + pad, ("%+.2f" % v).replace("-", "−"), ha="center",
                va="bottom" if v >= 0 else "top", fontsize=10.5, color=INK,
                zorder=4)

ax.axhline(0, color=INK, lw=1.3, zorder=4)
ax.set_xticks(range(len(JUDGES)))
ax.set_xticklabels(JUDGES)
ax.set_xlim(-0.62, len(JUDGES) - 0.38)
ax.set_ylim(-1.25, 1.75)
ax.set_yticks([-1, -0.5, 0, 0.5, 1, 1.5])
ax.set_yticklabels(["−1", "−0.5", "0", "+0.5", "+1", "+1.5"])
ax.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="x", length=0, pad=8)
ax.tick_params(axis="y", length=3, width=0.8)

ax.set_ylabel("Points on the 30-point total\n(New + Useful + Surprising)",
              labelpad=8)

fig.text(0.02, 1.02, "A judge's gap on its own family changes sign with the answer format",
         ha="left", va="bottom", fontsize=16, fontweight="bold", color=INK)
fig.text(0.02, 0.955,
         "What each judge gave the two baseline systems from its own model "
         "family, minus what the other two judges gave those same answers",
         ha="left", va="bottom", fontsize=11.5, color=MUTED)

ax.text(-0.58, 1.62, "above the line = scored its own family above the panel",
        fontsize=10.5, color=MUTED, va="center")
ax.text(-0.58, -1.13, "below the line = scored it below the panel",
        fontsize=10.5, color=MUTED, va="center")

ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), ncol=3,
          handlelength=1.2, handleheight=1.0, columnspacing=2.0)

ax.text(0.5, -0.30,
        "Raw differences, not adjusted for how strict each judge was overall. "
        "On full answers the GPT judge marked every\nagent about 2 points below "
        "the other two, so its −0.82 is strictness, not self-criticism. "
        "No error bars: the paper reports none.",
        transform=ax.transAxes, ha="center", va="top", fontsize=9.5,
        color=MUTED, linespacing=1.45)

save(fig, "judge-bias")
