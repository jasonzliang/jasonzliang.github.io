---
layout: post
title: >-
  My 11-of-14 win tally evaporated when I audited it
date: 2026-07-26
description: >-
  Eleven of fourteen matched pairs favoured the expansive disposition. Five
  discounts later, one each way.
image: /img/blog/2026-07-26-bin-packing-values/offline-inrun-vs-heldout.webp
tags: [self-improving-agents, evaluation, values]
---

I have been testing whether a coding agent's starting **values** change what it
builds. Two disposition documents, three bullets and 120 to 150 words each,
everything else byte-identical. Cautious: smallest verified step, reuse the
proven approach, a solved problem is done, bank it and stop. Expansive: the move
that most widens what you could do next, nothing you achieve is a stopping
point. I call them control and nietzsche, after [the second's
source](/blog/nietzsche/).

This post covers 28 runs plus an 8-run replication cohort. v3, sm-v4 and sm-v5
are successive versions of the two files; the sm ones let the agent rewrite its
own values mid-run. A cell is one task, disposition and version; a pair is two
cells differing only in disposition; the detail that governs everything is **one
run per cell**.

Values change *what* the agent builds, a lot. Which is better, this study cannot
say.

## The task

Every run is the same loop: the agent edits one solver, commits, and is
re-scored by a fixed evaluator, ten times over, twenty in the earliest cohort.
The task is [one-dimensional
bin-packing](https://en.wikipedia.org/wiki/Bin_packing_problem), pack items into
as few fixed-size bins as possible: NP-hard, with strong classical baselines,
the standard LLM-heuristic-discovery testbed since
[FunSearch](https://doi.org/10.1038/s41586-023-06924-6).

**Offline** shows the solver the whole list up front; **online** feeds items one
at a time, no lookahead. Offline is close to solved by a classical heuristic
plus local search, so the optimised score pins near the ceiling and every arm
ties; online leaves headroom above the best simple rule, so it separates
solvers. Two earlier tasks, cobench and generalize, were offline variants, here
only in the tally.

The **in-run** score is the one the agent sees and pushes up; the **held-out**
score I compute after, on families it never trained against, from published
generators with a seed it cannot read. Everything turns on that difference. I
redesigned that set partway through: the original, Schoenfield's Hard28, had
both arms and the reference heuristics all solving exactly 5 of its 28 to the
proven optimum, its tie a property of the instrument, not a finding.

## Offline, in-run says nothing

{% include figure.html
   src="/img/blog/2026-07-26-bin-packing-values/offline-inrun-vs-heldout.webp"
   alt="Dot plot of in-run and held-out scores for eight offline runs."
   caption="Eight offline runs; the sm-v4 cells were run twice, in two cohorts.
            The dashed line is the Best-Fit-Decreasing floor at 0.837, tied
            exactly here by First-Fit-Decreasing: two runs finish at or barely
            above it, one below. Both dispositions appear in the top three rows
            and the bottom three, so the spread is a finding and the ordering
            is not."
%}

All eight finished between **0.9905 and 0.9955** on the optimised score, a
spread of 0.005 across six conditions in two cohorts; the same eight on held-out
instances spread over 0.235, from **0.756 to 0.991**.

Within one matched pair, same task and values version, the held-out gap to
optimum was 0.010 for one arm and 0.244 for the other, a factor of **24**; in
another, 0.009 against 0.159, a factor of 18 the other way.

Read 24 as an order of magnitude, not a measurement. The 0.244 is a mean over 40
held-out instances, 4 of them infeasible inside the compute budget and scored as
a full 100 per cent gap: those four are 10 of the 24.4 points, and across the
other 36 the solver packed 16.0 per cent above the optimum, the classical floor
within noise. Standard error 0.039: the failure is real and large, the multiple
is not.

Offline only: online the in-run score is not pinned, and it agreed with held-out
in the final-harness cohort.

## What they built

| Signature | control, cautious | nietzsche, expansive |
|---|---|---|
| Helper tools per run | 1, 1, 6, 1 | 7, 8, 10, 15 |
| Solver size, v3 and sm-v4 | 765, 385 lines | 1038, 979 |
| Strategies | 1-2: greedy, local search | 4: adds perfect-fit search |
| Unproven additions | pruned or withheld | shipped |
| Where the bulk goes | ruling-out tests, audits | more solver machinery |

Those are logical lines, blanks, comments and docstrings excluded; the run
report counts the same four files raw, in order, at 1278 and 628 against 1429
and 1553, so files on disk run 1.4 to 1.7 times longer. The cautious runs
converge onto one line of work and defend it; the expansive ones build a tool
whenever one would help and ship machinery whose value they have not shown. The
size half is offline only: online the scoring functions are compact whoever
wrote them; the difference is in the kind of rule.

One episode illustrates the mechanism without testing it. In offline sm-v4 the
cautious arm built a perfect-fit search late, an engine capable of exact optima,
and did not ship it: on its in-run metric it looked like noise. It then lost
that held-out cell by a factor of roughly 18. The disposition changed what got
shipped, not what could be built; that reading comes from the commit log, not
the final code, which no longer holds the engine. The same engine sank the
expansive arm one cell over: in offline v3 its perfect-packing endgame ran past
the compute budget on the large held-out instances, where those four infeasible
packings came from. One artifact, overreach in one cell and the winning move in
another; it labels outcomes, it does not predict them.

Four non-independent runs per arm, not seed-controlled, and the cautious tool
count varies from 1 to 6 across its four. A behavioural signature, not proof.

## The tally evaporates

The number I wanted to be true: across 14 matched pairs, **11 favoured the
expansive disposition** on the in-run score, sign test p around 0.06, exactly
the shape of result that gets written up. So I went through them.

**About four of the wins are saturated ties**, both arms pinned: offline in-run
at about 0.99, cobench at about 0.999, and Hard28, the generalize task's
held-out, saturated as above. Those margins run 0.0006 to 0.0011: a win of a
thousandth on a benchmark that cannot resolve the arms is not a win.

**About two are against broken control runs:** the one in a committed report
never left the Best-Fit floor, in-run 0.9534 and held-out 0.9549 against a
reference of 0.9524. Beating a failed run tells me about that run, not the
disposition.

**One pair is contaminated and excluded:** its expansive arm imported a
published heuristic tuned on the exact test distribution; the clean re-run flips
to cautious.

**Three more are one result in three hats:** pairs A1, A2 and E6 are
near-duplicate expansive solvers on shared held-out draws, so counting them as
three inflates the tally by two.

**And one cohort points the other way:** the three generalize pairs run −0.0028,
−0.0009 and +0.0009 in-run, one of them in the eleven, netting −0.0028 for
control. Warm-started, so not clean evidence either, but not support.

The categories are not a partition; subtracting in sequence would be dishonest:
the broken control arm belongs to A1, itself one of the near-duplicates, so that
pair is disqualified twice and removable once. Nor do they cover everything:
nine of the eleven wins fall into them, and of the two left over one is an older
run I never reported, leaving exactly one clean expansive win standing.

What is left is the four pairs under the final matched harness, with a
discriminating held-out. On held-out that cohort is **2 to 2**; on in-run 3 to 1
for the expansive arm, but two of those three are the saturated offline ties
above and the two online pairs carry opposite signs and cancel.
Recency-weighted, the pooled online effect on held-out is −0.0024,
indistinguishable from zero. The 11-of-14 direction does not shrink; it
evaporates.

Two more things I cannot explain away as tidying. Re-running sm-v4 **reversed
the held-out winner in both tasks**, offline expansive to cautious, online
cautious to expansive: direct non-reproducibility, though confounded, because
the re-run also changed the harness, including a wall clock that went from one
hour to three. And in the "clean" cohort one cautious arm rewrote its own values
eight times mid-run, growing that block from 14 to 33 lines, its held-out score
from its ninth iteration rather than its tenth, so even that pair is not the
controlled contrast it looks like.

That last discount cuts against me: the pair it damages is one the cautious arm
won. Throw it out and the recent online evidence is a single clean pair, won by
the expansive arm. Against a split offline result, that is still not a
direction, but the tidying is not free.

## What survives

My verdict slide put it in five words: behaviour changes, direction does not. It
attaches a condition, once the analysis is recency-weighted, and that condition
does real work.

The behaviour half holds up: two dispositions differing by about 150 words
produce measurably different artifacts, and generalization swings by up to 24
times while the training score barely moves. So an evaluation reading only the
optimised score is blind to most of what the values did. The direction half is
not a finding, and one run per cell is why: a single pair mixes the values
effect with seed luck and trajectory, which no amount of extra instance draws
fixes, only more runs. The study shows an effect, not its size or which way it
runs. The fix is a powered replication, several runs per condition with the
[analysis fixed in advance](/blog/pre-registration/), which is what I ran next,
on a different task, where the question got a real answer.

The uncomfortable part is how close I came to publishing 11 of 14: a plausible
p-value, a mechanism and a story, and no tally that meant anything once I looked
at the pairs one by one. One clean win each way is not a direction.
