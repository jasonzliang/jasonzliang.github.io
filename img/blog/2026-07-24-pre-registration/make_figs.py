"""Figure for "I froze my analysis, and it said I was underpowered".

The verdict gate: the rule that forces every result into one of four boxes.
The four outcomes are drawn top to bottom in the order the post lists them,
and both orders come from `self_improvement_v2/analysis/REPORTING.md` sec 6a:

    Rule the OUTCOME axis, exactly one of: Effect (gap survives
    interval/effect-size framing + exceeds seed noise); Null (needs BOTH
    headroom -- runs at a known-optimum ceiling or shared floor =>
    Inconclusive-by-saturation, NOT Null -- AND a stated noise band / min
    detectable effect at this N); or Inconclusive/underpowered (can't bound
    the effect).

Nothing here is measured data; it is a diagram of a decision rule.

The axes deliberately spans the whole figure so that one data unit is one
inch, and every box is sized from the measured width of the text it holds.
That is what keeps the labels inside their boxes.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#718096", "#c53030"
INK, MUTED, RULE = "#1a202c", "#4a5568", "#cbd5e0"
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "text.color": INK,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join("/tmp", "_prereg_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


W, H = 10.1, 6.6
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])          # 1 data unit == 1 inch
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")


def measure(s, **kw):
    """Width and height of a text block, in inches."""
    t = fig.text(0, 0, s, **kw)
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    t.remove()
    return bb.width / fig.dpi, bb.height / fig.dpi


def box(cx, cy, w, h, text, fc, ec, fs, weight="normal", tc=INK):
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2.0, cy - h / 2.0), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.13",
        fc=fc, ec=ec, lw=1.6, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            fontweight=weight, color=tc, zorder=3, linespacing=1.55)


def arrow(pts, colour=RULE):
    for i in range(len(pts) - 2):
        ax.plot([pts[i][0], pts[i + 1][0]], [pts[i][1], pts[i + 1][1]],
                color=colour, lw=1.8, solid_capstyle="round", zorder=1)
    ax.add_patch(FancyArrowPatch(
        pts[-2], pts[-1], arrowstyle="-|>", mutation_scale=16, color=colour,
        lw=1.8, shrinkA=0, shrinkB=0, zorder=1))


def tag(x, y, s):
    ax.text(x, y, s, fontsize=10.5, color=MUTED, ha="center", va="center",
            zorder=4)


# --- content -------------------------------------------------------------
QUESTIONS = [
    "Could this benchmark have shown a difference at all?",
    "Can you bound the effect at this number of runs?",
    "Does the difference clear the measured noise floor?",
]
VERDICTS = [
    ("INCONCLUSIVE BY SATURATION",
     "every condition sits at a ceiling or a floor", "#fffaf0", ORANGE),
    ("UNDERPOWERED", "no causal claim either way", "#fff5f5", RED),
    ("EFFECT", "report it with an interval", "#ebf8ff", BLUE),
    ("NULL", "report the smallest detectable effect", "#f7fafc", GREY),
]
EXITS = ["no", "no", "yes", "no"]        # answer that sends you to each verdict

QFS, VFS = 11.5, 10.5

# Size both columns from the widest string they have to hold.
qw = max(measure(q, fontsize=QFS)[0] for q in QUESTIONS) + 0.60
vw = max(max(measure(a, fontsize=VFS, fontweight="bold")[0],
             measure(b, fontsize=VFS, fontweight="bold")[0])
         for a, b, _, _ in VERDICTS) + 0.60
qh, vh = 0.80, 1.00

QX = 0.30 + qw / 2.0                      # centre of the question column
VX = W - 0.30 - vw / 2.0                  # centre of the verdict column
ROWS = [5.10, 3.60, 2.10, 0.65]           # one row per verdict

for (head, sub, fc, ec), y in zip(VERDICTS, ROWS):
    box(VX, y, vw, vh, head + "\n" + sub, fc, ec, VFS, "bold", ec)

for q, y in zip(QUESTIONS, ROWS):
    box(QX, y, qw, qh, q, "#f7fafc", RULE, QFS)

qr, vl = QX + qw / 2.0, VX - vw / 2.0     # facing edges of the two columns

# question -> its verdict, straight across
for i in range(3):
    arrow([(qr, ROWS[i]), (vl, ROWS[i])])
    tag((qr + vl) / 2.0, ROWS[i] + 0.26, EXITS[i])

# question -> next question, straight down
for i in range(2):
    arrow([(QX, ROWS[i] - qh / 2.0), (QX, ROWS[i + 1] + qh / 2.0)])
    tag(QX - 0.36, (ROWS[i] + ROWS[i + 1]) / 2.0, "yes")

# last question -> NULL, down then across
arrow([(QX, ROWS[2] - qh / 2.0), (QX, ROWS[3]), (vl, ROWS[3])])
tag(QX - 0.36, (ROWS[2] + ROWS[3]) / 2.0 + 0.15, "no")

ax.text(0.30, H - 0.30,
        "Every result lands in exactly one box, and the boxes are fixed "
        "before scoring",
        fontsize=15, fontweight="bold", va="top", ha="left")

save(fig, "verdict-gate")
