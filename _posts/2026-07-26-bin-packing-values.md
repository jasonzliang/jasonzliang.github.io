---
layout: post
title: "I took my own result apart, pair by pair"
date: 2026-07-26
description: >-
  A tally said the expansive disposition won 11 of 14 matched pairs. Once I
  removed the ties, the broken runs and the duplicates, the direction was gone.
  What survived was smaller, and more concrete.
image: /img/blog/2026-07-26-bin-packing-values/offline-inrun-vs-heldout.webp
tags: [self-improving-agents, evaluation, values]
---

I have been testing whether a coding agent's starting **values** change what it
builds. Two short disposition documents, three bullet points and 120 to 150
words each, everything else byte-identical. One is cautious: take the smallest
verified step, reuse the proven approach, a solved problem is done, bank it and
stop. The other is expansive: take the move that most widens what you could do
next, nothing you achieve is a stopping point. I call them control and
nietzsche, after [where the second one came from](/blog/nietzsche/).

This post covers 28 runs plus an 8-run replication cohort, paired cautious
against expansive inside matched conditions. Labels like v3 and sm-v4 below are
successive versions of the two disposition files; the sm ones also let the agent
rewrite its own values mid-run, which turns out to matter. A cell is one
combination of task, disposition and version, and a pair is the two dispositions
inside one cell. The design detail that governs everything, and I want it stated
before any number: **one run per cell.** Every comparison here is a single agent
against a single agent.

The result I ended up with is that values change *what* the agent builds, a lot,
and that this study cannot tell you which disposition is better. Most of this
post is how I got there, because the raw tally said something far more exciting
first.

## The task

Every run is the same loop. The agent edits one solver, commits, and is
re-scored by a fixed evaluator, about ten times over, and twenty times in the
earliest cohort. The task is one-dimensional bin-packing: pack a set of items
into as few fixed-size bins as possible. It is NP-hard, it has strong and
well-studied classical baselines, and it is the standard testbed for LLM-driven
heuristic discovery, which is why I chose it. FunSearch was benchmarked on it,
and so were several of the methods that followed.

There are two settings. **Offline** bin-packing shows the solver the whole list
of items up front. **Online** bin-packing feeds items one at a time, each to be
placed immediately with no lookahead. That distinction does more work than it
sounds like. Offline is close to solved by a good classical heuristic plus a
little local search, so the score the agent optimises pins near the ceiling and
every arm ties. Online leaves real headroom above the best simple rule, so it
separates solvers. Two earlier missions, which I called cobench and generalize,
were offline variants; they only appear here in the tally.

I need two axes to keep straight, and everything below turns on the difference.
The **in-run** score is the one the agent can see and is pushing up. The
**held-out** score is one I compute after the run, on families the agent never
trained against, generated fresh from published generators using a seed the
agent cannot read.

I had to redesign that held-out set partway through. The original one was
Schoenfield's Hard28, and on Hard28 the cautious arm, the expansive arm, and the
plain reference heuristics all solved exactly 5 of its 28 instances to the
proven optimum. A benchmark that everything ties on has stopped measuring, and
the tie it produces is a property of the instrument rather than a finding.

## Offline, the training score tells you nothing

{% include figure.html
   src="/img/blog/2026-07-26-bin-packing-values/offline-inrun-vs-heldout.webp"
   alt="A dot plot with eight rows, one per offline run. Every hollow circle,
        the score during the run, sits in a tight cluster between 0.9905 and
        0.9955 at the right-hand edge. The filled circles, the held-out scores,
        fan out from 0.991 down to 0.756, with a dashed red line at the BFD/FFD
        baseline of 0.837. The top three rows are orange, blue, orange; the
        bottom three are blue, orange, orange."
   caption="Eight offline runs, one run per cell; the sm-v4 cells were run
            twice, in two cohorts. The score each agent optimised spans 0.005.
            The score the same solvers got on instances they never saw spans
            0.235. The dashed line is the Best-Fit-Decreasing floor, which
            First-Fit-Decreasing ties exactly here: it is the classical
            heuristic every arm is meant to beat, and two runs finish at or
            barely above it while one finishes below. Both dispositions appear
            in the top three rows and in the bottom three, which is why the
            spread is a finding and the ordering is not."
%}

Offline, all eight runs finished between **0.9905 and 0.9955** on the score they
were optimising. That is a spread of 0.005 across six conditions in two cohorts.
The same eight solvers, scored on held-out instances, spread from **0.756 to
0.991**.

Within a single matched pair, cautious against expansive on the same task and
the same values version, the held-out gap to the known optimum was 0.010 for one
arm and 0.244 for the other: a factor of **24**. In another pair it was 0.009
against 0.159, a factor of 18, pointing the other way. Near-identical training
scores, and generalization that differs by more than an order of magnitude in
either direction.

Read 24 as an order of magnitude rather than a measurement. That 0.244 is a mean
over 40 held-out instances, and 4 of them came back infeasible inside the
compute budget and were scored as a full 100 per cent gap. Those four account
for 10 of the 24.4 points on their own; across the other 36 the solver packed at
16.0 per cent above the optimum, which is the classical floor to within noise.
The standard error on that mean is 0.039. The failure is real and it is large.
The exact multiple is not a stable quantity.

This is an offline story. Online, where the in-run score is not pinned at the
ceiling, the two rankings agreed in the final-harness cohort.

## What the two dispositions built

The most tangible evidence is not in the scores at all. It is in the code.

| Signature | control (cautious) | nietzsche (expansive) |
|---|---|---|
| Helper tools written, per run | 1, 1, 6, 1 | 7, 8, 10, 15 |
| Offline solver size (v3, sm-v4) | 765 and 385 lines | 1038 and 979 lines |
| Solver strategies | 1-2: greedy, local search | 4: adds a perfect-fit search |
| Unproven additions | pruned or withheld | shipped |
| Where the bulk goes | ruling-out tests, audits | more solver machinery |

Line counts here are logical lines, with blanks, comments and docstrings
excluded. The run report counts the same four files raw, in the same order, at
1278 and 628 against 1429 and 1553, so the files on disk run about 1.4 to 1.7
times longer than the table. The cautious runs converge onto one line of work
and defend it. The expansive runs build a tool whenever a tool would help, keep
four separate strategies alive, and ship machinery whose value they have not yet
demonstrated.

The size half of that is an offline observation only. Online, the scoring
functions are compact whichever disposition wrote them, so size does not
separate the arms there and the difference is in the kind of rule.

One episode is as concrete as this gets, and it is an illustration rather than a
test. In the offline sm-v4 cell, the cautious arm built a perfect-fit search
late in its run, an engine capable of reaching exact optima, and then did not
ship it: on its own in-run metric the addition looked like noise, so it withheld
it. It then lost that held-out cell by a factor of roughly 18. The disposition
changed what got shipped, not what could be built. That reading comes from the
run's commit log rather than from the final code, which no longer contains the
engine.

The same kind of engine is what sank the expansive arm one cell over. In the
offline v3 cell its perfect-packing endgame ran past the compute budget on the
large held-out instances, which is where those four infeasible packings came
from. One artifact, overreach in one cell and the winning move in another. It
labels outcomes; it does not predict them.

That is four non-independent runs per arm, not seed-controlled, and the cautious
arm's own tool count already varies from 1 to 6 across its four runs. Read it as
a behavioural signature, not proof.

## The tally, and what happened to it

Here is the number I wanted to be true. Across 14 matched pairs, **11 favoured
the expansive disposition** on the in-run score. A sign test puts that at p
around 0.06. It is exactly the shape of result that gets written up.

So I went through the pairs.

**About four of the wins are saturated ties.** They sit where both arms are
pinned: the offline in-run score at about 0.99, the cobench cohort at about
0.999, and Hard28, which the generalize mission used as its held-out and where
cautious, expansive and the reference heuristics all stop at 5 of 28. Those four
margins run from 0.0006 to 0.0011. A win of a thousandth on a benchmark that
cannot resolve the arms is not a win.

**About two are against control runs that were broken.** The one I can point to
in a committed report never left the Best-Fit floor at all: it finished in-run
at 0.9534 and held-out at 0.9549, against a Best-Fit reference of 0.9524.
Beating a run that failed tells me about that run, not about the disposition.

**One pair is contaminated and excluded.** Its expansive arm imported a
published heuristic that had been tuned on the exact test distribution. The
clean re-run of that cell flips to the cautious arm.

**Three more are one result wearing three hats.** The pairs I labelled A1, A2
and E6 are near-duplicate expansive solvers scored on shared held-out draws.
Counting them as three independent pairs inflates the tally by two.

**And one cohort points the other way.** The three generalize pairs run −0.0028,
−0.0009 and +0.0009 in-run, netting to −0.0028 in favour of control. They were
warm-started, so they are not clean evidence either, but they are certainly not
support.

Those categories are not a partition, and it would be dishonest to subtract them
in sequence. The broken control arm I quoted above belongs to A1, which is also
one of the three near-duplicates, so that pair is disqualified twice over and
can only be removed once. They also do not cover everything. Two of the eleven
wins fall outside all of them, and one of those two is an older run I never
wrote a report for, which leaves exactly one clean expansive win standing. I
come back to it below.

What is left is the four pairs run under the final matched harness, with the
redesigned held-out that actually discriminates. On held-out, that clean recent
cohort is **2 to 2**. On in-run it is 3 to 1 for the expansive arm, but two of
those three are the saturated offline ties above, and the two online pairs carry
opposite signs and cancel. Recency-weighted, the pooled online effect on
held-out is −0.0024, which is indistinguishable from zero. The 11-of-14
direction does not shrink so much as evaporate.

Two more things happened that I cannot explain away as tidying. Re-running the
sm-v4 condition **reversed the held-out winner in both missions**: offline went
from expansive to cautious, online from cautious to expansive. That is direct
non-reproducibility, though it is confounded, because the re-run also changed
the harness, including a wall-clock budget that went from one hour to three. And
inside the "clean" cohort, one cautious arm rewrote its own values eight times
mid-run, growing that block from 14 lines to 33, and its held-out score is from
its ninth iteration rather than its tenth. So even that pair is not the
controlled contrast it looks like.

That last discount cuts against me, and I should say so. The pair it damages is
one the cautious arm won. Throw it out and the recent online evidence is a
single clean pair, which the expansive arm won. Against a split offline result
that is still not a direction, but the tidying is not free.

## What survives

My own verdict slide put it in five words: behaviour changes, direction does
not. It attaches a condition, once the analysis is recency-weighted, and that
condition is doing real work.

The behaviour half is the part that holds up. Two dispositions, differing by
about 150 words, produce measurably different artifacts and generalization that
swings by up to 24 times while the training score moves by 0.005. That is not a
subtle effect, and it means an evaluation that only reads the score the agent
optimised is blind to most of what the values did. One run per cell still bites
here, mind: it cannot fully separate the values from the seed and the
trajectory. What it establishes is that there is an effect, not how large it is
or which way it runs.

The direction half is not a finding at all, and one run per cell is why. A
single pair mixes the values effect with plain seed luck, and no amount of extra
instance draws fixes that; only more runs do. The fix is a powered replication
with several runs per condition and the analysis fixed in advance, which is what
I ran next, [on a different task, where the direction question got a real
answer, and not a tidy one](/blog/powered-replication/).

The uncomfortable part is how close I came to publishing 11 of 14. It had a
plausible p-value, a mechanism, and a story. What it did not have was a tally
that meant anything once I looked at the pairs one at a time. What was left was
one clean win for each disposition, and that is not a direction.
