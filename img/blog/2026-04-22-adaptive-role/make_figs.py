"""Figure for "The agent rewrites its own job description before it starts".

Three runs from ONE batch, three starting queries, three role descriptions the
agent wrote for itself before exploring anything.

Provenance. All five runs in the `4_5_*` batch were launched within eight
seconds of each other (03:57:43 to 03:57:51 in their own logs), from the same
checkout, with the same exploration model (`gpt-5.4-mini`) and the same
`config_creative` settings. Only the starting query differs. That is why the
figure can say "same code, same instruction": it is one batch, not three runs
picked from three different months. An earlier version of this figure mixed a
December-2025 run (whose prompt still said "~500 tokens", not "~N words") with
a May-2026 one, and could not honestly claim either.

Every string below is a VERBATIM substring of that run's own console log, under
  /Users/jason/Desktop/rome/caesar/result/<run>/__rome__/
      agent_CaesarExplorer.console.log

  Query   the `Starting Query:` line. "…" marks a cut; nothing is reworded.
  Name    the `[ADAPT ROLE] Using newly adapted role:` block, from the
          "Your role: ..." opening. The agent's own capitalisation and wording
          are kept, which is why run 2 is a sentence fragment rather than a
          title.
  Words   a contiguous verbatim span from the same block. "…" marks a cut.
          Nothing is condensed or paraphrased.

  run 1  4_5_constrained_creativity
  run 2  4_5_crossdomain_synthesis
  run 3  4_5_openended_creativity

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, RED = "#2b6cb0", "#dd6b20", "#c53030"
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
    png = os.path.join("/tmp", "_role_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# (query the run started from, name the agent gave itself, its own next words)
RUNS = [
    (BLUE,
     "Invent a new emotion that humans don't experience…",
     "Speculative Affective Cartographer",
     "…an explorer of the unmapped regions of feeling, tasked with inventing "
     "emotions that sit just beyond the human repertoire…"),
    (ORANGE,
     "Apply the mathematical structure of calculus… to cooking…",
     "A structural translator of recipes into calculus-like transformations",
     "…you are a pattern cartographer who seeks the formal skeleton shared by "
     "calculus and cooking."),
    (RED,
     "Invent a completely original business idea that doesn't exist yet.",
     "Blue-Ocean Cartographer of Hidden Frictions",
     "…an explorer who turns overlooked annoyance, workaround, and emerging "
     "technological overlap into completely original business concepts."),
]

fig, ax = plt.subplots(figsize=(10.2, 7.1))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ax.text(0.0, 0.99, "One batch, one instruction. Three queries, three "
        "self-written roles.", fontsize=15, fontweight="bold", va="top")

# Keep (top - 2 * (height + gap)) - height comfortably above 0, or the bottom
# card is clipped away by bbox_inches="tight".
top, height, gap = 0.915, 0.285, 0.028
LABEL_X, VALUE_X = 0.028, 0.155
for i, (colour, query, name, words) in enumerate(RUNS):
    y = top - i * (height + gap)
    ax.add_patch(FancyBboxPatch(
        (0.0, y - height), 1.0, height,
        boxstyle="round,pad=0.004,rounding_size=0.012",
        fc="#f7fafc", ec="#e2e8f0", lw=1.0, zorder=1))
    ax.add_patch(FancyBboxPatch(
        (0.0, y - height), 0.008, height,
        boxstyle="square,pad=0", fc=colour, ec="none", zorder=2))

    ax.text(LABEL_X, y - 0.044, "Starting query", fontsize=10,
            color=MUTED, va="center", zorder=3)
    ax.text(VALUE_X, y - 0.044, "“%s”" % query, fontsize=11.5, style="italic",
            color=MUTED, va="center", zorder=3)
    ax.text(LABEL_X, y - 0.111, "Role it wrote", fontsize=10,
            color=MUTED, va="center", zorder=3)
    ax.text(VALUE_X, y - 0.111, name, fontsize=13,
            fontweight="bold", color=colour, va="center", zorder=3)
    ax.text(LABEL_X, y - 0.158, "\n".join(textwrap.wrap(words, 90)),
            fontsize=11, color=INK, va="top", zorder=3, linespacing=1.5)

save(fig, "three-roles")
