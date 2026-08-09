"""Figure for "An agent's map of the web stays a tree for 400 steps".

Panels 1 and 2 are read straight off the saved graph snapshots of one run,
  rome/caesar/result/12_13_constrained_creativity/
      agent_CaesarExplorer.graph_iter{50,100,...,1000}.json
which the agent wrote every 50 steps.

  Pages  = len(nodes).
  Loops  = the cycle rank E - V + C of the undirected graph, where C is the
           number of connected components. Every snapshot of THIS run has
           C = 1, but 63 of the 2,382 snapshots in the set do not, and
           E - V + 1 goes negative on 14 of them, so C is computed, never
           assumed.

What the snapshots say, and what the post quotes:
  step   50 100 150 200 250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000
  pages  26  58  84  91 119 140 167 200 236 266 304 324 345 372 401 425 456 477 504  522
  loops   0   0   0   0   0   0   0   0   1   1   1   1   1   1   1   1   7  11  11   19
  depth   5  19  23  23  23  23  23  23  26  31  31  31  31  31  31  31  31  31  31   31

Panel 3 is the across-run context, without which panels 1 and 2 read as
typical when they are not. Population: the 77 runs that snapshot every 50
steps and reach step 1,000 (the full set is 102 runs, but 13 snapshot every
10 steps and 1 every 5, and only 80 reach step 1,000, so restricting to a
single interval keeps the onset resolution comparable across runs).

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks the matplotlib import).
"""

import collections
import glob
import gzip
import json
import os
import re
import statistics

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image  # noqa: E402

BLUE, ORANGE, GREY, RED = "#2b6cb0", "#dd6b20", "#a0aec0", "#c53030"
INK, MUTED = "#1a202c", "#4a5568"
OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = "/Users/jason/Desktop/rome/caesar/result"
SRC = ROOT + "/12_13_constrained_creativity"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 12, "axes.titlesize": 14.5, "axes.titleweight": "bold",
    "axes.labelsize": 11.5, "axes.edgecolor": MUTED, "axes.linewidth": 0.9,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "legend.frameon": False, "legend.fontsize": 11,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save(fig, name, quality=88):
    png = os.path.join(OUT, "_%s.png" % name)
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    out = os.path.join(OUT, name + ".webp")
    Image.open(png).convert("RGB").save(out, "WEBP", quality=quality, method=6)
    os.remove(png)
    print("%s  (%.0f KB)" % (out, os.path.getsize(out) / 1024.0))


def components(node_ids, undirected_edges):
    adj = {n: set() for n in node_ids}
    for a, b in undirected_edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    seen, n = set(), 0
    for start in adj:
        if start in seen:
            continue
        n += 1
        stack = [start]
        seen.add(start)
        while stack:
            for nxt in adj[stack.pop()]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
    return n


def read(path):
    """One snapshot -> (pages, loops). Two node schemas exist: the older one
    keys nodes by 'url', the newer by 'id'."""
    opener = gzip.open if path.endswith(".gz") else open
    d = json.load(opener(path, "rt"))
    ids = [n["id"] if "id" in n else n["url"] for n in d["nodes"]]
    und = {tuple(sorted((e["source"], e["target"]))) for e in d["edges"]}
    return len(ids), len(und) - len(ids) + components(ids, und)


def series(rundir):
    """step -> (pages, loops). The same snapshot is occasionally stored both
    plain and gzipped; keyed by step, so it is only counted once."""
    out = {}
    for f in glob.glob(rundir + "/agent_CaesarExplorer.graph_iter*.json*"):
        step = int(re.search(r"iter(\d+)\.json", f).group(1))
        if step not in out:
            out[step] = read(f)
    return out


# ---- panel 1 and 2 data: the one run ----
one = series(SRC)
steps = sorted(one)
pages = [one[s][0] for s in steps]
loops = [one[s][1] for s in steps]
assert (pages[0], pages[-1], loops[-1]) == (26, 522, 19), one
assert len(steps) == 20 and steps[-1] == 1000

# ---- panel 3 data: when the first loop closes, across comparable runs ----
onsets, never = [], 0
for rundir in sorted({os.path.dirname(f) for f in glob.glob(
        ROOT + "/**/agent_CaesarExplorer.graph_iter*.json*", recursive=True)}):
    s = series(rundir)
    ks = sorted(s)
    if max(ks) < 1000:
        continue
    gaps = collections.Counter(b - a for a, b in zip(ks, ks[1:]))
    if gaps.most_common(1)[0][0] != 50:
        continue
    first = next((k for k in ks if s[k][1] > 0), None)
    if first is None:
        never += 1
    else:
        onsets.append(first)
n_runs = len(onsets) + never
med = statistics.median(onsets)
assert (n_runs, never, med) == (77, 1, 150), (n_runs, never, med)
counts = collections.Counter(onsets)

fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(13.6, 4.3))
for ax in (a1, a2):
    ax.set_xlabel("Exploration steps taken", labelpad=6)
    ax.set_xlim(0, 1080)
    ax.set_xticks([0, 200, 400, 600, 800, 1000])
for ax in (a1, a2, a3):
    ax.grid(True, color="#e2e8f0", lw=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=3, width=0.8)

# ---- left: pages discovered
a1.plot(steps, pages, "-o", color=BLUE, lw=2.5, ms=4, zorder=3)
a1.set_title("One run: the map keeps growing", loc="left", pad=12)
a1.set_ylabel("Pages on the map")
a1.set_ylim(0, 600)
a1.set_yticks([0, 100, 200, 300, 400, 500])
# Both labels sit above the curve; anything below or on it collides.
a1.annotate("26 pages", xy=(50, 26), xytext=(105, 215), fontsize=11,
            color=MUTED, ha="left", va="bottom",
            arrowprops=dict(arrowstyle="->", color=MUTED))
a1.annotate("522 pages", xy=(1000, 522), xytext=(575, 468), fontsize=11,
            color=MUTED, ha="left", va="bottom",
            arrowprops=dict(arrowstyle="->", color=MUTED))

# ---- middle: cycles in the map
a2.plot(steps, loops, "-o", color=ORANGE, lw=2.5, ms=4, zorder=3)
a2.set_title("and folds back on itself late", loc="left", pad=12)
a2.set_ylabel("Loops in the map")
a2.set_ylim(-1.0, 23)
a2.set_yticks([0, 5, 10, 15, 20])
a2.text(195, 1.4, "a pure tree\nfor 400 steps", fontsize=10.5, color=MUTED,
        ha="center", va="bottom")
a2.annotate("exactly one loop\nfor the next 350", xy=(620, 1.2),
            xytext=(430, 8.4), fontsize=10.5, color=MUTED,
            arrowprops=dict(arrowstyle="->", color=MUTED))
a2.annotate("then 19", xy=(1000, 19), xytext=(800, 15.0), fontsize=11,
            color=MUTED, arrowprops=dict(arrowstyle="->", color=MUTED))

# ---- right: onset across runs, i.e. how unusual that run is
xs = sorted(counts)
bars = a3.bar(xs, [counts[x] for x in xs], width=42, color=GREY, zorder=3)
for x, b in zip(xs, bars):
    if x >= 450:
        b.set_color(ORANGE)
a3.set_title("but most runs get there sooner", loc="left", pad=12)
a3.set_xlabel("Step at which the first loop closes", labelpad=6)
a3.set_ylabel("Runs (of 77)")
a3.set_xlim(0, 950)
a3.set_xticks([0, 200, 400, 600, 800])
a3.set_ylim(0, 24)
a3.set_yticks([0, 5, 10, 15, 20])
# zorder 2 keeps the median line behind the bars, so it does not split the
# one it lands on into what looks like two bars.
a3.axvline(med, color=BLUE, lw=1.6, ls=(0, (4, 2.5)), zorder=2)
a3.annotate("median\nstep %d" % med, xy=(med, 21.4), xytext=(255, 20.6),
            fontsize=10.5, color=BLUE, ha="left", va="top",
            arrowprops=dict(arrowstyle="->", color=BLUE))
a3.annotate("the run at left, and 11 others,\nare still trees at step 400\n"
            "(one never closes a loop at all)",
            xy=(452, 2.5), xytext=(942, 15.6), fontsize=10.3, color=ORANGE,
            ha="right", va="top",
            arrowprops=dict(arrowstyle="->", color=ORANGE,
                            connectionstyle="arc3,rad=0.16"))

fig.subplots_adjust(wspace=0.30)
save(fig, "graph-growth")
