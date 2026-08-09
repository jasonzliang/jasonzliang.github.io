---
layout: post
title: >-
  I ran it once and got a headline. I ran it five times and it reversed.
date: 2026-08-07
description: >-
  A single-run experiment said an agent's values drove how well its code
  generalized. A properly powered replication found no evidence of that effect
  at all.
image: /img/blog/2026-08-07-powered-replication/cliffs-delta.webp
tags: [self-improving-agents, replication, evaluation]
---

On 2 August I ran an experiment on self-improving coding agents and got a result
I liked. Three days later I ran it properly and the result went away.

## The setup

An agent is given a task, write a program that plays 2048 well, and a loop. 2048
is the sliding-tile game: you swipe a 4×4 grid, two equal tiles that collide
merge into one worth double, and after every swipe a new tile drops into a free
square, usually a 2 and about one time in ten a 4. Your score is the running
total of what you have merged, climbing until the board jams and no move is
legal. Every score in this post is that running total. Each iteration the agent
improves its own solver, commits, and gets re-scored. It does this a fixed
number of times: twenty in the first experiment, fifteen in the replication.

The one thing I vary is a short document describing the agent's **disposition**.
One version is cautious: take the smallest verified step, reuse what works, a
solved problem is done. The other is expansive: take the move that widens what
you could do next, branch when a line stops teaching you, nothing you achieve is
a stopping point.

Then I score each finished solver two ways. On the games it was tuned against,
which it can see. And on games it has never seen: a harder tile-spawn, where the
new tile is a 4 one time in four instead of one in ten, and, critically, a **5×5
board**, when every game it was tuned on was 4×4. That second kind of score is
the one I care about, because it asks whether the agent built something general
or something that merely fits.

## What the first experiment said

The first version had nine conditions and **one run in each**. It produced a
satisfying story: the expansive disposition led to solvers that generalized to
the bigger board, and letting the agent rewrite its own values amplified that.
Its best run scored roughly 800,000 points on the 5×5 board, a number a
truncation-free re-score later trimmed to about 720,000. The two reference
points on that board are random play, worth about 8,000, and a greedy program
that just takes whichever move scores best right now, worth about 80,000. Board
size moves those anchors a long way, because the extra row and column keep a
game alive far longer: the same greedy program scores only about 4,500 on 4×4.
Every reference score in this post is quoted for the board it belongs to.

That is a clean narrative with a mechanism, and I believed it for three days.

## What happened with five runs per condition

The second version [pre-specified the analysis](/blog/pre-registration/), then
ran twenty runs, five in each of four conditions: the two dispositions crossed
with how freely the agent could rewrite its own values, bounded to its three
value bullets or unrestricted. A ten-run follow-up then added two more
conditions at five runs each, where the values were frozen entirely and never
self-edited.

I will use one statistic, Cliff's delta: a rank measure between −1 and +1, where
**+1** means every single expansive run outscored every single cautious run,
**−1** is the reverse, and **0** means the groups are interleaved. [Which unit
it is computed at](/blog/hub-vs-leaf/) is the part that is easy to get wrong;
here it is the run.

| What was measured | Cliff's delta | p |
|---|---|---|
| Score on the games it tuned against | **+0.80** | 0.001 |
| Score on a harder tile-spawn it never saw | **+0.60** | 0.024 |
| Score on the unseen 5×5 board | **−0.05** | 0.86 |

The first two lines are large, clean, powered effects. Disposition really does
shape how good the solver gets: on the 4×4 tuning games the expansive conditions
averaged roughly 78,000 to 88,000 points against the cautious conditions' 53,000
to 65,000, which is twelve to twenty times that 4,500 greedy anchor.

Neither of those two lines is a replication, though. The first study had read
in-distribution score as precisely the place where values did *not* act, because
a third arm, one written to overfit deliberately, topped that leaderboard. The
capability effect is the powered study's own finding, not a confirmation of the
first one.

The third line is a null. On the thing I actually cared about, does it
generalize to a board size it has never seen, the two dispositions are
indistinguishable.

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/cliffs-delta.webp"
   alt="Horizontal bars of Cliff's delta on a scale running from minus 1 to
        plus 1, ten expansive runs against ten cautious runs. Games it tuned
        against, plus 0.80, p 0.001. A harder tile-spawn, plus 0.60, p 0.024.
        An unseen 5 by 5 board, minus 0.05, p 0.86, a bar barely visible
        against zero."
   caption="The same twenty runs, expansive against cautious, measured three
            ways. Two large effects, and one the study could not detect at all,
            which is not the same as showing it is absent. The third bar is the
            one the original headline was about."
%}

The first headline was that values drive generalization. The powered study finds
no evidence that they do, which is not the same as showing they do not. The
report calls itself a partial reversal, and that is the honest word for it.

One limit on how far the reversal reaches. To buy power for the cautious against
expansive contrast, the second study dropped a third condition the first one had
carried, the deliberate overfitter I have [written about
separately](/blog/overfit/). That was the first study's central contrast, with
all three overfitter runs landing below the random floor on 5×5, and it is not
re-tested here at all. My own report puts it flatly: it "is neither confirmed
nor denied".

## The part that killed my mechanism

The first story also said self-modification was doing the work: values set a
ceiling, and letting the agent rewrite them is what "realizes" it.

So I added ten more runs where the values were **frozen**, never self-edited at
all. If self-modification were realizing the effect, freezing it should shrink
the gap.

The frozen runs reproduced the capability gap **in full**, at Cliff's delta
**+1.00**. Every frozen expansive run beat every frozen cautious run. The effect
is intrinsic to the disposition, and self-modification added no significant
capability benefit on top of it. On the 5×5 board the freest self-modification
setting was directionally worse than the more constrained one (delta 0.41
against it), though at p = 0.14 that is a hint rather than a finding. The
cleaner fact there needs no p-value: not one of the ten frozen runs failed
outright on the 5×5 board, against four such failures among the twenty
self-modifying ones.

I had the right effect attached to the wrong cause.

## Why the first result looked so good

Once you look at the individual runs, the 5×5 result stops being a smooth
gradient and becomes something else entirely. Within a single condition, runs
span from "cannot play 5×5 at all" to about ten times the greedy 5×5 baseline.
The spread inside a condition is larger than any difference between conditions.

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/heldout-5x5-per-run.webp"
   alt="A log-scale dot plot with one dot per run and six conditions along the
        bottom. Every condition has runs up between about 250,000 and 960,000
        points and runs down at or below the random floor near 8,000, with only
        three dots anywhere in between. A dashed line marks the greedy baseline
        at 80,424 and a dotted line the random floor at 8,196. Four runs are
        drawn as crosses on the floor, meaning they could not play the board at
        all, and one dot is half-clipped by the bottom of the axis."
   caption="Panel B of Figure 2 of the powered report, reproduced as the report
            drew it, half-clipped dot and all. Thirty runs, five per condition,
            raw 5x5 score on a log axis. The labels are the report's own: ctrl
            is cautious, niet is expansive, and frz, sm and rad are the three
            self-modification levels. The spread inside a single condition
            covers two orders of magnitude, which is why five runs per cell
            cannot resolve a difference between conditions on this split."
%}

The reason is that 5×5 transfer is **near-binary**. A run either happens to keep
a board representation that works at any size, or it bakes the 4×4 shape into
its data structures for speed and is then structurally incapable of playing a
bigger board. There is almost nothing in between.

It is also not purely a lottery, and I should not have implied it was. A
commit-by-commit scan of the twenty self-modifying runs found twelve that ended
up able to play any board size. Three of those got there incidentally, as a free
by-product of vectorizing a 4×4 engine. The other nine did it on purpose, seven
of them by explicitly de-hardcoding the search and measuring what it bought. The
report's phrase is that attending to the untested size assumption is a real, if
uncommon, learned move.

So it is a near-binary decision that some runs make on purpose and others simply
fall into, and either way it dominates the score. My nine-run study sampled that
once per condition and read the pattern as signal. With one run per cell, I
could not have distinguished a real effect from that. The honest description of
the first result is not "wrong conclusion from good data": it is that the data
could never have supported the conclusion.

## What this cost and what it bought

Thirty runs and about $1,257 of logged compute, $886 for the twenty powered ones
and $371 more for the frozen ten, on top of the $515 the original nine runs had
already cost. The $1,257 is a floor, not an exact figure: one frozen run's log
recorded a cost for only eight of its fifteen iterations. What that bought was
the conversion of a satisfying story into a smaller and duller true one: **an
agent's stated disposition strongly shapes how good its code gets, and does not
detectably shape whether that code generalizes to a structurally different
problem.**

I only caught it because I went back. The first result was internally
consistent, had a plausible mechanism, and would have survived review by anyone
who did not re-run it. There is no version of me reading that write-up more
carefully and spotting the problem. The only thing that finds it is the second
experiment.
