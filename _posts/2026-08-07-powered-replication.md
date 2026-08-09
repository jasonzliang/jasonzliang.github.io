---
layout: post
title: >-
  I ran it once and got a headline. I ran it five times and it reversed.
date: 2026-08-07
description: >-
  A single-run experiment said an agent's values drove how well its code
  generalized. A replication with five runs per condition found no evidence of
  it at all.
image: /img/blog/2026-08-07-powered-replication/cliffs-delta.webp
tags: [self-improving-agents, replication, evaluation]
---

On 2 August I ran an experiment on self-improving coding agents and got a result
I liked. Three days later I ran it properly and the result went away.

## The setup

An agent is given a task, write a program that plays 2048 well, and a loop. 2048
is the sliding-tile game: you swipe a 4×4 grid, colliding equal tiles merge into
one worth double, and a new tile drops in after every swipe, usually a 2 and
about one time in ten a 4. Your score is the running total of what you have
merged, and every score here is that total. Each iteration the agent improves
its own solver, commits, and gets re-scored: twenty iterations in the first
experiment, fifteen in the replication.

The one thing I vary is a short document describing the agent's **disposition**.
One version is cautious: take the smallest verified step, reuse what works, a
solved problem is done. The other is expansive: take the move that widens what
you could do next, branch when a line stops teaching you, nothing you achieve is
a stopping point.

Then I score each finished solver two ways. On the games it was tuned against,
which it can see. And on games it has never seen: a harder tile-spawn, where the
new tile is a 4 one time in four instead of one in ten, and, critically, a **5×5
board**, when every game it tuned on was 4×4. The second is the one I care
about: it asks whether the agent built something general or something that
merely fits.

## What the first experiment said

The first version had nine conditions and **one run in each**. It produced a
satisfying story: the expansive disposition led to solvers that generalized to
the bigger board, and letting the agent rewrite its values amplified that. Its
best run scored roughly 800,000 points on 5×5, a number a truncation-free
re-score later trimmed to about 720,000. The reference points on that board are
random play, about 8,000, and a greedy program taking whichever move scores best
now, about 80,000. Board size moves those anchors a long way, because a bigger
board keeps a game alive longer: the same greedy program scores only about 4,500
on 4×4. Every reference score here is quoted for the board it belongs to.

## What happened with five runs per condition

The second version [pre-specified the analysis](/blog/pre-registration/), then
ran twenty runs, five in each of four conditions: the two dispositions crossed
with how freely the agent could rewrite its values, bounded to its three value
bullets or unrestricted. A ten-run follow-up added two more conditions at five
runs each, values frozen and never self-edited.

One statistic, Cliff's delta: a rank measure between −1 and +1, where **+1**
means every expansive run outscored every cautious one, **−1** is the reverse,
and **0** means the groups are interleaved. [Which unit it is computed
at](/blog/hub-vs-leaf/) is easy to get wrong; here it is the run.

| What was measured | Cliff's delta | p |
|---|---|---|
| Score on the games it tuned against | **+0.80** | 0.001 |
| Score on a harder tile-spawn it never saw | **+0.60** | 0.024 |
| Score on the unseen 5×5 board | **−0.05** | 0.86 |

The first two lines, over the twenty runs and not the frozen ten, are large and
clean. Disposition really does shape how good the solver gets: on the 4×4 tuning
games the expansive conditions averaged roughly 78,000 to 88,000 points against
the cautious 53,000 to 65,000, twelve to twenty times that 4,500 anchor.

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/dev-capability-curve.webp"
   alt="Six averaged curves across fifteen iterations, five runs each, with
        shaded standard-error bands. The three green expansive curves sit above
        the three blue cautious ones from about iteration 3 onward, ending near
        70,000 to 92,000 against 54,000 to 58,000. A dotted line near the
        bottom marks the greedy baseline at 4,451."
   caption="Figure 1 of the five-run report: the per-iteration climb behind the
            first row of the table. All six conditions, so it also carries the
            frozen ten that the table's deltas exclude. Labels are the report's
            own, control for cautious and nietzsche for expansive, with frozen,
            sm and radical the three self-modification levels, never
            self-edited, bounded to the three value bullets, and unrestricted.
            The separation opens by mid-run at every level."
%}

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/heldout-curve.webp"
   alt="The same six curves scored on the harder tile-spawn, fifteen
        iterations, shaded standard-error bands. The green expansive curves
        again separate upward from the blue cautious ones from about iteration
        6, ending near 54,000 to 59,000 against 41,000 to 43,000. A dotted line
        marks the greedy baseline at about 4,700."
   caption="The same thirty runs on the harder tile-spawn they never saw,
            behind the second row of the table. The separation survives the
            shift, so the capability effect is not an artifact of the games the
            agent tuned on. Note which held-out split this is: re-scoring the
            5x5 board every iteration would have cost 15 to 60 machine-hours,
            so the per-iteration held-out curve is the cheap 4x4 one, not the
            split the headline was about."
%}

Neither line is a replication, though. The first study had read in-distribution
score as precisely where values did *not* act, because a third condition,
written to overfit deliberately, topped that leaderboard. The capability effect
is the five-run study's own finding, not a confirmation of the first.

The third line is a null: on the thing I actually cared about, generalizing to a
board size it has never seen, the dispositions are indistinguishable.

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/cliffs-delta.webp"
   alt="Horizontal bars of Cliff's delta from minus 1 to plus 1, ten expansive
        runs against ten cautious. The bars for the games it tuned against and
        for a harder tile-spawn run well right; the bar for the unseen 5 by 5
        board is barely visible against zero."
   caption="The same twenty runs, expansive against cautious, measured three
            ways. The third bar is the one the original headline was about."
%}

The first headline was that values drive generalization. The five-run study
finds no evidence that they do, which is not the same as showing they do not.
The report calls itself a partial reversal, and that is the honest word.

One limit on how far the reversal reaches. To buy power for the cautious against
expansive contrast, the second study dropped a third condition the first had
carried, the deliberate overfitter I have [written about
separately](/blog/overfit/). That was the first study's central contrast, all
three overfitter runs landing below the random floor on 5×5, and it is not
re-tested here at all. My own report puts it flatly: it "is neither confirmed
nor denied".

I should add that "central contrast" is doing work it has not earned. The 5×5
board was labelled a breadth check, not the primary endpoint, until twelve hours
after those runs finished, and on the endpoint I had designated beforehand the
overfitter generalized better than any of the other eight. It changes nothing on
this page, a different study with a different design, but it does mean the
contrast that was not re-tested was never as settled as the phrase implies.

## The part that killed my mechanism

The first story also said self-modification was doing the work: values set a
ceiling, and letting the agent rewrite them is what "realizes" it.

So I added ten more runs with the values **frozen**, never self-edited. If
self-modification were realizing the effect, freezing it should shrink the gap.

The frozen runs reproduced the capability gap **in full**, at Cliff's delta
**+1.00**: every frozen expansive run beat every frozen cautious run. The effect
is intrinsic to the disposition; self-modification added no significant
capability benefit on top. On the 5×5 board the freest self-modification setting
was directionally worse than the more constrained one (delta 0.41 against it),
though at p = 0.14 that is a hint, not a finding. The cleaner fact needs no
p-value: not one of the ten frozen runs failed outright on 5×5, against four
such failures among the twenty self-modifying ones.

I had the right effect attached to the wrong cause.

## Why the first result looked so good

Look at the individual runs and the 5×5 result stops being a smooth gradient.
Within one condition, runs span from "cannot play 5×5 at all" to about ten times
the greedy 5×5 baseline: the spread inside a condition is larger than any
difference between conditions.

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/heldout-5x5-per-run.webp"
   alt="A log-scale dot plot, one dot per run, six conditions along the bottom.
        Every condition has runs between about 250,000 and 960,000 points and
        runs at or below the random floor near 8,000, only three dots in
        between. A dashed line marks the greedy baseline at 80,424, a dotted
        line the random floor at 8,196. Four runs are crosses on the floor,
        meaning they could not play the board at all; one dot is half-clipped
        by the axis."
   caption="Panel B of Figure 2 of the five-run report, reproduced as drawn,
            half-clipped dot and all. Thirty runs, five per condition, raw 5x5
            score on a log axis. Labels are the report's own: ctrl is cautious,
            niet is expansive, frz, sm and rad the three self-modification
            levels. Two orders of magnitude inside one condition is why five
            runs per cell cannot resolve a difference on this split."
%}

The reason is that 5×5 transfer is **near-binary**. A run either keeps a board
representation that works at any size, or bakes the 4×4 shape into its data
structures for speed and is then structurally incapable of a bigger board. There
is almost nothing in between.

It is also not purely a lottery, and I should not have implied it was. A
commit-by-commit scan of the twenty self-modifying runs found twelve able to
play any size: three incidentally, a free by-product of vectorizing a 4×4
engine, and nine on purpose, seven of those by explicitly de-hardcoding the
search and measuring what it bought. The report's phrase is that attending to
the untested size assumption is a real, if uncommon, learned move.

Either way, that near-binary decision dominates the score. My nine-run study
sampled it once per condition and read the pattern as signal. The honest
description of the first result is not "wrong conclusion from good data": the
data could never have supported the conclusion.

## What this cost and what it bought

Thirty runs and about $1,257 of logged compute, $886 for the twenty
self-modifying ones and $371 for the frozen ten, on top of the $515 the original
nine runs cost. The $1,257 is a floor: one frozen run's log recorded a cost for
only eight of its fifteen iterations. What that bought was a satisfying story
converted into a smaller, duller, true one: **an agent's stated disposition
strongly shapes how good its code gets, and does not detectably shape whether
that code generalizes to a structurally different problem.**

I only caught it because I went back. The first result was internally
consistent, had a plausible mechanism, and would have survived review by anyone
who did not re-run it. There is no version of me reading that write-up more
carefully and spotting the problem. Only the second experiment finds it.
