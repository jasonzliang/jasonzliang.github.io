"""Figure for "I told an agent to overfit on purpose".

Three stacked panels over the SAME nine conditions in the SAME left-to-right
order, so each condition can be traced between them.

Top:    the tuned-games score (4x4 DEV), linear, with the greedy 1-ply anchor.
Middle: the endpoint designated PRIMARY before the runs launched -- the DEV ->
        held-out drop on fresh same-distribution 4x4 seeds, with +/-1 pooled SE.
        Smaller is better here; the other two panels are larger-is-better.
Bottom: the same nine solvers on an unseen 5x5 board, log scale, against the
        random floor and the greedy 5x5 baseline. This is the endpoint that was
        relabelled primary 12.5 h AFTER the runs started, with results in hand.

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
        results/_eval/g2048-<arm>-20260802/run-*/heldout.json -> the in_dist
        row (role=scale) for the middle panel: score, score_se, and the drop
        DEV - score. n = 5 replicate draws x 20 seeds = 100; the SE is pooled
        across the 5 draw means, so it is the SE of the held-out mean and
        therefore of the drop (the DEV anchor is a single 20-seed draw).
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
    "font.size": 12, "axes.titlesize": 13.5, "axes.titleweight": "bold",
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
# (disposition, self-mod level, tuned score, DEV->held-out drop, drop SE,
#  drop percent, 5x5 score or None = crashed, is-overfitter, mark)
ROWS = [
    # anti-sm      dev=82400.2 ho=71872.44 drop=10527.76 se=3584.21
    ("overfitter", "bounded", 82400, 10528, 3584, 12.8, 5092, True, ""),
    # anti         dev=78989.4 ho=75541.76 drop= 3447.64 se=2251.83
    ("overfitter", "frozen", 78989, 3448, 2252, 4.4, 5510, True, ""),
    # nietzsche-sm dev=77204.4 ho=63396.52 drop=13807.88 se=2788.85
    ("expansive", "bounded", 77204, 13808, 2789, 17.9, 492031, False, ""),
    # nietzsche    dev=76624.6 ho=62506.04 drop=14118.56 se=1406.11
    ("expansive", "frozen", 76625, 14119, 1406, 18.4, 36965, False, ""),
    # control-sm   dev=71115.6 ho=58277.84 drop=12837.76 se=3921.88
    ("cautious", "bounded", 71116, 12838, 3922, 18.1, 234918, False, "*"),
    # control      dev=70413.0 ho=55892.32 drop=14520.68 se=2370.91
    ("cautious", "frozen", 70413, 14521, 2371, 20.6, None, False, ""),
    # anti-radical dev=66473.4 ho=54665.40 drop=11808.00 se=2986.79
    ("overfitter", "radical", 66473, 11808, 2987, 17.8, 4802, True, ""),
    # control-rad  dev=64638.8 ho=57371.32 drop= 7267.48 se=1396.48
    ("cautious", "radical", 64639, 7267, 1396, 11.2, 358431, False, ""),
    # nietzsche-r  dev=61772.2 ho=54011.64 drop= 7760.56 se=2886.13
    ("expansive", "radical", 61772, 7761, 2886, 12.6, 723300, False, ""),
]
GREEDY_DEV, RANDOM_5X5, GREEDY_5X5 = 4451, 8196, 80425

fig, (axt, axm, axb) = plt.subplots(
    3, 1, figsize=(11.4, 14.2), sharex=True,
    gridspec_kw={"height_ratios": [1.0, 0.92, 1.08], "hspace": 0.40})

xs = list(range(len(ROWS)))
cols = [RED if r[7] else BLUE for r in ROWS]

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
axt.set_title("The metric the agents could see: score on the 4x4 games they "
              "tuned against\n(taller is better)", loc="left", pad=10)
axt.set_ylabel("Score")

# ---- middle: the endpoint designated primary BEFORE the runs launched
axm.bar(xs, [r[3] for r in ROWS], width=0.66, zorder=3, color=cols,
        yerr=[r[4] for r in ROWS], ecolor=MUTED,
        error_kw={"lw": 1.1, "capsize": 4, "capthick": 1.1, "zorder": 5})
for x, r in zip(xs, ROWS):
    axm.text(x, r[3] + r[4] + 700, "{:,}".format(r[3]), ha="center",
             va="bottom", fontsize=10, color=INK, zorder=4)
    axm.text(x, r[3] + r[4] + 2500, "{:.1f}%".format(r[5]), ha="center",
             va="bottom", fontsize=9, color=MUTED, zorder=4)
axm.set_ylim(0, 20500)
axm.set_yticks([0, 5000, 10000, 15000])
axm.set_yticklabels(["0", "5k", "10k", "15k"])
axm.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axm.set_axisbelow(True)
for s in ("top", "right"):
    axm.spines[s].set_visible(False)
axm.tick_params(length=3, width=0.8)
axm.set_title("Designated primary 78 minutes before the runs launched: the "
              "drop from the tuned score\nto fresh 4x4 games, "
              "±1 SE (SHORTER is better)", loc="left", pad=10)
axm.set_ylabel("Drop")

# ---- bottom: the same nine solvers on a board they never saw
BOT = 3000
for x, r in zip(xs, ROWS):
    v = r[6]
    if v is None:
        axb.text(x, BOT * 1.08, "crashes\non 5x5", ha="center", va="bottom",
                 fontsize=10, color=MUTED, linespacing=1.35, style="italic",
                 zorder=4)
        continue
    axb.bar([x], [v - BOT], width=0.66, bottom=BOT, zorder=3,
            color=RED if r[7] else BLUE)
    axb.text(x, v * 1.08, "{:,}{}".format(v, r[8]), ha="center", va="bottom",
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
axb.set_title("Relabelled primary 12.5 hours after the runs started, with the "
              "results in hand:\nan unseen 5x5 board, log scale (taller is "
              "better)", loc="left", pad=10)
axb.set_ylabel("Score")
axb.set_xticks(xs)
axb.set_xticklabels(["%s\n%s" % (r[0], r[1]) for r in ROWS], fontsize=9.5,
                    linespacing=1.45)
axb.set_xlim(-0.7, len(ROWS) - 0.3)

axb.text(0.0, -0.24,
         "red = the three runs told to optimize only what is measured. They "
         "take the top two bars in the top panel, the\nshortest bar in the "
         "middle panel, and the bottom three in the panel below it. The three "
         "panels are not on one\nscale: the 5x5 board is bigger, so every "
         "policy scores higher there, and that axis is logarithmic.\n"
         "*cautious bounded is a lower bound (45 of its 50 games hit the CPU "
         "cap). The two expansive self-modifying\nruns are re-scored at a "
         "3-minute cap to remove the same truncation.",
         transform=axb.transAxes, fontsize=10, color=MUTED,
         linespacing=1.5, va="top")

save(fig, "tuned-vs-heldout")
