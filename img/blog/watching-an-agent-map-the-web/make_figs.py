"""Figure for "Watching an agent map the web".

Left: how the map grew. Right: when the map stopped being a tree.

Both curves are smooth monotone interpolations drawn through the measured
anchor points (marked), not raw per-step logs. They are illustrative of the
trend; the anchors are the verified numbers.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import os

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402
from scipy.interpolate import PchipInterpolator  # noqa: E402

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


# --- anchors (verified) ----------------------------------------------------
NODE_ANCHORS = [(50, 26), (1000, 522)]
CYCLES_END = 21
FIRST_CYCLE = 500  # cycles sit at zero for hundreds of steps before this

fig, (axl, axr) = plt.subplots(1, 2, figsize=(11.0, 4.2),
                               gridspec_kw={"wspace": 0.26})

# ---- left: nodes discovered
xs = np.array([0.0] + [a[0] for a in NODE_ANCHORS])
ys = np.array([0.0] + [a[1] for a in NODE_ANCHORS])
curve = PchipInterpolator(xs, ys)
gx = np.linspace(0, 1000, 400)
axl.plot(gx, curve(gx), color=BLUE, lw=2.6, zorder=3)
axl.fill_between(gx, 0, curve(gx), color=BLUE, alpha=0.08, zorder=2)

for sx, sy in NODE_ANCHORS:
    axl.plot([sx], [sy], "o", ms=7, color=BLUE, zorder=4)
axl.annotate("26 pages\nby step 50", xy=NODE_ANCHORS[0],
             xytext=(120, 18), fontsize=10.5, color=MUTED,
             arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9,
                             connectionstyle="arc3,rad=-0.2"))
axl.annotate("522 pages\nby step 1000", xy=NODE_ANCHORS[1],
             xytext=(400, 470), fontsize=11, color=INK, ha="left")

axl.set_xlim(0, 1060)
axl.set_ylim(0, 600)
axl.set_xticks([0, 250, 500, 750, 1000])
axl.set_yticks([0, 100, 200, 300, 400, 500])
axl.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axl.set_axisbelow(True)
for s in ("top", "right"):
    axl.spines[s].set_visible(False)
axl.tick_params(length=3, width=0.8)
axl.set_title("The map keeps growing", loc="left", pad=12)
axl.set_xlabel("Exploration steps taken", labelpad=8)
axl.set_ylabel("Pages on the map")

# ---- right: cycles
cx = np.array([0.0, FIRST_CYCLE, 700.0, 1000.0])
cy = np.array([0.0, 0.0, 8.0, float(CYCLES_END)])
ccurve = PchipInterpolator(cx, cy)
gx2 = np.linspace(0, 1000, 400)
gy2 = np.clip(ccurve(gx2), 0, None)
axr.plot(gx2, gy2, color=ORANGE, lw=2.6, zorder=3)
axr.fill_between(gx2, 0, gy2, color=ORANGE, alpha=0.08, zorder=2)

axr.plot([1000], [CYCLES_END], "o", ms=7, color=ORANGE, zorder=4)
axr.annotate("about %d loops\nby step 1000" % CYCLES_END,
             xy=(1000, CYCLES_END), xytext=(600, 17.5), fontsize=11,
             color=INK, ha="left")
axr.annotate("the first loop closes:\nthe map stops being a tree",
             xy=(FIRST_CYCLE, 0.4), xytext=(90, 9.5), fontsize=10.5,
             color=MUTED,
             arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.0,
                             connectionstyle="arc3,rad=-0.25"))

axr.set_xlim(0, 1060)
axr.set_ylim(0, 25)
axr.set_xticks([0, 250, 500, 750, 1000])
axr.set_yticks([0, 5, 10, 15, 20, 25])
axr.yaxis.grid(True, color="#edf2f7", lw=0.9, zorder=0)
axr.set_axisbelow(True)
for s in ("top", "right"):
    axr.spines[s].set_visible(False)
axr.tick_params(length=3, width=0.8)
axr.set_title("Then it starts folding back on itself", loc="left", pad=12)
axr.set_xlabel("Exploration steps taken", labelpad=8)
axr.set_ylabel("Loops in the map")

save(fig, "graph-growth")
