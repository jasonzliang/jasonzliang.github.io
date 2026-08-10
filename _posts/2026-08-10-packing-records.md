---
layout: post
title: >-
  My AI agent's new solver beat 21 circle-packing records at once
date: 2026-08-10
description: >-
  A self-improvement run built a solver that beats 21 live Packomania
  records. The follow-up run, warm-started from it, found nothing new.
image: /img/blog/2026-08-10-packing-records/sweep.webp
tags: [self-improving-agents, optimization, benchmarks]
record: Record
---

Pack N circles into a unit square. Any sizes, no overlaps, nothing outside.
Maximise the sum of their radii. For every N,
[Packomania](https://www.packomania.com/csqv/csqv.html) lists the best value
anyone has found.

Last week I wrote about an agent whose solver [took the record at 27
circles](/blog/circle-packing/). This is the next run. Its solver, extracted
unchanged and swept from 2 to 93 circles, beats **21** of those records.

Against the table as it stood on 10 August: **21 wins, 45 ties, 26 short, none
infeasible** across the 92 sizes it solved. The wins are N = 50 to 55, 62, 63,
66 to 69, 71, 72, 77, 80, 82 to 85 and 87, by margins from **2.3e-5** at N=55 to
**2.6e-3** at N=51.

{% include figure.html
   src="/img/blog/2026-08-10-packing-records/sweep.webp"
   alt="Scatter of our sum of radii minus the record, for every N from 2 to 93,
        on a symmetric-log axis. Twenty-one blue circles sit above the line,
        clustered between N=50 and N=87; forty-five grey squares sit on it,
        almost all below N=50; twenty-six orange triangles sit below it."
   caption="Figure 1 of the report. Above the line is a win, on it a tie, below
            it a loss. Nothing under 50 circles is a win, because those records
            are already saturated: the solver ties them instead."
%}

## What the run cost

One self-improvement run, ten substantive iterations, **$28.83** and 117 minutes
of wall clock, single seed. It got an [expansive disposition](/blog/nietzsche/)
and the freedom to [rewrite that document](/blog/values-rewriting/) wholesale
each iteration. No web assistance, and no solver code copied from anywhere.

The whole result arrives at **iteration 2**. Iteration 1 built a competent
multistart search that landed 3.5e-4 *below* the N=54 record. Iteration 2 moved
the circle centres inside the linear program, crossed the record, and every
iteration after it returned a measured null on the tuning it tried: zero
accepted moves at 3 and 4, 0 of 504 fresh starts beating the incumbent at 5,
losses at 8 through 10. What those eight iterations bought was not a better
score at N=54. It was the finding that the pipeline was exhausted there, plus
the generalization from one N to all of them, which is where the other 20
records came from.

## Why it works

One idea does the load-bearing work, and it is not mine or the agent's. **Fix
the centres and the best radii are a linear program** — maximise the sum subject
to each pair of radii summing to no more than the distance between their
centres, and each radius fitting its walls. That is
[Eppstein's](https://arxiv.org/abs/1607.02184) formulation. It means the search
only ever explores centre positions, gets the radii exactly and for free, and
every configuration it scores is feasible by construction.

The agent's own move was the centre search. The previous solver optimised
centres and radii jointly and hopped between restarts greedily. This one
linearises the non-overlap constraint by its own convex under-estimator, so
every step stays strictly feasible and walks uphill to a jammed packing in about
a second, then wanders between those jammed packings accepting small losses on a
schedule that tightens as it goes, while the best-so-far only ever rises. That
substitution is what cracked sizes the old approach had plateaued on.

Every component has plain prior art: the radii program is Eppstein's, the
convex-concave linearisation is Shen, Diamond, Gu and Boyd's, monotonic basin
hopping is Addis, Locatelli and Schoen's and was invented for disk packing, and
threshold accepting is Dueck and Scheuer's, from 1990. **No technique here is
new.** What the loop did was assemble four graduate-level pieces into a working
pipeline and tune the split between its two stages, unaided.

## The margins are not floating-point noise

Each win was re-derived from its coordinates by a checker that shares no code
with the solver and re-counts the circles, containment, overlaps and total
itself. The packings are strictly feasible with room to spare, not
feasible-within-tolerance: at N=54 the tightest gap to a wall is 1.0e-11 and the
tightest gap between two circles 1.8e-11, against a winning margin of 9.0e-4.
The margin is seven to eight orders of magnitude larger than the slack.

## Which records were beatable

Not the good ones. Packomania's table mixes a recent, heavily optimised frontier
with much older contributed entries, and the 21 wins are all against the older
kind. The famous N=26 value now credited to Haowei Lin, and the roughly 25
improvements Everett Dutton contributed on 1 August, are not among them: at N=26
this solver ties, 2.5e-10 short.

The table is also **moving fast**. Between snapshots on 3 and 10 August, 43 of
the first 100 records rose. Fifteen of my 21 win sizes had their bar raised
inside that same week, and the values above clear the *raised* bar. But a win
here means "above the best value anyone has published", never "optimal", and
next week's table may absorb some of these.

It already absorbed the last one. Packomania now lists 2.685978684198 at N=27,
which is the number the earlier solver found, so that solver's sweep re-scored
against today's table reads **0 wins, 28 ties, 70 short** — it ties the record
it set. Records that hold get overwritten by their own holder.

## The follow-up that found nothing

I ran a second experiment the next day, seeded byte-identically from the
finished solver, to ask whether warm-starting from packings already solved at
other sizes could cross more records. It could not, and the shape of the failure
is the useful part.

It tied its own target at N=44, 3e-11 under the record. It once reached an
above-record value at N=50 and then discovered it had re-derived a packing the
first solver already held; asked to repeat that, **40 out of 40** warm rounds
returned the identical number for zero gain. Three targeted sizes under the full
recipe: zero crossings. Grafting pieces of foreign packings in: improving moves,
zero crossings. A last ten-arm attempt: 0 for 10. Each of those was a prediction
written down before it was measured.

Then it measured why. Under a test that treats rotations and reflections of the
same packing as the same packing, the **48 endpoints its last five iterations
generated turned out to be 24 distinct packings.** Its new generators were
rediscovering optima it already had. Fresh compute on independent seeds moved
sizes from short to winning; recycling solved packings moved nothing.

$24.39 for a run whose entire output is nulls and one saturation measurement.
That is a fair price, and it is the run I would have been most tempted not to
publish.

## What I am claiming

Twenty-one packings that beat the best published values, each one checkable in a
second by arithmetic on a list of coordinates, produced by a loop that wrote its
own solver for under thirty dollars. Not a new algorithm. Not proven optima. Not
a record set that will survive contact with next month's table.

The caveats are the same four as last time, and one is worth repeating because
it cuts against the headline: **each self-improvement run is a single seed.**
The build-then-saturate story across these two runs is one observation, not a
finding. What does not depend on the run count is the artifacts, which are fixed
and verifiable however they were found.
