"""Figures for "An agent tied a famous benchmark on its first try".

Three figures. Two are cropped out of the source report (see extract_*() at
the bottom of this file); the third is redrawn here:

  packings-26-per-run.webp   report Figure 1, the six N=26 packings
  packing-old-vs-new.webp    redrawn below, the N=27 record before and after
  n27-emergence.webp         report Figure 2, when the N=27 win first appears

The redrawn one has three panels: the previous N=27 record arrangement, the
new one, and where the 0.000629 gain actually came from.

Coordinates are verbatim (x, y, r) triples from the circle-packing-sota repo,
pasted in so this script needs no network and no checkout:

  PREV  writeup/prev_n27_record.json          sum_radii 2.685350025201274
        our own solver's packing at the previously listed Packomania csqv
        record for N=27 (2.685350025228, D. W. Cantrell, 2011/12). Cantrell's
        coordinates were never published, so this stands in at the same total.
  NEW   sota/ours/wins/csqv27.seed1.json      sum_radii 2.685978684198309
        the packing that now holds the listed record.

  gain = 2.685978684198309 - 2.685350025201274 = +6.286589970e-4  (+0.023%)

This is the VARIABLE-radius problem (circles may differ in size); the
equal-circle problem at N=27 is a different, proven-optimal question.

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
from matplotlib.patches import Circle, Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
INK, MUTED = "#1a202c", "#4a5568"
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 13, "axes.titleweight": "bold",
    "axes.labelsize": 11, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
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
REPORTS = "<research-repo>/self_improvement_v2/reports"
SOTA_REPORT = "circle-packing/2026-08-02_circle-packing_sota-comparison_report.pdf"


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


def extract_packings_26():
    """Figure 1 of the sota-comparison report: the six final N=26 packings.

    The post's headline is that five of six runs reached the best known value,
    and this is the artifact that shows it: five identical optimal packings
    (identical up to reflection and relabelling) and one visibly different,
    slightly worse local optimum at 2.6310936. No redrawing of ours conveys
    "the same arrangement, five times" as directly as the packings do.

    Cropped to the figure's own title plus the six panels; the LaTeX caption
    underneath is excluded. Panel labels are the report's internal condition
    names (control / nietzsche x frozen / -sm / radical), kept as they are.
    """
    extract(SOTA_REPORT, 3, (88.32, 313.44, 523.20, 624.00),
            "packings-26-per-run")


def extract_n27_emergence():
    """Figure 2 of the sota-comparison report (Appendix B).

    Each of the run's ten solver versions re-run on N=27 at 120 s/seed over 50
    seeds. Top: best-of-50, seed 1 alone, and the 50-seed spread, against the
    Packomania record. Bottom: the share of the 50 seeds that beat the record.

    This is the figure behind the report's verdict that self-improvement did
    not create the N=27 capability: iteration 1's solver already beat the
    record on 10% of seeds, and iterations 2 to 10 moved that only to 14%.

    Cropped to both stacked panels; the LaTeX caption underneath is excluded.
    """
    extract(SOTA_REPORT, 8, (96.00, 182.40, 515.04, 501.12), "n27-emergence")


# --- data (verified; see the module docstring for provenance) --------------
PREV = [
    (0.105552726975, 0.745173174992, 0.105552726974),
    (0.074022553020, 0.303325413485, 0.074022553019),
    (0.637018059857, 0.240740549294, 0.086437716410),
    (0.896687327255, 0.662896510232, 0.103312672744),
    (0.882888421164, 0.882888421164, 0.117111578835),
    (0.759259450706, 0.362981940143, 0.086437716410),
    (0.495297658963, 0.863039488320, 0.136960511679),
    (0.783757808733, 0.216242191267, 0.062332991210),
    (0.707338775342, 0.747994509805, 0.104279580585),
    (0.906519810926, 0.466349435139, 0.093480189073),
    (0.914041734837, 0.287068706895, 0.085958265162),
    (0.252005490195, 0.292661224658, 0.104279580585),
    (0.318283190743, 0.681716809257, 0.116440427349),
    (0.075860262747, 0.924139737253, 0.075860262746),
    (0.117111578836, 0.117111578836, 0.117111578835),
    (0.712931293105, 0.085958265163, 0.085958265162),
    (0.337103489768, 0.103312672745, 0.103312672744),
    (0.582967988453, 0.417032011547, 0.097953416461),
    (0.535937283088, 0.619521093303, 0.109925672137),
    (0.453757382151, 0.268501593697, 0.098913710828),
    (0.254826825008, 0.894447273025, 0.105552726974),
    (0.380478906697, 0.464062716912, 0.109925672137),
    (0.899147427456, 0.100852572544, 0.100852572543),
    (0.533650564861, 0.093480189074, 0.093480189073),
    (0.136960511680, 0.504702341037, 0.136960511679),
    (0.696674586515, 0.925977446980, 0.074022553019),
    (0.731498406303, 0.546242617849, 0.098913710828),
]

NEW = [
    (0.101538679591, 0.754863942626, 0.101538679590),
    (0.101283795041, 0.331844334409, 0.101283795040),
    (0.612785473469, 0.253941521559, 0.094238245564),
    (0.905179664650, 0.675172044653, 0.094820335349),
    (0.884485966121, 0.884485966121, 0.115514033878),
    (0.746058478441, 0.387214526531, 0.094238245564),
    (0.456778762441, 0.889715341020, 0.110284658979),
    (0.771480365395, 0.228519634605, 0.066479958319),
    (0.579411938530, 0.709646165529, 0.107577232683),
    (0.906026589985, 0.486380198944, 0.093973410014),
    (0.909774060095, 0.302218973441, 0.090225939904),
    (0.251535731217, 0.244979224082, 0.072270783453),
    (0.331320354792, 0.668679645208, 0.143873934957),
    (0.072975385227, 0.927024614773, 0.072975385226),
    (0.115514033879, 0.115514033879, 0.115514033878),
    (0.697781026559, 0.090225939905, 0.090225939904),
    (0.324827955347, 0.094820335350, 0.094820335349),
    (0.530013271746, 0.469986728254, 0.137120282944),
    (0.755020775918, 0.748464268783, 0.072270783453),
    (0.420837802360, 0.261892875849, 0.097874045762),
    (0.245136057374, 0.898461320409, 0.101538679590),
    (0.290353834471, 0.420588061470, 0.107577232683),
    (0.893673197679, 0.106326802321, 0.106326802320),
    (0.513619801056, 0.093973410015, 0.093973410014),
    (0.110284658980, 0.543221237559, 0.110284658979),
    (0.668155665591, 0.898716204959, 0.101283795040),
    (0.738107124151, 0.579162197640, 0.097874045762),
]

r_prev = sorted((c[2] for c in PREV), reverse=True)
r_new = sorted((c[2] for c in NEW), reverse=True)
SUM_PREV, SUM_NEW = sum(r_prev), sum(r_new)
GAIN = SUM_NEW - SUM_PREV
DELTAS = [b - a for a, b in zip(r_prev, r_new)]
assert len(PREV) == len(NEW) == 27
assert abs(sum(DELTAS) - GAIN) < 1e-15

fig, (axl, axm, axr) = plt.subplots(
    1, 3, figsize=(13.4, 4.4),
    gridspec_kw={"width_ratios": [1.15, 1.15, 1.35], "wspace": 0.30})


def draw_packing(ax, circles, title, total):
    """One packing. Fill darkness tracks radius, so the size spread reads."""
    rs = [c[2] for c in circles]
    lo, hi = min(rs), max(rs)
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, lw=1.6, ec=MUTED,
                           zorder=2))
    for x, y, r in circles:
        shade = 0.16 + 0.46 * (r - lo) / (hi - lo)
        ax.add_patch(Circle((x, y), r, facecolor=BLUE, alpha=shade,
                            edgecolor=BLUE, lw=0.9, zorder=3))
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal", adjustable="box", anchor="N")
    ax.axis("off")
    ax.set_title(title, loc="center", pad=10)
    ax.text(0.5, -0.045, "sum of radii  %.6f" % total, transform=ax.transAxes,
            ha="center", va="top", fontsize=11.5, color=INK)


draw_packing(axl, PREV, "The 2011/12 record, reproduced", SUM_PREV)
draw_packing(axm, NEW, "The agent's packing", SUM_NEW)

# --- right: where the gain came from
xs = range(1, len(DELTAS) + 1)
axr.bar(xs, DELTAS, width=0.72, zorder=3,
        color=[BLUE if d >= 0 else ORANGE for d in DELTAS])
axr.axhline(0, color=MUTED, lw=1.0, zorder=4)
axr.axhline(GAIN, color=RED, lw=1.4, ls="--", zorder=5)
axr.annotate("the 27 changes add up\nto just +0.00063",
             xy=(6.0, GAIN), xytext=(6.0, 0.0090),
             ha="left", va="top", fontsize=11, color=RED, zorder=6,
             arrowprops=dict(arrowstyle="-", color=RED, lw=1.0,
                             shrinkA=4, shrinkB=1))
axr.set_xlim(0.3, 27.7)
axr.set_ylim(-0.0085, 0.0095)
axr.set_yticks([-0.008, -0.004, 0, 0.004, 0.008])
axr.set_yticklabels(["-0.008", "-0.004", "0", "+0.004", "+0.008"])
axr.set_xticks([1, 5, 10, 15, 20, 25])
axr.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axr.set_axisbelow(True)
for s in ("top", "right"):
    axr.spines[s].set_visible(False)
axr.tick_params(length=3, width=0.8)
axr.set_title("Nearly every radius changed", loc="center", pad=10)
axr.set_ylabel("New radius minus old radius")
axr.set_xlabel("the 27 radii of each packing, largest to smallest", labelpad=6)

fig.text(0.045, 1.045,
         "A 27-circle packing record from 2011/12, beaten by 0.023%",
         ha="left", va="bottom", fontsize=16.5, fontweight="bold", color=INK)
fig.text(0.045, 0.975,
         "Circles may be any size. The score is the sum of all 27 radii, "
         "and bigger is better.",
         ha="left", va="bottom", fontsize=12, color=MUTED)
fig.text(0.045, -0.130,
         "The 2011/12 coordinates were never published, so the left panel, and "
         "the \"old\" side of the bar chart, is our own solver's\npacking at "
         "that record's total. The bars line the two packings' radii up by "
         "size, not circle by circle.",
         ha="left", va="bottom", fontsize=10.5, color=MUTED, linespacing=1.5)

save(fig, "packing-old-vs-new")
extract_packings_26()
extract_n27_emergence()
