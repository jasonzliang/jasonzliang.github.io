"""Shared house style for blog figures.

Each post's make_figs.py inlines a copy of this so it runs standalone; this file
is the canonical reference.

House palette (colourblind-safe):
    blue   #2b6cb0   orange #dd6b20   grey #a0aec0   red #c53030

Note on the environment: a stray /tmp/six.py shadows the real `six` package, so
never run these scripts with /tmp as the working directory.
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
INK, MUTED = "#1a202c", "#4a5568"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.labelsize": 11.5,
    "axes.edgecolor": MUTED,
    "axes.linewidth": 0.9,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.frameon": False,
    "legend.fontsize": 11,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def tidy(ax, spines=("top", "right")):
    """Strip chartjunk: drop the named spines and lighten the ticks."""
    for s in spines:
        ax.spines[s].set_visible(False)
    ax.tick_params(length=3, width=0.8)
    return ax


def save(fig, name, outdir, quality=88):
    """Render to PNG then re-encode as WebP (matplotlib cannot write WebP)."""
    png = os.path.join("/tmp", "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(outdir, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))
    return out
