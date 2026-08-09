"""Figure for "I told an agent to overfit on purpose".

Two stacked panels over the SAME nine conditions in the SAME left-to-right
order, so each condition can be traced between them.

Top: the tuned-games score (4x4 DEV), linear, with the greedy 1-ply anchor.
Bottom: the same nine solvers on an unseen 5x5 board, log scale, against the
random floor and the greedy 5x5 baseline.

Source: science_moonshot/self_improvement_v2/results/heldout_9arm_20260802/
        <arm>.heldout.json  ->  dev_mean (tuned games) and board_5x5.mean;
        control.heldout.json board_5x5 is {"na": true, "reason": "move-1
        crash: IndexError: tuple index out of range"}.
        _baselines.json     ->  greedy dev_mean 4450.8, board_5x5 80424.8;
                                random dev_mean 1231.4, board_5x5 8196.16.
        redo_5x5.json       ->  truncation-free 180 s re-score, used for
                                nietzsche-sm (492031.2) and nietzsche-radical
                                (723300.4); their raw 60 s-cap numbers were
                                503113.76 and 788405.36 with 6% / 36% of games
                                truncated (see the 9-arm report, section 7).
        control-sm's 234918.16 is a lower bound: 45 of its 50 games truncated.
Arm names map to the post's words: anti = overfitter, nietzsche = expansive,
control = cautious; no suffix = frozen, -sm = bounded, -radical = radical.

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
    "font.size": 12, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.labelsize": 11.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "legend.frameon": False, "figure.facecolor": "white",
    "axes.facecolor": "white", "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join(OUT, "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    os.remove(png)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# --- data (verified against the JSON above) --------------------------------
# (disposition, self-mod level, tuned score, 5x5 score or None = crashed,
#  is-overfitter, mark)
ROWS = [
    ("overfitter", "bounded", 82400, 5092, True, ""),     # anti-sm
    ("overfitter", "frozen", 78989, 5510, True, ""),      # anti
    ("expansive", "bounded", 77204, 492031, False, ""),   # nietzsche-sm
    ("expansive", "frozen", 76625, 36965, False, ""),     # nietzsche
    ("cautious", "bounded", 71116, 234918, False, "*"),   # control-sm
    ("cautious", "frozen", 70413, None, False, ""),       # control
    ("overfitter", "radical", 66473, 4802, True, ""),     # anti-radical
    ("cautious", "radical", 64639, 358431, False, ""),    # control-radical
    ("expansive", "radical", 61772, 723300, False, ""),   # nietzsche-radical
]
GREEDY_DEV, RANDOM_5X5, GREEDY_5X5 = 4451, 8196, 80425

fig, (axt, axb) = plt.subplots(
    2, 1, figsize=(11.4, 8.6), sharex=True,
    gridspec_kw={"height_ratios": [1.0, 1.08], "hspace": 0.16})

xs = list(range(len(ROWS)))
cols = [RED if r[4] else BLUE for r in ROWS]

# ---- top: every condition, scored on the games it tuned against
axt.bar(xs, [r[2] for r in ROWS], width=0.66, zorder=3, color=cols)
for x, r in zip(xs, ROWS):
    axt.text(x, r[2] + 1400, "{:,}".format(r[2]), ha="center", va="bottom",
             fontsize=10, color=INK, zorder=4)
axt.axhline(GREEDY_DEV, color=INK, lw=1.4, ls="--", zorder=4)
axt.text(1.008, GREEDY_DEV, "greedy\nbaseline\n{:,}".format(GREEDY_DEV),
         transform=axt.get_yaxis_transform(), ha="left", va="center",
         fontsize=10, color=INK, linespacing=1.35, zorder=5)
axt.set_ylim(0, 97000)
axt.set_yticks([0, 20000, 40000, 60000, 80000])
axt.set_yticklabels(["0", "20k", "40k", "60k", "80k"])
axt.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axt.set_axisbelow(True)
for s in ("top", "right"):
    axt.spines[s].set_visible(False)
axt.tick_params(length=3, width=0.8)
axt.set_title("Score on the 4x4 games it tuned against", loc="left", pad=10)
axt.set_ylabel("Score")

# ---- bottom: the same nine solvers on a board they never saw
BOT = 3000
for x, r in zip(xs, ROWS):
    v = r[3]
    if v is None:
        axb.text(x, BOT * 1.08, "crashes\non 5x5", ha="center", va="bottom",
                 fontsize=10, color=MUTED, linespacing=1.35, style="italic",
                 zorder=4)
        continue
    axb.bar([x], [v - BOT], width=0.66, bottom=BOT, zorder=3,
            color=RED if r[4] else BLUE)
    axb.text(x, v * 1.08, "{:,}{}".format(v, r[5]), ha="center", va="bottom",
             fontsize=10, color=INK, zorder=4)
axb.axhline(RANDOM_5X5, color=INK, lw=1.4, ls=":", zorder=4)
axb.text(1.008, RANDOM_5X5, "random\nplay\n{:,}".format(RANDOM_5X5),
         transform=axb.get_yaxis_transform(), ha="left", va="center",
         fontsize=10, color=INK, linespacing=1.35, zorder=5)
axb.axhline(GREEDY_5X5, color=INK, lw=1.4, ls="--", zorder=4)
axb.text(1.008, GREEDY_5X5, "greedy\nbaseline\n{:,}".format(GREEDY_5X5),
         transform=axb.get_yaxis_transform(), ha="left", va="center",
         fontsize=10, color=INK, linespacing=1.35, zorder=5)
axb.set_yscale("log")
axb.set_ylim(BOT, 3.0e6)
axb.set_yticks([10000, 100000, 1000000])
axb.set_yticklabels(["10k", "100k", "1M"])
axb.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axb.set_axisbelow(True)
for s in ("top", "right"):
    axb.spines[s].set_visible(False)
axb.tick_params(length=3, width=0.8)
axb.set_title("Score on an unseen 5x5 board (log scale)", loc="left", pad=10)
axb.set_ylabel("Score")
axb.set_xticks(xs)
axb.set_xticklabels(["%s\n%s" % (r[0], r[1]) for r in ROWS], fontsize=9.5,
                    linespacing=1.45)
axb.set_xlim(-0.7, len(ROWS) - 0.3)

axb.text(0.0, -0.20,
         "red = the three runs told to optimize only what is measured. The two "
         "panels have different scales:\nthe 5x5 board is bigger, so every "
         "policy scores higher there, and the axis is logarithmic.\n"
         "*cautious bounded is a lower bound (45 of its 50 games hit the CPU "
         "cap). The two expansive self-modifying\nruns are re-scored at a "
         "3-minute cap to remove the same truncation.",
         transform=axb.transAxes, fontsize=10, color=MUTED,
         linespacing=1.5, va="top")

save(fig, "tuned-vs-heldout")
