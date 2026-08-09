"""Figure for "The self-overcoming thesis".

A diagram of the argument, not a measurement. Nothing in this post has been
demonstrated, so the figure deliberately carries no axes, no units and no
quantities: it draws the structural claim that in a self-improving system each
generation is judged by criteria it inherited, so the starting values are an
axiom rather than a fence.

Generation numbering follows the post, which follows
<research-repo>/documentation/self_improvement/nietzsche_thesis.md: generation
zero is the agent a person writes, carrying the values a person chose ("a bias
of size epsilon in the generation-zero value function"), and generation ten is
ten self-edits later ("ten generations of self-edit"). Numbering the
human-written agent 1 instead would make generation ten only nine self-edits
old, which is what the earlier version of this figure and its post got wrong.

The top ending is verbatim from that document ("not a wiser agent but a more
confidently sycophantic one"); the bottom one is its statement of what the
alternative aims at ("constantly surpass their own past states"). Neither has
been observed: both are what the thesis predicts, and the figure says so.

The axes spans the whole figure so that one data unit is one inch, and every
box is sized from the measured width of the text it holds. That is what keeps
the labels inside their boxes.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE = "#2b6cb0", "#dd6b20"
INK, MUTED = "#1a202c", "#4a5568"
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "text.color": INK,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join("/tmp", "_thesis_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


TITLE = "Each generation is written and judged by the one before it"
SUB = ("Same loop, same code, two different starting values.\n"
       "Generation zero is the last thing a person writes. Every later one is "
       "written, and judged, by the one before it.")
FOOT = "Both endings are what the thesis predicts. Neither has been observed."

ROWS = [
    (ORANGE, "values that reward agreeing\nwith the median rater",
     "not a wiser agent but a more\nconfidently sycophantic one"),
    (BLUE, "values that require surpassing\nyour own last version",
     "systems that constantly surpass\ntheir own past states"),
]

GENS = [0, 1, 2, 10]
DX = [0.00, 0.95, 1.90, 3.25]            # last hop is longer: it is dashed
R = 0.29
GAP = 0.52                               # box edge to circle edge
BOXFS, BOXH = 10.5, 1.02

fig = plt.figure(figsize=(10.0, 5.5))
ax = fig.add_axes([0, 0, 1, 1])          # 1 data unit == 1 inch
ax.axis("off")


def measure(s, **kw):
    """Width and height of a text block, in inches."""
    t = fig.text(0, 0, s, **kw)
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    t.remove()
    return bb.width / fig.dpi, bb.height / fig.dpi


bold = dict(fontsize=BOXFS, fontweight="bold", linespacing=1.5)
sw = max(measure(s, **bold)[0] for _, s, _ in ROWS) + 0.58
ew = max(measure(e, **bold)[0] for _, _, e in ROWS) + 0.58

LEFT = 0.30
c1x = LEFT + sw + GAP + R                # centre of the generation-0 circle
elx = c1x + DX[-1] + R + GAP             # left edge of the ending box
W = max(elx + ew,                                       # the two rows
        LEFT + measure(SUB, fontsize=11.5, linespacing=1.5)[0],   # subtitle
        elx + ew / 2.0 + measure(FOOT, fontsize=10)[0] / 2.0,     # footnote
        ) + LEFT
H = 5.25
fig.set_size_inches(W, H)
ax.set_xlim(0, W)
ax.set_ylim(0, H)

YS = [3.25, 1.25]

for (colour, seed, ending), y in zip(ROWS, YS):
    ax.add_patch(FancyBboxPatch(
        (LEFT, y - BOXH / 2.0), sw, BOXH,
        boxstyle="round,pad=0.02,rounding_size=0.13",
        fc="#f7fafc", ec=colour, lw=1.6, zorder=3))
    ax.text(LEFT + sw / 2.0, y, seed, ha="center", va="center", color=colour,
            zorder=4, **bold)

    ax.add_patch(FancyArrowPatch(
        (LEFT + sw + 0.10, y), (c1x - R - 0.06, y), arrowstyle="-|>",
        mutation_scale=15, color=colour, lw=1.7, shrinkA=0, shrinkB=0,
        zorder=2))

    for i, (dx, g) in enumerate(zip(DX, GENS)):
        filled = i == 0
        ax.add_patch(Circle((c1x + dx, y), R, fc=colour if filled else "white",
                            ec=colour, lw=2.0, zorder=3))
        ax.text(c1x + dx, y, str(g), ha="center", va="center", fontsize=11.5,
                fontweight="bold", zorder=4,
                color="white" if filled else colour)

    for i in range(len(DX) - 1):
        ax.add_patch(FancyArrowPatch(
            (c1x + DX[i] + R + 0.06, y), (c1x + DX[i + 1] - R - 0.06, y),
            arrowstyle="-|>", mutation_scale=15, color=colour, lw=1.7,
            linestyle="-" if i < len(DX) - 2 else "--",
            shrinkA=0, shrinkB=0, zorder=2))

    ax.add_patch(FancyArrowPatch(
        (c1x + DX[-1] + R + 0.06, y), (elx - 0.10, y), arrowstyle="-|>",
        mutation_scale=15, color=colour, lw=1.7, shrinkA=0, shrinkB=0,
        zorder=2))
    ax.add_patch(FancyBboxPatch(
        (elx, y - BOXH / 2.0), ew, BOXH,
        boxstyle="round,pad=0.02,rounding_size=0.13",
        fc="#f7fafc", ec=colour, lw=1.6, zorder=3))
    ax.text(elx + ew / 2.0, y, ending, ha="center", va="center", color=colour,
            zorder=4, **bold)

ax.text(c1x, YS[0] - R - 0.16, "written by\na person", ha="center", va="top",
        fontsize=9.5, color=MUTED, linespacing=1.4)
ax.text(c1x + DX[-1] / 2.0, YS[1] - R - 0.18, "generation", ha="center",
        va="top", fontsize=10.5, color=MUTED)

ax.text(LEFT, H - 0.26, TITLE, fontsize=15, fontweight="bold", va="top")
ax.text(LEFT, H - 0.74, SUB, fontsize=11.5, color=MUTED, va="top",
        linespacing=1.5)
ax.text(elx + ew / 2.0, YS[1] - BOXH / 2.0 - 0.34, FOOT, ha="center", va="top",
        fontsize=10, color=MUTED)

save(fig, "compounding")
