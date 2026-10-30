---
layout: post
title: >-
  How Caesar's web exploration graphs grow and reconnect
date: 2026-05-12
description: >-
  Saved web explorations show frequent returns to earlier pages and large
  differences in how new routes and connections develop.
image: >-
  /img/blog/2026-05-12-graph-growth/graph-growth.webp
tags: [agents, knowledge-graphs, visualization, caesar]
---

[Caesar](https://jasonzliang.github.io/caesar-agent/) records its web exploration
as a graph. Pages become nodes; followed links become edges. That structure
supplies context for [note-taking](/blog/hub-vs-leaf/) and records how the
agent moves between sources.

In a comparison set of **77 crawls**, the median run spends about **44% of its
steps reopening pages**. The first recorded graph cycle appears at a median of
[**150 steps**](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-05-12-graph-growth/make_figs.py#L124-L143). A single illustrative run develops cycles much later, showing
why one trajectory is an unreliable description of the whole system.

## The comparison set

A step is one turn of the exploration loop: open a page, read it and choose the
next move. A 1,000-step crawl therefore need not contain 1,000 distinct pages.
Each node's visit counter makes revisits directly countable.

The archive contains 102 runs, of which 80 reached 1,000 steps
([reported counts and plotting code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-05-12-graph-growth/make_figs.py#L15-L27)). Of those, 77
saved snapshots every 50 steps and form the comparison set. The consistent
interval makes their recorded timing comparable.
Revisit rates, variance, depth and question-type comparisons use unpublished
exploration snapshots.

The [plotted example](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-05-12-graph-growth/make_figs.py#L15-L20) explores a constrained-synthesis question about inventing
an emotion humans do not experience. It grows from 26 nodes at step 50 to
**522 at step 1,000**. The largest graph in the comparable set reaches 941.
Revisits can reflect backtracking through earlier branches, so their frequency
alone cannot establish wasted effort or an optimal traversal policy.

Discovery rates fluctuate within individual crawls as well as between them.
Only about a third of discovery-rate variance lies between runs. The smooth
cumulative growth curve conceals intervals in which the agent adds pages quickly
and others in which progress slows.

## When cycles appear

The [cycle count](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-05-12-graph-growth/make_figs.py#L71-L102) uses the graph's undirected
[cycle rank](https://en.wikipedia.org/wiki/Cyclomatic_number):
**edges − nodes + [connected components](https://en.wikipedia.org/wiki/Component_%28graph_theory%29)**.
It counts independent cycles, or the number of edges that must be removed to
leave a forest. The formula also handles disconnected graphs. Zero means the
undirected graph contains no cycles; it does not mean the agent never
backtracked.

In the example, the graph remains a tree through step 400. A cycle first
appears in the step-450 snapshot, and the count stays at one through step 800.
It then rises to 7, 11, 11 and **19** in the final four snapshots. Across all 77
runs, the final count ranges from 0 to 126.

{% include figure.html
   src="/img/blog/2026-05-12-graph-growth/graph-growth.webp"
   alt="One crawl grows from 26 pages at step 50 to 522 at step 1,000. Its cycle
        count stays zero through step 400, reaches one at step 450 and ends at
        19. Across 77 crawls, the median first recorded cycle is at step 150."
   caption="The first two panels show one crawl sampled every 50 steps. The
            third gives its context among 77 comparable runs. Cycle onset is
            resolved only to the snapshot interval; the example reconnects
            later than most runs."
%}

Thirty-seven runs already contain a cycle by step 100; only 12 remain trees at
step 400. Seventy-six eventually contain a cycle, first recorded between steps
50 and 850; one remains acyclic through
step 1,000. Among runs that develop a cycle, the median first recorded
onset is 150 steps. Constrained-synthesis runs have a median onset of 225,
compared with 100 for open-ended synthesis.

In the median run, 40% of the final cycle count is present by step 500 and 76%
by step 800. Only 10 of 77 runs gain more than half their cycles in the final
fifth.

A cycle records an additional connection between already connected pages. It
may reflect convergence between lines of inquiry, but topology alone cannot
establish a meaningful conceptual connection or improved understanding.

## Depth and question type

Depth here follows the route by which a page was first reached, rather than its
shortest path from the start. The example reaches depth 23 by step 150, stays
there through step 400, then reaches 26 at step 450 and 31 at step 500. Its
maximum depth remains 31 for the rest of the run.

Across the full set, the median run reaches 87% of its final depth by step 500,
but 48 runs continue deeper afterward. Among those, the median additional gain
is 36 levels. The example is shallow beside the overall median final depth
of 84.

Sixty comparable runs carry one of five question types, with twelve runs per
type. Open-ended synthesis produces the largest median graph, **678 pages**.
The other four types have medians from 531 to 544; those small differences do
not support a clear size ordering.

Constrained synthesis is more distinctive in connectivity: its median cycle
count per page is 0.023, compared with 0.043 for cross-domain synthesis, 0.042
for counterfactual reasoning, 0.033 for meta-creativity and 0.036 for open-ended
synthesis. These are descriptive comparisons from the archived runs, without
uncertainty intervals or a controlled test of question type.

The 400-step tree phase and flat second-half depth belong to one run; the
archive supplies the denominator needed to interpret them.
