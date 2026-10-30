---
layout: post
title: >-
  An AI-generated solver improved 21 historical circle-packing values
date: 2026-08-24
description: >-
  Established methods yielded independently checkable improvements across many
  circle counts; a follow-up starting from the finished solver found no
  additional records.
image: /img/blog/2026-08-10-packing-records/sweep.webp
tags: [self-improving-agents, optimization, benchmarks]
record: Record
---

A solver written during one self-improvement run exceeded **21 best-known
values** in the **10 August 2026** [Packomania snapshot](https://github.com/jasonzliang/circle-packing-sota/blob/main/sota/sm-radical-v6-n54/comparison.md). A separate sweep used
the extracted solver unchanged across **N=2 through N=93** unequal circles
in a unit square, maximizing their total radius while preventing overlaps.

Across 92 sizes, the sweep produced **21 improvements, 45 ties, and 26
shortfalls**, with no infeasible packings. Improvements occurred at
**N=50–55, 62, 63, 66–69, 71, 72, 77, 80, 82–85, and 87**, with absolute
margins from **2.3e-5 at N=55** to **2.6e-3 at N=51**. These are dated
comparisons with [Packomania](https://www.packomania.com/csqv/csqv.html),
whose entries continue to change.

{% include figure.html
   src="/img/blog/2026-08-10-packing-records/sweep.webp"
   alt="Solver total radius minus the 10 August reference value for N=2 to 93
        on a symmetric-log axis: 21 improvements, 45 ties and 26 shortfalls."
   caption="Comparison with the historical reference snapshot. Positive
            differences exceed its entries; absolute differences within 1e-6 count
            as ties. All twenty-one
            improvements occur between fifty and eighty-seven circles.
            Agreement at other sizes does not prove optimality."
%}

This followed an earlier solver's
[27-circle improvement](/blog/circle-packing/). The sweep does not establish
whether the agent's disposition or permission to rewrite values caused the
improvement.

## What changed during the run

The run used an [expansive disposition](/blog/nietzsche/) and unrestricted
permission to [rewrite it](/blog/values-rewriting/). Ten substantive iterations
took **117 minutes** and **$28.83** in API spending, using one agent seed.
The run used no web assistance or copied external solver code. The API figure
is not a complete CPU-compute budget or a matched comparison with other systems.
The final records combine several search passes: a base sweep taking roughly
seven hours on ten CPU cores, followed by targeted searches with larger
per-seed budgets. The [reproduction instructions](https://github.com/jasonzliang/circle-packing-sota#reproduce-the-21-improvements-n54-solver)
separate those costs from agent development.

The decisive solver change appeared at **iteration two**. Iteration one built
a multistart search that finished **3.5e-4 below** the N=54 reference. The next
iteration included centre movements in a linear-programming step and exceeded
that value.

Later iterations failed to improve the N=54 incumbent: iterations three and
four accepted no moves; iteration five found no improvement in **504 fresh
starts**; iterations eight through ten tested changes that lost score. The
run also generalized the solver to other circle counts. The eventual 21-size
result came from subsequent search passes rather than 21 separate breakthroughs
inside the agent loop.

## How the solver works

With circle centres fixed, choosing the best radii is a linear program. Each
radius must fit between its centre and the square's walls, and each pair must
sum to no more than the distance between its centres. This formulation appears
in [Eppstein's work](https://arxiv.org/abs/1607.02184). It solves radius
selection for a proposed set of centres, leaving centre placement as the outer
search problem. Numerical solutions still require feasibility checks.

The new solver used sequential linear programming to move the centres. A
linear lower bound on centre distance supplies conservative non-overlap
constraints, allowing feasible improvements toward a locally jammed packing,
typically in about a second. A second stage perturbed those packings and
accepted some small losses under a tightening threshold, retaining the best
packing throughout.

The ingredients have established precedents: Eppstein's radius optimization;
[convex-concave linearization](https://arxiv.org/abs/1604.02639) associated with Shen, Diamond, Gu and Boyd;
[monotonic basin hopping](https://doi.org/10.1287/ijoc.1080.0263) developed by Addis, Locatelli and Schoen for disk
packing; and Dueck and Scheuer's [threshold accepting](https://www.sciencedirect.com/science/article/pii/002199919090201B). The result demonstrates
autonomous assembly and tuning of known methods, without establishing a new
optimization technique.

## Independent checks and a changing reference table

A [separate checker](https://github.com/jasonzliang/circle-packing-sota#verify-the-results)
recomputed circle counts, containment, pairwise separation, and total radii
from saved coordinates, sharing no code with the solver. All twenty-one
improvements were strictly feasible under that check.

At N=54, the smallest wall clearance was **1.0e-11** and the smallest
circle-to-circle gap **1.8e-11**, compared with a **9.0e-4** improvement over
the historical reference. The improvement is seven to eight orders of
magnitude larger than those clearances. Feasibility and the objective value
are independently checkable properties of the saved packing.

The reference table combines older contributed packings with recently
optimized entries. These twenty-one improvements concerned the older group;
they did not exceed the recent N=26 entry credited to Haowei Lin or the roughly
25 improvements Everett Dutton contributed on 1 August. At N=26, this solver
was **2.5e-10 below** the reference, counted as a numerical tie.

Between the 3 and 10 August snapshots, **43 of the first 100 entries** increased.
Fifteen of the twenty-one improved sizes had their reference raised during
that week, and the new packings exceeded those raised values. Conversely, the
earlier N=27 result had already entered the table: rescoring the original
solver against the 10 August snapshot gave **zero improvements, 28 ties, and
70 shortfalls**. It now tied its own contribution.

## A follow-up produced no additional records

A second run began from a byte-identical copy of the finished solver. It
tested whether packings found at other sizes could provide useful starting
points for further records. The run cost **$24.39** and found no additional
record crossings.

At N=44 it finished **3e-11 below** the reference, a numerical tie. An apparent
N=50 improvement reproduced a packing already held by the first solver;
**40 of 40** warm-start rounds returned the same value. Tests at three targeted
sizes produced no crossings. Transplanting parts of other packings improved
some candidates without crossing a reference value; a final ten-arm attempt
also yielded **zero of ten**. The predictions preceded their measurements.

The last five iterations generated **48 endpoints**, which reduced to
**24 distinct packings** after treating rotations and reflections as
equivalent. These counts suggest that the tested generators repeatedly
revisited existing local optima. Additional independent seeds did move some
sizes from below-reference to above-reference values; the tested recycling
strategy added none.

Each self-improvement experiment used one seed, so the contrast between a
productive first run and a saturated follow-up remains one observation. The
twenty-one independently checkable packings exceeded a dated reference table.
They are best-known-value improvements for that comparison, with no claim of
global optimality or permanent record status.
