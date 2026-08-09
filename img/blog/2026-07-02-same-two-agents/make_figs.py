"""Figure for "I called it a replication. My own audit called it a tie."

Four mission-mode self-improvement runs: two mission catalogs x two values
files, one run per cell. The post's subject is that two documents of mine
disagree about these four runs, so the figure asks the only question I can
still answer from the archived workspaces: which measured differences between
the cautious and the expansive run came out the same way on BOTH missions?

Every number below was counted today in the workspaces, not copied from the
slide deck. Sources, all under
/Users/jason/Desktop/science_moonshot/self_improvement_v1/result/

  M1 = 20260623-025758_{original,nietzsche}_50i_40m_evolving-agents
  M2 = 20260624-043601_{original,nietzsche}_40i_60m_agent-evolution

  Bar cleared at iteration.
    M1 cautious: bench/CRITERION.md freezes baseline held-out 0.728217 and
    bar >= 0.745; artifacts/iter5-2026-06-23-surrogate-search/README.md
    records held-out 0.74932, 9/10 seeds, +5.2 SEM. Cleared at iteration 5,
    never cleared again.
    M1 expansive: bench/CRITERION.md freezes random search 0.064140 as the
    bar (lower is better) over the naive EA's 0.065937, in writing:
    "Freezing the EA's 0.0659 as the bar would be a strawman." Never met;
    TASKS_DONE.md and every later artifact README keep saying so.
    M2 cautious: bench/CRITERION.md freezes qd_score 1841.000189 and bar
    2025.10 (+10%) plus coverage 1.000 plus held-out >= 2031.70;
    artifacts/iter4-2026-06-24-annealed-step-qd/README.md records 2040.66
    scored, 2033.98 held-out, coverage 1.000. Cleared at iteration 4.
    M2 expansive: bench/CRITERION.md freezes test_mean 0.867839 and bar
    >= 0.8978; TASKS_DONE.md line 2925 records the best controller at
    0.894753, short by 0.003. Never met.

  Frozen benchmarks left on disk.  ls -d bench*  ->  1, 10, 6, 13.

  TASKS_DONE.md lines, archived entries included.  wc -l  ->  869, 852,
    1487, 3055. The M2 cautious run is the only one that archived: its
    TASKS_DONE_archive/2026-06-24-iters-01-15.md holds another 994 lines,
    so the honest total for that run is 2481, not 1487. By bytes the M2
    pair is 269,678 against 308,045.

  Loose .py files at the workspace root.  ls *.py  ->  0, 39, 0, 0.

  Modules hoisted into tools/.  ls tools/*.py  ->  nk_sweep.py (1),
    stats.py (1), none (0), paired_stats.py + qd_paired.py (2).

Run from this directory. Never from /tmp: a stray /tmp/six.py there shadows
the real `six` package and breaks the matplotlib import.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
PALE = "#9fc0e0"
INK, MUTED, GRID = "#1a202c", "#4a5568", "#e2e8f0"
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 12.5, "axes.titleweight": "bold",
    "axes.labelsize": 11, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 10.5, "ytick.labelsize": 11,
    "legend.frameon": False, "legend.fontsize": 11.5,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join(OUT, "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality,
                                        method=6)
    os.remove(png)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# Bar order, top to bottom, in every panel.
ROWS = ["Mission 1  cautious", "Mission 1  expansive",
        "Mission 2  cautious", "Mission 2  expansive"]
COLS = [BLUE, ORANGE, BLUE, ORANGE]

# title, verdict, repeated?, values (None = the run never cleared its bar),
# x limit, value formatter
PANELS = [
    ("Cleared its own numerical bar", "Same on both missions", True,
     [5, None, 4, None], 9.0, lambda v: "iteration %d" % v),
    ("Frozen benchmarks left on disk", "Same on both missions", True,
     [1, 10, 6, 13], 16.0, lambda v: "%d" % v),
    ("Modules hoisted into tools/", "Not the same on both missions", False,
     [1, 1, 0, 2], 2.9, lambda v: "%d" % v),
    ("Lines of TASKS_DONE.md", "Not the same on both missions", False,
     [869, 852, 2481, 3055], 3750.0, lambda v: "{:,}".format(v)),
    ("Loose .py files at the root", "Not the same on both missions", False,
     [0, 39, 0, 0], 47.0, lambda v: "%d" % v),
]

fig, axes = plt.subplots(2, 3, figsize=(12.4, 5.9))
plt.subplots_adjust(wspace=0.22, hspace=0.55)

for k, (title, verdict, repeated, vals, xmax, fmt) in enumerate(PANELS):
    ax = axes[k // 3][k % 3]
    for i, v in enumerate(vals):
        y = -i
        if v is None:
            ax.text(xmax * 0.012, y, "never cleared it", ha="left",
                    va="center", fontsize=10.5, color=RED,
                    fontweight="bold", zorder=6)
            continue
        ax.barh(y, v, height=0.52, color=COLS[i], zorder=3)
        # The one archived log: show the archived part in a paler blue.
        if title.startswith("Lines of") and i == 2:
            ax.barh(y, 2481 - 1487, left=1487, height=0.52, color=PALE,
                    zorder=4)
        ax.text(v + xmax * 0.022, y, fmt(v), ha="left", va="center",
                fontsize=10.5, color=MUTED, zorder=6)
    ax.set_yticks([-i for i in range(4)])
    ax.set_yticklabels(ROWS if k % 3 == 0 else ["", "", "", ""])
    ax.set_ylim(-3.6, 0.6)
    ax.set_xlim(0, xmax)
    ax.set_xticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title(title, loc="left", pad=22, color=INK)
    ax.text(0, 1.045, verdict, transform=ax.transAxes, ha="left",
            va="bottom", fontsize=11,
            color=(INK if repeated else RED),
            fontweight=("bold" if repeated else "normal"))

# Sixth cell: the caveat that outranks every panel beside it.
note = axes[1][2]
note.axis("off")
note.text(0.0, 1.12,
          "The confound, which outranks\nall five panels",
          transform=note.transAxes, ha="left", va="top", fontsize=12.5,
          fontweight="bold", color=INK)
note.text(0.0, 0.80,
          "Each agent picked its own target from its\n"
          "catalog and froze its own bar at iteration 1,\n"
          "so the two runs inside a mission never sat\n"
          "the same test. Part of what I am calling\n"
          "character is the choice of target itself.\n"
          "One run per cell.",
          transform=note.transAxes, ha="left", va="top", fontsize=11,
          color=MUTED, linespacing=1.4)

fig.text(0.012, 1.055,
         "Two of five countable behaviours came out the same way on both "
         "missions.",
         ha="left", va="bottom", fontsize=16.5, fontweight="bold", color=INK)
fig.text(0.012, 0.985,
         "Four runs: two unrelated mission catalogs, two values files, one "
         "run per cell. Every number counted in the archived workspaces.",
         ha="left", va="bottom", fontsize=12, color=MUTED)

handles = [
    Patch(facecolor=BLUE, label="Cautious values file"),
    Patch(facecolor=ORANGE, label="Expansive values file"),
    Patch(facecolor=PALE, label="Log entries the run moved to "
                                "TASKS_DONE_archive/"),
]
fig.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.012, -0.045),
           ncol=3, handlelength=1.2, handleheight=1.0, columnspacing=1.8)

save(fig, "what-replicated")
