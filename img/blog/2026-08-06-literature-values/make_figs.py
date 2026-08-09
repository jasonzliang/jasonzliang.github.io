"""Figure for "I tried deriving an agent's values from the literature".

The citation ledger: every paper cited by the literature-derived values report,
grouped by the two paper sets, coloured by which hallucination-audit pass
checked it, with the identifier the audit resolved.

Source of every number, every paper name and every ID:
  self_improvement_v2/reports/literature-values/
    2026-08-06_literature-derived-agent-values_report.pdf
  (read with `pdftotext -layout`)

  Section 1, Method and provenance:
    "The initial audit verified 17/17 cited papers real (arXiv ID resolves to
     the claimed title, first author, and year) with 4/4 headline metrics
     verbatim-supported in the abstracts."
    "GPT-4 was added to Part A, and Chain-of-Thought, ReAct, Toolformer, and
     Voyager to Part B; each of these 5 additions passed the same gate 5/5
     (metadata MATCH, with each paper's core contribution quoted verbatim from
     the abstract), for 22/22 cited papers verified real and zero fabricated
     papers or misattributions."
    "Part B contributions are quoted from primary sources; Part A per-paper
     contributions are drawn from established knowledge (plus the verified
     GPT-4 abstract) and marked medium confidence."

  Section 2, Part A top-10 by z-score: Qwen2, Llama 3, GPT-4, MT-Bench,
    Llama 2, Mamba, DPO, LLaMA, Phi-3, RAG survey.  Plus reference [1], the
    NLLG arXiv report the ranking itself comes from  ->  11 papers.

  Section 3, Part B: Chain-of-Thought, ReAct, Toolformer, Voyager, Reflexion,
    Self-Refine, STaR, InstructGPT, Constitutional AI, AlphaZero/AlphaGo Zero
    ("self-play spans two companion papers")  ->  ten entries, 11 papers.

  Sections 4 and 5 headings: "Value Set A ... (medium confidence)" and
    "Value Set B ... (high confidence)".  That asymmetry is the second column
    subtitle on each side.

  References [1]-[22] supply the IDs in the right-hand column.  Twenty-one are
  arXiv IDs; [22] AlphaGo Zero is Nature 550:354-359 and has no arXiv ID, which
  is why the subtitle says "every ID below" rather than "every arXiv ID".

  11 + 11 = 22, matching the 22 numbered references in the report and the
  22/22 audit figure.  The five orange tiles are exactly the five late
  additions named above.  Voyager's dagger is the debate verdict from
  section 1: "Voyager's compound/reuse disposition is folded as a clause into
  the verifier bullet".

Run from THIS directory, never from /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
INK, MUTED = "#1a202c", "#4a5568"
GRID = "#e2e8f0"
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


# --- the ledger.  (label, identifier, second audit pass?) -------------------
PART_A = [
    ("NLLG arXiv ranking report", "2412.12121", False),
    ("Qwen2", "2407.10671", False),
    ("Llama 3", "2407.21783", False),
    ("GPT-4", "2303.08774", True),
    ("MT-Bench / LLM-as-a-Judge", "2306.05685", False),
    ("Llama 2", "2307.09288", False),
    ("Mamba", "2312.00752", False),
    ("DPO", "2305.18290", False),
    ("LLaMA", "2302.13971", False),
    ("Phi-3", "2404.14219", False),
    ("RAG survey", "2312.10997", False),
]
PART_B = [
    ("Chain-of-Thought", "2201.11903", True),
    ("ReAct", "2210.03629", True),
    ("Toolformer", "2302.04761", True),
    ("Voyager  †", "2305.16291", True),
    ("Reflexion", "2303.11366", False),
    ("Self-Refine", "2303.17651", False),
    ("STaR", "2203.14465", False),
    ("InstructGPT", "2203.02155", False),
    ("Constitutional AI", "2212.08073", False),
    ("AlphaZero", "1712.01815", False),
    ("AlphaGo Zero", "Nature 550:354", False),
]

assert len(PART_A) + len(PART_B) == 22
assert sum(1 for _, _, w2 in PART_A + PART_B if w2) == 5
assert len({i for _, i, _ in PART_A + PART_B}) == 22

FIG_W, FIG_H = 10.6, 7.0
fig = plt.figure(figsize=(FIG_W, FIG_H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

TOP = 0.672          # y of the first row's centre
STEP = 0.0530        # row pitch
ROW_H = 0.0435       # row background height
COLS = [0.035, 0.525]
COL_W = 0.440
CHIP_H = 0.0172                     # chip side, in y-units
CHIP_W = CHIP_H * FIG_H / FIG_W     # same side in x-units, so it is square

for x0, header, sub1, sub2, rows in [
    (COLS[0], "Part A: top-cited papers",
     "the window-normalized top ten, plus the ranking report it came from",
     "contributions from established knowledge, GPT-4 aside: "
     "medium confidence",
     PART_A),
    (COLS[1], "Part B: self-improving-agent papers",
     "ten entries; self-play spans two companion papers",
     "contributions quoted from the primary sources: high confidence",
     PART_B),
]:
    ax.text(x0, 0.798, header, ha="left", va="baseline",
            fontsize=13, fontweight="bold", color=INK)
    ax.text(x0, 0.764, sub1, ha="left", va="baseline",
            fontsize=10.5, color=MUTED)
    ax.text(x0, 0.735, sub2, ha="left", va="baseline",
            fontsize=10.0, color=MUTED)
    ax.plot([x0, x0 + COL_W], [0.716, 0.716], color=GRID, lw=1.4,
            solid_capstyle="butt")
    for i, (label, ident, wave2) in enumerate(rows):
        y = TOP - i * STEP
        ax.add_patch(FancyBboxPatch(
            (x0, y - ROW_H / 2), COL_W, ROW_H,
            boxstyle="round,pad=0,rounding_size=0.006",
            linewidth=0, facecolor="#f7fafc", zorder=1))
        col = ORANGE if wave2 else BLUE
        ax.add_patch(FancyBboxPatch(
            (x0 + 0.014, y - CHIP_H / 2), CHIP_W, CHIP_H,
            boxstyle="round,pad=0,rounding_size=0.003",
            linewidth=0, facecolor=col, zorder=2))
        ax.text(x0 + 0.014 + CHIP_W + 0.016, y, label, ha="left", va="center",
                fontsize=11.4, color=INK, zorder=3)
        ax.text(x0 + COL_W - 0.014, y, ident, ha="right", va="center",
                fontsize=10.2, color=MUTED, zorder=3)

# --- title, legend, footer --------------------------------------------------
fig.text(0.035, 0.988, "22 cited papers, 22 verified real, 0 fabricated",
         ha="left", va="top", fontsize=17.5, fontweight="bold", color=INK)
fig.text(0.035, 0.948,
         "An independent audit pass resolved every ID below to the claimed "
         "title, first author and year.",
         ha="left", va="top", fontsize=12, color=MUTED)

for leg_y, col, text in [
    (0.900, BLUE, "first audit pass: 17 / 17 real, and 4 / 4 headline metrics "
                  "verbatim-supported in the abstracts"),
    (0.859, ORANGE, "the five late additions: 5 / 5 real, each paper's core "
                    "contribution quoted verbatim"),
]:
    ax.add_patch(FancyBboxPatch(
        (0.035, leg_y - CHIP_H / 2), CHIP_W, CHIP_H,
        boxstyle="round,pad=0,rounding_size=0.003",
        linewidth=0, facecolor=col, zorder=2))
    ax.text(0.035 + CHIP_W + 0.013, leg_y, text, ha="left", va="center",
            fontsize=11, color=MUTED)

fig.text(0.035, 0.062,
         "†  Voyager was the only late addition a structured debate let "
         "change a value: its compound-and-reuse disposition was folded into "
         "the verifier bullet.",
         ha="left", va="center", fontsize=10.9, color=ORANGE)
fig.text(0.035, 0.022,
         "Zero fabricated papers and zero misattributions across both passes.",
         ha="left", va="center", fontsize=10.9, color=MUTED)

save(fig, "citation-ledger")
