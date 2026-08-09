"""Figures for "An agent that illustrates its own research".

1. `generated.webp` -- the illustration the run produced, re-encoded.
2. `funnel.webp`    -- one square per scraped candidate image: never scored,
   scored, kept.
3. `provenance.webp` -- the illustration with each region matched BY HAND to
   the reference whose caption shows up in that part of the prompt. The run
   records captions and the prompt; it does not record regions.

Everything is read from the run's own provenance sidecar, so the counts,
scores, captions and source URLs are the ones the pipeline recorded:

    caesar/result/05-13-26_nano_q-920e2951_t-30/generated_image.png.provenance.json

The one number not in the sidecar is SCORED (60): it comes from the run's
console log, `__rome__/agent_CaesarExplorer.console.log`, which reads
"Scraped 343 candidate images from 20 cited URLs / Scoring 60 candidate
images via VLM...". Which 60 of the 343 were sampled is not recorded, so the
funnel scatters them.

The four reference photographs are deliberately NOT republished here. Two are
Wikimedia Commons files and two are stock photographs on a commercial site;
the figure names and links them instead of copying them.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import json
import os
import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREEN, PURPLE = "#2b6cb0", "#dd6b20", "#2f855a", "#6b46c1"
GREY, INK, MUTED = "#cbd5e0", "#1a202c", "#4a5568"
OUT = os.path.dirname(os.path.abspath(__file__))

RUN = ("/Users/jason/Desktop/rome/caesar/result/"
       "05-13-26_nano_q-920e2951_t-30")
SRC_IMG = os.path.join(RUN, "generated_image.png")
SRC_JSON = SRC_IMG + ".provenance.json"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "text.color": INK, "axes.labelcolor": INK,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join("/tmp", "_illus_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


if not os.path.exists(SRC_JSON):
    raise SystemExit("run artifacts not found: %s" % SRC_JSON)

prov = json.load(open(SRC_JSON))
CANDIDATES = prov["candidate_count"]      # 343
PAGES = prov["cited_urls_scraped"]        # 20
REFS = prov["references"]                 # 4, each with url/alt/score/caption
assert len(REFS) == 4, len(REFS)
SCORED = 60                               # from the console log, not the sidecar


# ----------------------------------------------------------------- 1. figure
im = Image.open(SRC_IMG).convert("RGB")
im.save(os.path.join(OUT, "generated.webp"), "WEBP", quality=86, method=6)
print("%s/generated.webp" % OUT)


# ------------------------------------------------------------------ 2. funnel
# Three states per candidate: never scored, scored but not kept, kept. The four
# kept are drawn last so they read as a block; the scored-not-kept cells are
# scattered because the run does not record WHICH 60 it sampled.
COLS = 26
rows = -(-CANDIDATES // COLS)
KEPT_FROM = CANDIDATES - len(REFS)     # the four survivors sit last
PALE, MID = "#e2e8f0", "#93a7bf"

random.seed(20260513)
scored_only = set(random.sample(range(KEPT_FROM), SCORED - len(REFS)))

fig, ax = plt.subplots(figsize=(9.6, 4.8))
kept_cells = []
for k in range(CANDIDATES):
    r, c = divmod(k, COLS)
    y = rows - 1 - r
    if k >= KEPT_FROM:
        colour = BLUE
        kept_cells.append((c, y))
    elif k in scored_only:
        colour = MID
    else:
        colour = PALE
    ax.add_patch(mpatches.Rectangle(
        (c, y), 0.78, 0.78, facecolor=colour, edgecolor="none"))

ax.set_xlim(-0.6, COLS + 0.4)
ax.set_ylim(-2.6, rows + 0.5)
ax.set_aspect("equal")
ax.axis("off")

# point at the survivors wherever the grid actually put them
kx = sum(c for c, _ in kept_cells) / float(len(kept_cells)) + 0.4
ky = kept_cells[0][1]
ax.annotate("these four", xy=(kx + 2.4, ky + 0.35), xytext=(kx + 6.2, ky + 0.35),
            fontsize=12.5, fontweight="bold", color=BLUE,
            ha="left", va="center",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.4))

# legend, at fixed columns so long labels can't run into the next swatch
for lx, colour, label in (
        (0.0, PALE, "%d never scored" % (CANDIDATES - SCORED)),
        (8.0, MID, "%d scored, not kept" % (SCORED - len(REFS))),
        (17.0, BLUE, "%d kept as references" % len(REFS))):
    ax.add_patch(mpatches.Rectangle((lx, -1.65), 0.78, 0.78,
                                    facecolor=colour, edgecolor="none"))
    ax.text(lx + 1.05, -1.26, label, fontsize=10.5, color=MUTED, va="center")

ax.text(0, -2.45,
        "Which 60 the run scored is not recorded, so the scored cells are "
        "scattered rather than located.",
        fontsize=10, color=MUTED, va="center")

ax.text(0, rows + 0.05,
        "%d images left after the scrape filters, from the %d pages the "
        "report cited" % (CANDIDATES, PAGES),
        fontsize=12.5, color=MUTED, ha="left", va="bottom")
ax.set_title("343 candidates, 60 looked at, 4 used", pad=30)
save(fig, "funnel")


# -------------------------------------------------------------- 3. provenance
# Regions of the 1024x1024 illustration, in pixels, matched by eye to the
# reference each one derives from. Ordered as REFS is.
BOXES = [
    (296, 4, 530, 250),      # branching ribs and circular skylights
    (6, 652, 358, 368),      # the annotated inset panel
    (628, 322, 272, 286),    # lattice canopy towers
    (910, 168, 112, 470),    # green-clad high-rises
]
# where each number chip sits inside its box, so none covers artwork that the
# caption asks the reader to look at
CHIP = ["tl", "tr", "tl", "tl"]
COLOURS = [ORANGE, GREEN, BLUE, PURPLE]
WHAT = [
    "the branching ribs and circular skylights",
    "the annotated inset panel",
    "the lattice canopy towers",
    "the green-clad high-rises",
]


def source_of(url):
    if "wikimedia" in url or "wikipedia" in url:
        return "Wikimedia Commons"
    return url.split("/")[2].replace("www.", "")


def subject_of(url):
    name = url.rstrip("/").split("/")[-1]
    name = name.rsplit(".", 1)[0].replace("250px-", "")
    name = name.replace("%28", "(").replace("%29", ")")
    return name.replace("_", " ").replace("-", " ").strip()


fig = plt.figure(figsize=(11.6, 5.3))
axi = fig.add_axes([0.0, 0.0, 0.42, 1.0])
axl = fig.add_axes([0.45, 0.0, 0.55, 1.0])

axi.imshow(im)
axi.axis("off")
for n, ((x, y, w, h), colour, chip) in enumerate(zip(BOXES, COLOURS, CHIP), 1):
    axi.add_patch(mpatches.Rectangle((x, y), w, h, fill=False,
                                     edgecolor=colour, linewidth=3.0))
    cx, ha = (x + 13, "left") if chip.endswith("l") else (x + w - 13, "right")
    axi.text(cx, y + 13, str(n), fontsize=13, fontweight="bold",
             color="white", va="top", ha=ha,
             bbox=dict(boxstyle="square,pad=0.30", facecolor=colour,
                       edgecolor="none"))

axl.axis("off")
axl.set_xlim(0, 1)
axl.set_ylim(0, 1)
axl.text(0, 0.97, "Where each region came from, matched by eye", fontsize=14,
         fontweight="bold", va="top")

y = 0.845
for n, (ref, colour, what) in enumerate(zip(REFS, COLOURS, WHAT), 1):
    axl.text(0.012, y, str(n), fontsize=12.5, fontweight="bold", color="white",
             va="center", ha="center",
             bbox=dict(boxstyle="square,pad=0.34", facecolor=colour,
                       edgecolor="none"))
    axl.text(0.062, y + 0.032, what, fontsize=12.5, fontweight="bold",
             va="center", color=INK)
    axl.text(0.062, y - 0.032,
             "%s   %s   relevance %.1f"
             % (subject_of(ref["url"])[:38], source_of(ref["url"]),
                ref["score"]),
             fontsize=10.5, va="center", color=MUTED)
    y -= 0.155

axl.text(0, 0.285,
         "The boxes are drawn by hand. The run records each reference's caption\n"
         "and the prompt written from them; which pixels a phrase became is my\n"
         "eye, not the pipeline's bookkeeping.",
         fontsize=10.5, va="top", color=MUTED, linespacing=1.5)

axl.text(0, 0.135,
         "The reference photographs are not reproduced here: two Wikimedia\n"
         "Commons files and two stock images on a commercial site. The agent\n"
         "looked at them, this figure only names them.",
         fontsize=10.5, va="top", color=MUTED, linespacing=1.5)

save(fig, "provenance", quality=84)


# ---------------------------------------------------------------- 4. gallery
# Four more runs put through the same pipeline, one per research question.
# Images and sidecars are in `_source/`; every number below is read from the
# sidecar, not typed. The point of the figure is that one pipeline, unchanged,
# produces four completely different visual registers, and that one of the four
# found nothing good enough to look at and fell back to text only.
GALLERY = [
    ("04030533", "A recipe calculus for cooking"),
    ("04030524", "Echolocation instead of colour vision"),
    ("04030527", "Invent a business idea that does not exist"),
    ("04030532", "How would you score creativity itself"),
]
SRC_DIR = os.path.join(OUT, "_source")


def _sidecar(stamp):
    for f in os.listdir(SRC_DIR):
        if stamp in f and f.endswith(".webp.json"):
            return json.load(open(os.path.join(SRC_DIR, f))), \
                os.path.join(SRC_DIR, f[:-5])
    raise SystemExit("no sidecar for %s" % stamp)


fig, axes = plt.subplots(2, 2, figsize=(11.4, 7.0))
for ax, (stamp, question) in zip(axes.ravel(), GALLERY):
    meta, img_path = _sidecar(stamp)
    ax.imshow(Image.open(img_path).convert("RGB"))
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_edgecolor("#e2e8f0")
        s.set_linewidth(1.0)

    refs = meta["refs_passed_to_api"]
    top = max([r["score"] for r in meta["picked_pool"]] or [0.0])
    if refs:
        note = "%d of %d scraped images used as visual references" % (
            refs, meta["candidate_count"])
        colour = INK
    else:
        # The 7.0 gate is use_refs_top_score; it is applied to the BEST
        # surviving reference, not to the set.
        note = ("best of %d scraped images scored %.1f, under the 7.0 gate:\n"
                "drawn from the text alone"
                % (meta["candidate_count"], top))
        colour = ORANGE
    ax.set_title(question, fontsize=12, fontweight="bold", loc="left", pad=8)
    ax.set_xlabel(note, fontsize=10, color=colour, labelpad=7)

fig.suptitle("Same pipeline, same code, four different research reports",
             fontsize=15, fontweight="bold", x=0.005, ha="left", y=0.995)
fig.tight_layout(rect=(0, 0, 1, 0.965))
save(fig, "gallery", quality=82)
