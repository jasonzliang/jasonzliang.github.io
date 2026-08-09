"""Figures for "Our AI judges said landslide. The humans said 56%."

Figure 1 (human-vs-machine): a modest human preference next to a decisive
machine verdict, on the same two systems and the same five challenges. Not on
identical stimuli: per caesar.pdf Appendix I.1, the human raters compared
LLM-normalized two-paragraph summaries (2-3 sentence core idea + 3-4 sentence
argument), while the LLM judges scored the full answers.

Figure 2 (human-by-challenge): the same 112 votes broken out by challenge,
per caesar.pdf Table 12. The aggregate 56.25% is an average over a split:
Caesar wins three challenges and loses two, both by wide margins.

Cliff's delta here is computed over the 5 per-challenge means, so 1.00 means
strict dominance (worst Caesar challenge mean above best baseline mean), NOT
"every Caesar answer beat every competing answer".

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import stats  # noqa: E402

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
    png = os.path.join("/tmp", "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# --- data (verified) -------------------------------------------------------
# Sources, all caesar/paper/caesar.pdf unless noted:
#   63 of 112, 56.25%, "odds ratio 1.29"      - Sec 4.1 and Table 12 (App I).
#     (1.29 is 63/49, i.e. the odds, not an odds ratio.)
#   Raters saw LLM-NORMALIZED two-paragraph summaries, not full answers
#     - App I.1. The LLM judges scored the full answers - Table 1.
#   Per-challenge counts                      - Table 12.
#   Caesar tops all five challenges on the automated full-answer eval
#     - App C.1 / Table 5.
#   The matching automated effect size is Table 1's full-answer row for
#     Gemini 3 (Deep): delta = 0.84. (The paper's "delta >= 0.76" is the
#     minimum over ALL baselines and formats, a different, weaker claim.)
#   0.47 is the large-effect threshold, Table 1 caption.
#   n = 5 challenges per group for the delta   - App B.5.
WINS, N = 63, 112
DELTA = 0.84       # Caesar vs Gemini 3 (Deep), full answers
LARGE = 0.47       # threshold for a "large" effect

# Table 12: (label, Caesar votes, Gemini 3 votes)
CHALLENGES = [
    ("C1  Constrained\n      synthesis", 5, 18),
    ("C2  Counterfactual\n      reasoning", 18, 5),
    ("C3  Cross-domain\n      synthesis", 20, 2),
    ("C4  Meta-\n      creativity", 13, 9),
    ("C5  Open-ended\n      synthesis", 7, 15),
]
assert sum(c for _, c, _ in CHALLENGES) == WINS
assert sum(c + g for _, c, g in CHALLENGES) == N

pct = 100.0 * WINS / N
lo, hi = stats.binomtest(WINS, N, 0.5).proportion_ci(
    confidence_level=0.95, method="exact")
lo, hi = lo * 100, hi * 100
print("share %.2f%%  95%% CI %.2f-%.2f" % (pct, lo, hi))


# =========================================================================
# Figure 1: the two verdicts side by side
# =========================================================================
fig, (axl, axr) = plt.subplots(
    1, 2, figsize=(11.0, 4.1), gridspec_kw={"width_ratios": [1.35, 1.0],
                                            "wspace": 0.24})

# ---- left: what the people preferred
# Coin-flip line stops above the footnote so it does not strike through it.
axl.plot([50, 50], [-0.24, 0.82], color=INK, lw=1.5, ls="--", zorder=2)
axl.text(49.2, 0.60, "a coin flip", ha="right", va="bottom", fontsize=11,
         color=INK)

axl.plot([lo, hi], [0, 0], color=BLUE, lw=3.5, solid_capstyle="round", zorder=3)
for x in (lo, hi):
    axl.plot([x, x], [-0.11, 0.11], color=BLUE, lw=2.2, zorder=3)
axl.plot([pct], [0], "o", ms=13, color=BLUE, zorder=4)

axl.text(pct, 0.20, "%.2f%%" % pct, ha="center", va="bottom", fontsize=14,
         fontweight="bold", color=BLUE)
axl.text(35.5, -0.30,
         "63 of 112 votes, on normalized summaries.\n"
         "The interval still includes a coin flip, and it\n"
         "assumes 112 independent votes: they are 21\n"
         "raters on 5 pairs, so the real one is wider.",
         ha="left", va="top", fontsize=10.5, color=MUTED)
axl.text(hi + 1.2, 0, "95%% confidence:\n%.0f%% to %.0f%%" % (lo, hi),
         ha="left", va="center", fontsize=10.5, color=MUTED)

axl.set_xlim(35, 78)
axl.set_xticks([40, 50, 60, 70])
axl.set_xticklabels(["40%", "50%", "60%", "70%"])
axl.set_ylim(-0.86, 0.85)
axl.set_yticks([])
axl.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axl.set_axisbelow(True)
for s in ("top", "right", "left"):
    axl.spines[s].set_visible(False)
axl.tick_params(axis="x", length=3, width=0.8)
axl.set_title("What the human raters preferred", loc="left", pad=12)
axl.set_xlabel("Share of head-to-heads won by the system", labelpad=8)

# ---- right: what the automated evaluation said
axr.barh([0], [DELTA], height=0.34, color=ORANGE, zorder=3)
axr.axvline(0, color=INK, lw=1.5, zorder=4)
axr.text(DELTA + 0.03, 0, "%.2f" % DELTA, ha="left", va="center",
         fontsize=14, fontweight="bold", color=ORANGE)

# Threshold line stops above the footnote so it does not strike through it.
axr.plot([LARGE, LARGE], [-0.24, 0.82], color=INK, lw=1.5, ls="--", zorder=5)
axr.text(LARGE - 0.02, 0.58, "a large effect\nstarts here", ha="right",
         va="bottom", fontsize=11, color=INK)
axr.text(0.02, -0.30, "The same two systems and challenges, scored\n"
         "by the machine on the full answers instead.\n"
         "One number over 5 challenge means, and the\n"
         "paper reports no interval around it.",
         ha="left", va="top", fontsize=10.5, color=MUTED)

axr.set_xlim(0, 1.12)
axr.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
axr.set_xticklabels(["0", "0.25", "0.50", "0.75", "1.00"])
axr.set_ylim(-0.86, 0.85)
axr.set_yticks([])
axr.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axr.set_axisbelow(True)
for s in ("top", "right", "left"):
    axr.spines[s].set_visible(False)
axr.tick_params(axis="x", length=3, width=0.8)
axr.set_title("What the automated scorer concluded", loc="left", pad=12)
axr.set_xlabel("Cliff's delta over the 5 challenge means: 1.00 = strict "
               "dominance", labelpad=8)

save(fig, "human-vs-machine")


# =========================================================================
# Figure 2: the same 112 votes, by challenge
# =========================================================================
fig2, ax = plt.subplots(figsize=(11.0, 3.6))

ys = list(range(len(CHALLENGES)))[::-1]
for y, (label, cw, gw) in zip(ys, CHALLENGES):
    share = 100.0 * cw / (cw + gw)
    col = BLUE if share > 50 else RED
    ax.barh([y], [share - 50], left=50, height=0.52, color=col, zorder=3)
    # Always "our agent's votes of the votes cast", so the label never has to
    # be read in the light of which side won.
    lab = "%d of %d" % (cw, cw + gw)
    if share > 50:
        ax.text(share + 1.2, y, lab, ha="left", va="center",
                fontsize=11, fontweight="bold", color=col)
    else:
        ax.text(share - 1.2, y, lab, ha="right", va="center",
                fontsize=11, fontweight="bold", color=col)

ax.axvline(50, color=INK, lw=1.5, ls="--", zorder=4)
ax.axvline(pct, color=GREY, lw=1.5, zorder=4)
ax.text(pct + 0.8, len(CHALLENGES) - 0.35, "overall 56.25%", ha="left",
        va="center", fontsize=10.5, color=MUTED)
ax.text(49.0, len(CHALLENGES) - 0.35, "a coin flip", ha="right", va="center",
        fontsize=10.5, color=INK)

ax.set_yticks(ys)
ax.set_yticklabels([c[0] for c in CHALLENGES], fontsize=10.5)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_ylim(-0.75, len(CHALLENGES) - 0.1)
ax.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=3, width=0.8)
ax.set_title("The same 112 votes, split by challenge", loc="left", pad=12)
ax.set_xlabel("Share of the votes cast on that challenge that preferred our "
              "agent. Blue: it won. Red: it lost.", labelpad=8)

save(fig2, "human-by-challenge")
