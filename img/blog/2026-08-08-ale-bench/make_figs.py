"""Figure for "I let four agents rewrite their own values".

The self-modification x disposition interaction on ALE-Bench AHC039: what
letting a run rewrite its own values mid-loop does to the verified score,
per disposition.

Source of every number:
  self_improvement_v2/reports/ale-bench-ahc039/
    2026-08-04_ale-bench-ahc039_2x4-values_report.pdf, Table 3
    ("The self-modification x disposition interaction"), best verified DEV
    score (post-run --no-cache recompute) per run:

        disposition   base      radical   delta (radical - base)
        control       3099.8    3573.9      +474
        anti          3559.6    3745.5      +186
        nietzsche     3533.6    3443.7       -90
        tzeentch      3787.2    3560.6      -227

  Context numbers in the footnote, same report, Section 1 (Setup):
    from-scratch baseline ~= 1851, anchor bar (best single 64x64 rectangle)
    = 1871.

  One run per cell: directional, not statistically powered.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
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
    png = os.path.join("/tmp", "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# ---------------------------------------------------------------------------
# What the figure has to show
#
# The claim is that self-modification helps the self-limiting dispositions and
# taxes the exploratory ones. The obvious rival explanation is regression to
# the mean: the run that started lowest had the most room to gain.
#
# Plotting the frozen score against the change tests that directly, and the
# data refutes it. `nietzsche` (3533.6) and `anti` (3559.6) start 26 points
# apart, effectively tied, and move in opposite directions: -90 and +186.
#
# An earlier version drew one arrow per disposition along a single score axis.
# That put absolute score and size-of-change on the same axis, so neither read
# cleanly, and gave the reader no way to check the claim in the title.
#
# Label offsets are hand-placed per point: at n=4 an automatic placer is not
# worth it, and two of the points sit close enough to collide.
RUNS = [
    # name, gloss, frozen, self-modifying, (dx, dy, ha, va) for the name label
    ("control", "smallest verified step,\nbank it and stop",
     3099.8, 3573.9, (0, -46, "center", "top")),
    ("nietzsche", "go at the hardest\nresistance",
     3533.6, 3443.7, (-18, -10, "right", "top")),
    ("anti", "chase the measured\nnumber, nothing else",
     3559.6, 3745.5, (0, 40, "center", "bottom")),
    ("tzeentch", "keep several lines\nalive, never settle",
     3787.2, 3560.6, (-26, 0, "right", "center")),
]

fig, ax = plt.subplots(figsize=(10.0, 6.2))
fig.subplots_adjust(top=0.80, bottom=0.26, left=0.10, right=0.97)

for name, gloss, frozen, radical, (dx, dy, ha, va) in RUNS:
    change = radical - frozen
    colour = BLUE if change > 0 else RED
    ax.scatter([frozen], [change], s=190, color=colour, zorder=4,
               edgecolor="white", linewidth=1.6)
    ax.annotate("%s\n%s" % (name, gloss), xy=(frozen, change),
                xytext=(dx, dy), textcoords="offset points",
                ha=ha, va=va, fontsize=10.5, color=MUTED, linespacing=1.45)
    ax.annotate("%+d" % round(change), xy=(frozen, change),
                xytext=(15, -5), textcoords="offset points",
                fontsize=13, fontweight="bold", color=colour)

ax.axhline(0, color=MUTED, lw=1.2, zorder=2)

# the pair that refutes the regression-to-the-mean reading
ax.plot([3533.6, 3559.6], [-89.9, 185.9], color=GREY, lw=1.2, ls=":", zorder=1)
ax.annotate("these two start 26 points apart\nand move in opposite directions",
            xy=(3548, 60), xytext=(3210, 330), fontsize=10.5, color=INK,
            ha="left", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.2,
                            connectionstyle="arc3,rad=-0.3"))

ax.set_xlim(3010, 3900)
ax.set_ylim(-340, 600)
ax.set_yticks([-200, 0, 200, 400])
ax.set_xlabel("Score with its values frozen", labelpad=8)
ax.set_ylabel("Change when allowed to rewrite them", labelpad=8)
ax.grid(color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)

fig.text(0.10, 0.955,
         "Rewriting its own values helped two dispositions and cost two",
         fontsize=15, fontweight="bold", va="top")
fig.text(0.10, 0.895,
         "If this were only the weakest run having the most room to improve, "
         "the points would fall on a line.",
         fontsize=11.5, color=MUTED, va="top")
fig.text(0.10, 0.135,
         "One run per cell: directional, not powered. Each point pairs a run "
         "with its own twin at the same values\ngeneration, but control and "
         "anti exist only at generation v6 while nietzsche and tzeentch ran at "
         "v7, so\ncompare within a pair more confidently than across pairs. "
         "The from-scratch starting solver scores 1,851.",
         fontsize=10.5, color=MUTED, va="top", linespacing=1.7)

save(fig, "self-mod-by-disposition")


# ---------------------------------------------------------------------------
# Second figure: the per-iteration score curve.
#
# Source: same report, Table 2 ("Verified per-iteration DEV score", one
# recompute per iteration). Transcribed verbatim below; the report's own
# delta column is computed from unrounded scores, so it can differ by 1 from
# these rounded values.
#
# Why this plot: the scatter above shows the endpoint interaction but hides
# how it arises. Pairing each disposition's frozen run (solid) against its
# self-modifying twin (dashed) in the same colour makes three things legible
# at once that the endpoint numbers only assert:
#   1. three of the four self-modifying runs start BELOW their frozen twin,
#      the early budget going into rewriting values instead of solver;
#   2. the exploiter plateau: anti-frozen and nietzsche-frozen are flat from
#      iteration 2 onward (+60 and +53 across the last nine);
#   3. control-radical's single-step jump at iteration 2, the largest in the
#      table, right after it rewrote its own values.
TRAJ = {
    # disposition: (frozen 10 iterations, self-modifying 10 iterations)
    "control": ([2880, 3058, 3060, 3084, 3042, 3036, 3047, 3091, 3059, 3100],
                [3048, 3486, 3505, 3508, 3558, 3568, 3571, 3571, 3573, 3574]),
    "anti": ([3496, 3519, 3528, 3538, 3540, 3557, 3560, 3558, 3559, 3556],
             [3374, 3503, 3516, 3680, 3690, 3689, 3723, 3727, 3736, 3746]),
    "nietzsche": ([3480, 3508, 3513, 3522, 3524, 3524, 3526, 3530, 3530, 3534],
                  [3095, 3148, 3248, 3335, 3348, 3405, 3407, 3419, 3420, 3444]),
    "tzeentch": ([3495, 3681, 3720, 3744, 3759, 3764, 3773, 3783, 3787, 3785],
                 [3397, 3476, 3511, 3521, 3522, 3526, 3552, 3558, 3559, 3561]),
}
GREEN, PURPLE = "#2f855a", "#6b46c1"
COLOUR = {"control": BLUE, "anti": ORANGE,
          "nietzsche": GREEN, "tzeentch": PURPLE}

ITERS = list(range(1, 11))

fig, ax = plt.subplots(figsize=(10.0, 6.4))
fig.subplots_adjust(top=0.80, bottom=0.22, left=0.10, right=0.80)

for name, (frozen, radical) in TRAJ.items():
    c = COLOUR[name]
    ax.plot(ITERS, frozen, color=c, lw=2.1, ls="-", zorder=3,
            marker="o", ms=3.5)
    ax.plot(ITERS, radical, color=c, lw=2.1, ls="--", zorder=3,
            marker="o", ms=3.5, dashes=(4, 2.2))

# Four of the eight endpoints land within 40 points of each other, so
# labelling every line at the right edge collides illegibly. A colour key
# outside the axes costs one lookup and stays readable.

# control-radical's jump, the single largest step in the table
ax.annotate("rewrote its own values at iteration 1,\nthen +438 in one step",
            xy=(2, 3486), xytext=(2.5, 2930), fontsize=10.5, color=INK,
            ha="left", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.2,
                            connectionstyle="arc3,rad=-0.2"))

ax.set_xlim(0.8, 10.2)
ax.set_ylim(2820, 3870)
ax.set_xticks(ITERS)
ax.set_xlabel("iteration", labelpad=8)
ax.set_ylabel("verified score on the 30 development cases", labelpad=8)
ax.grid(color=GRID, lw=0.8)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)

solid = plt.Line2D([], [], color=MUTED, lw=2.1, ls="-")
dashed = plt.Line2D([], [], color=MUTED, lw=2.1, ls="--", dashes=(4, 2.2))
style_key = ax.legend([solid, dashed],
                      ["values frozen", "values self-modifying"],
                      loc="lower right", fontsize=11)
ax.add_artist(style_key)

handles = [plt.Line2D([], [], color=COLOUR[n], lw=2.6) for n in TRAJ]
ax.legend(handles, list(TRAJ), loc="upper left",
          bbox_to_anchor=(1.015, 1.0), fontsize=11.5,
          title="disposition", alignment="left")

fig.text(0.10, 0.955,
         "The self-modifying runs start lower and climb harder",
         fontsize=15, fontweight="bold", va="top")
fig.text(0.10, 0.895,
         "Each colour is one disposition: solid is its frozen run, dashed is "
         "the twin allowed to rewrite its own values.",
         fontsize=11.5, color=MUTED, va="top")
fig.text(0.10, 0.105,
         "One run per cell: directional, not powered. The from-scratch "
         "starting solver scores 1,851, below the bottom of this axis.\n"
         "control and anti exist only at values generation v6 while nietzsche "
         "and tzeentch ran at v7, so compare within a\ncolour more confidently "
         "than across colours.",
         fontsize=10.5, color=MUTED, va="top", linespacing=1.7)

save(fig, "score-per-iteration")
