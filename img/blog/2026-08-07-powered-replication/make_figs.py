"""Figures for "I ran it once and got a headline".

Two figures, drawn two different ways:

1. cliffs-delta.webp        redrawn here in matplotlib
   Cliff's delta, expansive (nietzsche) runs against cautious (control) runs,
   on each of the three scored tests. Ten runs per side, pooled across the two
   self-modification levels of the powered arm.

   Numbers from reports/game-2048/2026-08-05_game-2048_powered_report.pdf, exec
   summary: DEV delta=+0.80 p=0.001; p4_25 (harder spawn) delta=+0.60 p=0.024;
   board_5x5 delta=-0.05 p=0.86. p values are exact two-sided permutation
   tests, pre-specified in the study design, which is why they are quoted here.

2. heldout-5x5-per-run.webp cropped out of the report itself
   Panel (B) of that report's Figure 2: the per-run 5x5 scatter that the
   summary above necessarily hides. See extract_heldout_5x5() below.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os
import shutil
import subprocess
import tempfile

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
    "font.size": 12, "axes.titlesize": 15, "axes.titleweight": "bold",
    "axes.labelsize": 11.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 11, "ytick.labelsize": 12,
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


# --- lifting a figure straight out of a report -----------------------------
#
# The report figures are vector art, not embedded rasters, so pdfimages finds
# nothing in these PDFs. The only way out is to render the page and cut.
#
# The reports tree lives outside this repo; set REPORTS to wherever it is.
REPORTS = "/Users/jason/Desktop/science_moonshot/self_improvement_v2/reports"


def extract(pdf, page, box_pt, name, dpi=400, max_width=2000, pad_pt=4.0,
            quality=88):
    """Render one page of a report PDF and crop one figure out of it.

    box_pt is (x0, y0, x1, y1) in PostScript points (72 per inch) measured
    from the top-left corner of the page, so the box stays correct if dpi
    changes. Equivalent by hand:

        pdftoppm -r <dpi> -png -f <page> -l <page> <pdf> /tmp/pg
        crop to (x0, y0, x1, y1) * dpi/72 pixels
    """
    tmp = tempfile.mkdtemp(prefix="reportfig-")
    try:
        subprocess.run(["pdftoppm", "-r", str(dpi), "-png",
                        "-f", str(page), "-l", str(page),
                        os.path.join(REPORTS, pdf), os.path.join(tmp, "pg")],
                       check=True)
        rendered = os.path.join(tmp, sorted(os.listdir(tmp))[0])
        img = Image.open(rendered).convert("RGB")
        s = dpi / 72.0
        x0, y0, x1, y1 = box_pt
        img = img.crop((int((x0 - pad_pt) * s), int((y0 - pad_pt) * s),
                        int((x1 + pad_pt) * s), int((y1 + pad_pt) * s)))
        if img.width > max_width:
            h = int(round(img.height * max_width / float(img.width)))
            img = img.resize((max_width, h), Image.LANCZOS)
        out = os.path.join(OUT, name + ".webp")
        img.save(out, "WEBP", quality=quality, method=6)
        print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def extract_heldout_5x5():
    """Panel (B) of Figure 2 of the powered 2048 report.

    Every one of the thirty runs as its own dot: raw 5x5 board score on a log
    axis, six conditions, with the greedy baseline (80,424) and the random
    floor (8,196) drawn in, and an x for a run that could not play 5x5 at all.
    This is the evidence for the null the redrawn Cliff's delta chart can only
    assert: the within-condition spread is two orders of magnitude, larger
    than any gap between conditions.

    Cropped to panel (B) alone. Panel (A) is the in-distribution capability
    bars, which the post covers with the Cliff's delta chart, and the LaTeX
    caption below the figure is excluded. Condition names are the report's
    own: ctrl = cautious (control), niet = expansive (nietzsche).
    """
    extract("game-2048/2026-08-05_game-2048_powered_report.pdf", 4,
            (280.80, 414.72, 537.60, 579.84), "heldout-5x5-per-run")


# --- data (verified) -------------------------------------------------------
ROWS = [
    ("Games it tuned against", 0.80, "p = 0.001", BLUE),
    ("A harder tile-spawn", 0.60, "p = 0.024", BLUE),
    ("An unseen 5x5 board", -0.05, "p = 0.86", GREY),
]

fig, ax = plt.subplots(figsize=(8.4, 3.4))
ys = range(len(ROWS))

for y, (label, val, pval, colour) in zip(ys, ROWS):
    ax.barh(y, val, height=0.58, color=colour, zorder=3)
    # Long bars carry their label inside, so nothing spills past the +/-1
    # ends of the scale (a Cliff's delta of 1 is the maximum, and a label
    # drawn beyond it reads as if the bar ran off the axis).
    if val >= 0.30:
        ax.text(val - 0.025, y, "+%.2f   %s" % (val, pval), va="center",
                ha="right", fontsize=11.5, color="white", zorder=4)
    elif val >= 0:
        ax.text(val + 0.035, y, "+%.2f   %s" % (val, pval), va="center",
                ha="left", fontsize=11.5, color=INK, zorder=4)
    else:
        ax.text(val - 0.035, y, "%.2f   %s" % (val, pval), va="center",
                ha="right", fontsize=11.5, color=INK, zorder=4)

ax.set_yticks(list(ys))
ax.set_yticklabels([r[0] for r in ROWS])
ax.invert_yaxis()

ax.axvline(0, color=MUTED, lw=1.2, zorder=2)
ax.set_xlim(-1.0, 1.0)
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_xticklabels(["-1", "-0.5", "0", "+0.5", "+1"])
ax.xaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
ax.set_axisbelow(True)

for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", length=3, width=0.8)

fig.text(0.005, 1.19,
         "Disposition changed how good the solver got, with no detectable "
         "effect on generalization",
         ha="left", va="bottom", fontsize=14.5, fontweight="bold", color=INK)
fig.text(0.005, 1.005,
         "Ten expansive runs against ten cautious runs, on each of the three "
         "tests. Undetectable is not the\nsame as absent: the 5x5 scores "
         "vary so much run to run that only a huge effect would show.",
         ha="left", va="bottom", fontsize=11.5, color=MUTED)

ax.set_xlabel(
    "Cliff's delta:  +1 means every expansive run beat every cautious run,\n"
    "0 means the two groups are indistinguishable",
    labelpad=10, fontsize=11, color=MUTED)

save(fig, "cliffs-delta")
extract_heldout_5x5()
