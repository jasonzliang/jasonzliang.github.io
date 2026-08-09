"""Figures for "Why I gave an AI agent Nietzsche".

Two figures:

1. `sandpile.webp` -- not generated here. This is the abelian-sandpile identity
   the standard-values agent itself produced at iteration 44 of its 60-iteration
   run. Copied and re-encoded as WebP. The source is 256x256 flat-colour pixel
   art, so it is upscaled with nearest-neighbour (keeping every cell crisp
   rather than smearing the fractal) and saved losslessly, which is both
   sharper and smaller than lossy WebP for an image with four colours.

2. `two-agents.webp` -- the two measured contrasts between the runs, both
   recounted from the archived workspaces under
   `self_improvement_v1/result/20260616-2346_{original,nietzsche}_30i_30m/`:
     - stdlib-only share of `tools/*.py`, by scanning each module for a
       third-party import: 24 of 27 (original; the three exceptions are
       membrane, moran, sandpile, exactly the three the write-up names) vs
       4 of 36 (nietzsche). The write-up says "~25 of 28 ... vs only 4 of 37";
       it is not self-consistent on either total (26/27/28 and 36/37) and
       neither total matches the disk.
     - WebSearch + WebFetch tool_use records in `runner.log`, bucketed by the
       `[loop] === iteration N/` markers: original 41 (22 search + 19 fetch),
       first at iter30, bursts at iter44 and iter50; nietzsche 1, at iter12.
       The 41 and the 1 match the write-up exactly; the per-iteration split is
       new, and it is why the right-hand panel is titled by the whole run
       rather than by the nudge (the single nietzsche call lands in the same
       iteration window as the nudge, so it is not a post-nudge count).

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE = "#2b6cb0", "#dd6b20"
INK, MUTED = "#1a202c", "#4a5568"
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 14, "axes.titleweight": "bold",
    "axes.labelsize": 11.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 11.5, "ytick.labelsize": 11.5,
    "legend.frameon": False, "legend.fontsize": 11.5,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join("/tmp", "_niet_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


# ---------------------------------------------------------------- 1. sandpile
# <research-repo> is a private tree that is not part of this repo;
# point it at a local checkout to re-run.
SRC = ("<research-repo>/self_improvement_v1/result/"
       "20260616-2346_original_30i_30m/artifacts/"
       "iter44-2026-06-17-abelian-sandpile/identity.png")
SCALE = 3

if os.path.exists(SRC):
    im = Image.open(SRC).convert("RGB")
    im = im.resize((im.width * SCALE, im.height * SCALE), Image.NEAREST)
    out = os.path.join(OUT, "sandpile.webp")
    im.save(out, "WEBP", lossless=True, quality=100, method=6)
    print("%s  %dx%d  (%.0f KB)" % (out, im.width, im.height,
                                    os.path.getsize(out) / 1024.0))
else:
    print("source art not found, keeping existing sandpile.webp: %s" % SRC)


# -------------------------------------------------------------- 2. two agents
fig, (axl, axr) = plt.subplots(1, 2, figsize=(10.6, 3.9),
                               gridspec_kw={"wspace": 0.42})

LABELS = ["Standard\nvalues", "Nietzschean\nvalues"]


def tidy(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(LABELS)
    ax.set_xlim(-0.62, 1.62)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", color="#e2e8f0", linewidth=0.8)
    ax.set_axisbelow(True)


# Left: share of modules that run on a bare Python install.
runs, total = [24, 4], [27, 36]
pct = [100.0 * r / t for r, t in zip(runs, total)]

axl.bar([0, 1], [100, 100], width=0.5, color="#edf2f7", zorder=1)
axl.bar([0, 1], pct, width=0.5, color=[BLUE, ORANGE], zorder=2)
# Both counted from disk (see module docstring), so neither label hedges.
LABELS_L = ["24 of 27", "4 of 36"]
for i, p in enumerate(pct):
    axl.text(i, p + 3.5, LABELS_L[i], ha="center",
             fontsize=13, fontweight="bold", color=[BLUE, ORANGE][i])
axl.set_ylim(0, 116)
axl.set_yticks([0, 25, 50, 75, 100])
axl.set_yticklabels(["0", "25%", "50%", "75%", "100%"])
axl.set_title("Modules that run with no extra install", loc="left", pad=12)
tidy(axl)

# Right: web calls after the identical mid-run nudge.
calls = [41, 1]
axr.bar([0, 1], calls, width=0.5, color=[BLUE, ORANGE], zorder=2)
for i, c in enumerate(calls):
    axr.text(i, c + 1.4, str(c), ha="center", fontsize=15,
             fontweight="bold", color=[BLUE, ORANGE][i])
axr.set_ylim(0, 48)
axr.set_yticks([0, 10, 20, 30, 40])
axr.set_title("Web calls in the whole 60-iteration run", loc="left", pad=12)
tidy(axr)

fig.text(0.0, -0.05,
         "Two 60-iteration runs, identical except for one values file. Both "
         "got the same mid-run nudge to use external sources,\n"
         "at about iteration 12. All 41 of the standard run's calls came "
         "after it, from iteration 30 on; the Nietzschean\nrun's single call "
         "came at iteration 12, and it made no others.",
         fontsize=11.5, color=MUTED, ha="left", va="top", linespacing=1.5)

save(fig, "two-agents")
