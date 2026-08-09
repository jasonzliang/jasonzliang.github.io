---
layout: post
title: "The same values swap made the same two agents twice"
date: 2026-07-02
description: >-
  Two mission catalogs, two values files, four runs. Both cautious runs cleared
  the numerical bar they set themselves in the first five iterations. Neither
  bold run cleared its bar at all.
image: >-
  /img/blog/2026-07-02-same-two-agents/four-runs.webp
tags: [self-improving-agents, values, agent-design]
---

In June I ran [two sixty-iteration agents that differed only in a values
file](/blog/nietzsche/). They came out visibly different, and the honest
conclusion was that at one run per condition there was no reliable winner. That
is still true.

This post has a narrower claim the earlier one could not make. The same values
swap was run on two unrelated mission catalogs, four runs in total, and the
character split came out the same shape both times.

The sample size, before anything else: two missions, one run per cell, four
runs. "Replicated" here means a shape appeared twice. It is not statistically
powered and it cannot tell you which disposition is better. It can tell you the
difference is not a one-off.

## What a mission run is

These four runs used the loop's focused mode. On iteration 1 the agent browses a
curated list of research repositories read-only, picks one target, and vendors
it offline. Then it builds its own benchmark: inputs, a scoring script, a
measured baseline, and a `CRITERION.md` holding one numeric bar it has to beat.
The benchmark is frozen from that point. Every later iteration changes one lever
and is attacked by refuter agents whose job is to falsify the claim.

**The bar is the agent's own.** Nobody outside the run picks the target or the
number. That matters for everything below.

The two catalogs are unrelated: one is a curated list of self-evolving agent
techniques, the other a different list on agent evolution. Mission 1 ran 50
iterations capped at 40 minutes each on 23 June. Mission 2 ran 40 iterations
capped at 60 minutes on 24 June. Same runner, same model, same honesty floor.
The planned difference is one file: a cautious values document against one
written from Nietzsche.

"Integrity pass" means six mechanical checks an auditor can re-run: frozen
graders byte-identical from iteration 1 to the final commit, an append-only
artifacts directory, an unedited instructions file, a single-root git history,
no network at evaluation time, and new benchmarks added rather than modified.
All four runs passed at run time.

## Mission 1

The cautious run picked a genetic search over prompts, built an offline stand-in
for the expensive scoring oracle, measured a baseline of 0.728217, and set its
bar at 0.745. It cleared that at **iteration 5**, with 0.74932 on held-out
seeds, wins on 9 of 10, and a margin of 5.2 standard errors. Its own capstone
calls that "the one frozen-bar pass": it never cleared the bar again, and did
not need to. It spent the remaining 45 iterations finding where the algorithm
breaks, ending on a budget-allocation law, a class of problems where sixteen
times more compute bought nothing, and one algorithm that crossed that wall.

The expansive run picked an LLM-driven program search applied to online bin
packing, and did something at iteration 1 that I keep coming back to. It had two
candidate baselines: a naive evolutionary algorithm at 0.0659 held-out, and
random search at 0.0641, where lower is better. It froze the **better** one as
its bar, writing the reason into its own criterion file: "Freezing the EA's
0.0659 as the bar would be a strawman." It chose the harder number deliberately,
before knowing whether it could reach it.

It never reached it. Eight outer-loop levers were tried and refuted on the
frozen bench. At iteration 13 one appeared to clear the gate; at iteration 14 a
pre-registered re-test killed it as optional stopping and the run retracted its
own win. At iteration 39 it ran the rival method's published code on its own
benchmark and found the reason: that method loses at the problem size the
mission was scored on and matches its published result at thirty times that
size. At iteration 41 it froze a new benchmark above the crossover, where the
same machinery won by a wide margin. Every artifact after that says this does
not move the frozen mission gate, still not met.

## Mission 2

Different catalog, same shape.

The cautious run picked an archive-based search method on a standard
ten-dimensional test function, measured a baseline of 1841.00, and set its bar
at baseline plus ten percent, or 2025.10, with a coverage requirement and a
held-out number attached. It cleared that at **iteration 4** with 2040.66. Then
it computed a closed-form ceiling for its own metric, 2318.36, and spent 36
iterations climbing towards it, ending at 2138.36 held-out, 92.2% of the
ceiling. Two further axes it closed by proving they could not be crossed.

The expansive run picked an archive controller from a different codebase and
replaced the LLM inside it with a deterministic oracle, so that any change could
be attributed to the controller rather than to model noise. Baseline 0.867839,
bar 0.8978. Its best controller reached 0.894753. Short by 0.003, and it never
closed that gap. It built thirteen frozen benchmarks instead, and its last real
experiment retracted its own headline law as coarse rather than fine.

{% include figure.html
   src="/img/blog/2026-07-02-same-two-agents/four-runs.webp"
   alt="Four horizontal bars, one per run. Mission 1 cautious: bar cleared at
        iteration 5, then 45 iterations finding where the algorithm breaks.
        Mission 1 expansive: bar never cleared over 50 iterations. Mission 2
        cautious: bar cleared at iteration 4, then 36 iterations climbing to
        92.2% of the ceiling. Mission 2 expansive: bar never cleared over 40
        iterations."
   caption="Each agent chose its own target and froze its own numerical bar at
            iteration 1, so the two runs inside a mission are not clearing the
            same bar. One run per cell. Every run reached its final iteration."
%}

## The part I find interesting

A disposition that reliably produces a run which fails to clear its own bar is a
stranger result than one that reliably clears it.

Both bold runs missed a number they had picked freely and could have set lower,
and neither lowered it afterwards, which is the failure I built the
frozen-grader machinery to catch. Both spent the back half of the run
characterising the miss, and both produced their sharpest work there.

Two readings, and I cannot separate them. Either this disposition picks harder
targets and pays for it, or it is simply worse at the narrow thing a mission
asks for. The mission-1 criterion file, where the run rejected the easier
baseline in writing, is evidence for the first. One run per cell cannot rule out
the second.

## What replicated, and what did not

The shape replicated, and there are counts behind it I can still check in the
archived workspaces. Frozen benchmarks: 1 against 10 on mission 1, 6 against 13
on mission 2. Log length on mission 2: 1,487 lines against 3,055.

Here is the confound, and it is not small. **The two agents inside a mission
were not working on the same problem.** Each picked its own target and wrote its
own bar, so "cleared the bar" compares two different tests. Part of what I am
calling character is the choice of target itself, which makes the headline
comparison less clean than it looks.

A later audit of mine, across nine runs, pushed harder in that direction. It
filed this mission-2 pair as the cleanest comparison in the set, called the two
runs near-indistinguishable, and concluded the philosophy left no fingerprint
but the vocabulary. That audit's headline has since been flagged internally as
over-generalised, and I have not resolved the disagreement. What I will say is
that the benchmark counts and log sizes above are things I can count today, and
they do not come out equal. On a third task altogether, [taking my own tally
apart pair by pair](/blog/bin-packing-values/) left no reliable direction at
all.

## What I checked

My write-up of the earlier sixty-iteration pair reported "60 of 60 completed"
when it meant the highest iteration number reached, so I checked these four
first. Here the figures are real: the runner log records every iteration from 1
to the cap finishing cleanly, none killed by the time limit. The count that
produced an artifact is lower, 47 and 45 of 50 and 32 and 33 of 40, and most of
that gap is the scheduled review checkpoint, which is defined not to run a new
experiment.

Three places my slide deck and the workspaces disagree. The deck gives mission 1
commit counts of 85 and 88; the write-up from the day gives 88 and 88; neither
is checkable, because the per-run git directories were deleted on archival,
which also makes "byte-identical graders" a run-time observation I can no longer
re-verify. The deck describes the mission-2 cautious run's benchmark using the
other run's benchmark, a copy-paste, though the baseline number attached to it
is right. And 92.2% is the held-out figure: the scored number is 93.5% of the
same ceiling, and one slide attaches 92.2% to it.

None of those move the shape. I would rather say them than have someone else
find them.
