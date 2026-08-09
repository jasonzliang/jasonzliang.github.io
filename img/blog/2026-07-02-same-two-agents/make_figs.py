"""Figure for "The same values swap made the same two agents twice".

Four mission-mode self-improvement runs: two missions x two values files, one
run per cell. Each bar is one run. The split point is the iteration at which
the run cleared the numerical bar it froze for itself at iteration 1.

Source of every number, in order of authority (workspace first, deck second):

  Workspaces, /Users/jason/Desktop/science_moonshot/self_improvement_v1/result/
    20260623-025758_{original,nietzsche}_50i_40m_evolving-agents/
    20260624-043601_{original,nietzsche}_40i_60m_agent-evolution/

  Run lengths. .loop/runner.log in each workspace records
  "[loop] iter N done: killed=False exit=0" for every N from 1 to the cap,
  with no killed=True anywhere. So 50/50 and 40/40 are real completions, not
  a configured ceiling. Iterations that left an artifact directory behind are
  fewer: 47 and 45 of 50, 32 and 33 of 40. Most of the gap is the scheduled
  review checkpoint (every tenth iteration on mission 1, every fifth on
  mission 2), which is defined to produce no new experiment.

  Mission 1, cautious. bench/CRITERION.md: frozen EvoPrompt-GA baseline
  held-out 0.728217, bar >= 0.745. artifacts/iter5-2026-06-23-surrogate-search/
  README.md: held-out 0.74932, 9 of 10 seeds, fresh 0.74862, +5.2 SEM. Bar
  cleared at iteration 5, and never cleared again.

  Mission 1, expansive. bench/CRITERION.md: frozen random-search baseline
  0.064140, bar <= 0.06114 (lower is better). TASKS_DONE.md and every later
  artifact README carry "the frozen mission gate (bench5, n=160) stays
  NOT MET". Eight outer-loop levers refuted; iteration 41 froze bench10 at
  n=2000 and won there (+0.029547, t=46.2, 32 of 32 seeds), explicitly not
  claimed as a retroactive bar pass.

  Mission 2, cautious. bench/CRITERION.md: frozen MAP-Elites baseline
  qd_score 1841.000189, bar >= 2025.10 (baseline + 10%) plus coverage 1.000
  plus held-out >= 2031.70. artifacts/iter4-2026-06-24-annealed-step-qd/
  README.md: 2040.66 scored, 2033.98 held-out, coverage 1.000. Bar cleared at
  iteration 4. TASKS_DONE.md line 24: champion at iteration 28 is 2168.66
  scored / 2138.36 held-out against a closed-form ceiling of 2318.36.
  2138.36 / 2318.36 = 92.2%; the scored 2168.66 is 93.5% of the same ceiling,
  so 92.2% is the held-out figure.

  Mission 2, expansive. bench/CRITERION.md: frozen baseline test_mean
  0.867839, bar >= 0.8978. TASKS_DONE.md line 2925: best controller reached
  0.894753, short of the bar by 0.003. Thirteen frozen benches on disk
  (bench, bench2 ... bench13), counted by ls.

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
    png = os.path.join(OUT, "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality,
                                        method=6)
    os.remove(png)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# --- data (verified above): label, run length, iteration the bar was cleared
#     (None = never cleared), text to set inside the post-bar stretch
RUNS = [
    ("Mission 1\ncautious",  50, 5,
     "45 iterations finding where the algorithm breaks"),
    ("Mission 1\nexpansive", 50, None,
     "8 levers refuted, then a forecast of where it would win"),
    ("Mission 2\ncautious",  40, 4,
     "36 iterations climbing to 92.2% of the ceiling"),
    ("Mission 2\nexpansive", 40, None,
     "missed by 0.003, built a 13-benchmark taxonomy instead"),
]

fig, ax = plt.subplots(figsize=(10.2, 4.9))

H = 0.40
START = 0.5

for i, (lab, n, clear, note) in enumerate(RUNS):
    y = -i
    if clear is None:
        ax.barh(y, n - START, left=START, height=H, color=GREY, zorder=3)
        ax.text(START + 0.7, y, note, ha="left", va="center",
                fontsize=10.5, color="white", zorder=6)
        ax.text(START, y + 0.34, "bar never cleared", ha="left", va="bottom",
                fontsize=11, color=RED, fontweight="bold", zorder=6)
    else:
        ax.barh(y, clear - START, left=START, height=H, color=BLUE, zorder=3)
        ax.barh(y, n - clear, left=clear, height=H, color=ORANGE, zorder=3)
        ax.text(clear + 0.7, y, note, ha="left", va="center",
                fontsize=10.5, color="white", zorder=6)
        ax.plot([clear, clear], [y - H / 2 - 0.06, y + 0.30], color=INK,
                lw=1.3, zorder=5, solid_capstyle="butt")
        ax.text(clear + 0.5, y + 0.34, "bar cleared, iteration %d" % clear,
                ha="left", va="bottom", fontsize=11, color=INK,
                fontweight="bold", zorder=6)
    ax.text(n + 0.6, y, "%d" % n, ha="left", va="center", fontsize=10.5,
            color=MUTED, zorder=6)

ax.set_yticks([-i for i in range(len(RUNS))])
ax.set_yticklabels([r[0] for r in RUNS])
ax.set_ylim(-len(RUNS) + 0.35, 0.72)
ax.set_xlim(0, 53.5)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_xlabel("Iteration")
ax.xaxis.grid(True, color=GRID, lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(length=3, width=0.8)
ax.tick_params(axis="y", length=0)

fig.text(0.015, 1.045,
         "Both cautious runs cleared their bar early. Neither expansive "
         "run cleared its bar at all.",
         ha="left", va="bottom", fontsize=16, fontweight="bold", color=INK)
fig.text(0.015, 0.972,
         "Four runs, two mission catalogs, two values files, one run per "
         "cell. Every run reached its final iteration.",
         ha="left", va="bottom", fontsize=12, color=MUTED)

handles = [
    Patch(facecolor=BLUE, label="Iterations before the bar was cleared"),
    Patch(facecolor=ORANGE, label="Iterations after the bar was cleared"),
    Patch(facecolor=GREY, label="Bar never cleared"),
]
ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(-0.001, -0.155),
          ncol=3, handlelength=1.2, handleheight=1.0, columnspacing=1.8)

fig.text(0.015, -0.20,
         "Each agent picked its own target from its mission's catalog and "
         "froze its own numerical bar at iteration 1, so the two runs inside\n"
         "a mission are not clearing the same bar. Mission 1 ran 50 "
         "iterations capped at 40 minutes each; mission 2 ran 40 capped at "
         "60.\nIterations that left an artifact behind: 47 and 45 of 50, "
         "32 and 33 of 40, the shortfall being mostly scheduled review "
         "checkpoints.",
         ha="left", va="top", fontsize=11, color=MUTED)

save(fig, "four-runs")
