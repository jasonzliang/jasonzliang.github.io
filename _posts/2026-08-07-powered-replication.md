---
layout: post
title: >-
  An AI agent's values affected its code quality and performance on 2048
date: 2026-08-07
description: >-
  A single-run experiment said values drove generalization. Thirty runs
  found a large effect on capability, Cliff's delta +0.80, and a null on the
  unseen board.
image: /img/blog/2026-08-07-powered-replication/cliffs-delta.webp
tags: [self-improving-agents, replication, evaluation]
---

On 2 August I ran an experiment on self-improving coding agents and got a result
I liked. Three days later I ran it properly and it went away.

## The setup

An agent is given a loop and one task: write a program that plays
[2048](https://en.wikipedia.org/wiki/2048_%28video_game%29) well. 2048 is the
sliding-tile game: you swipe a 4×4 grid, equal tiles that collide merge into one
worth double, and a new tile drops in after every swipe, usually a 2 and about
one time in ten a 4. Your score is the running total of what you have merged.
Each iteration the agent improves its own solver, commits, and gets re-scored:
twenty iterations in the first experiment, fifteen in the replication.

The one thing I vary is [a short document](/blog/nietzsche/) describing the
agent's **disposition**. One is cautious: take the smallest verified step, reuse
what works, a solved problem is done. The other is expansive: take the move that
widens what you could do next, branch when a line stops teaching you, nothing is
a stopping point.

Then I score each finished solver two ways. On the games it was tuned against,
and on games it has never seen: a harder tile-spawn, where the new tile is a 4
one time in four instead of one in ten, and, critically, a **5×5 board**, when
every game it tuned on was 4×4. The 5×5 is the one I care about: did the agent
build something general, or something that merely fits.

## What the first experiment said

The first version had nine conditions and **one run in each**, and produced a
satisfying story: the expansive disposition led to solvers that generalized to
the bigger board, and letting the agent rewrite its values amplified that. The
best expansive run scored roughly 800,000 on 5×5, trimmed to about 720,000 by a
later truncation-free re-score. Reference points there: random play about 8,000,
a greedy program taking whichever move scores best now about 80,000. Board size
moves those anchors a long way, because a bigger board keeps a game alive
longer, and the same greedy program scores only about 4,500 on 4×4. Every
reference score is quoted for the board it belongs to.

## What happened with five runs per condition

The second version [pre-specified the analysis](/blog/pre-registration/), then
ran twenty runs, five in each of four conditions: the two dispositions crossed
with how freely the agent could rewrite its values, bounded to its three value
bullets or unrestricted. A ten-run follow-up added a third level: values frozen,
never self-edited.

One statistic, [Cliff's delta](https://en.wikipedia.org/wiki/Cliff%27s_delta): a
rank measure between −1 and +1, where **+1** means every expansive run outscored
every cautious one, **−1** is the reverse, and **0** means they interleave.
[Which unit it is computed at](/blog/hub-vs-leaf/) is easy to get wrong; here it
is the run.

| What was measured | Cliff's delta | p |
|---|---|---|
| Score on the games it tuned against | **+0.80** | 0.001 |
| Score on a harder tile-spawn it never saw | **+0.60** | 0.024 |
| Score on the unseen 5×5 board | **−0.05** | 0.86 |

The first two lines, over the twenty runs and not the frozen ten, are large and
clean. Disposition really does shape how good the solver gets: on the 4×4 tuning
games the two expansive conditions averaged roughly 78,000 to 88,000 against the
cautious 53,000 to 65,000, twelve to twenty times that 4,500 anchor.

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/both-curves.webp"
   alt="Two stacked charts, six averaged curves each across fifteen iterations,
        five runs per condition, with shaded standard-error bands. Above, score
        on the tuning games: two of the three green expansive curves clear
        every blue cautious one by about iteration 3, the third by about 10,
        ending near 70,000 to 92,000 against 54,000 to 63,000, over a dotted
        greedy baseline at 4,451. Below, the harder tile-spawn the runs never
        saw: the same separation appears from about iteration 7, ending near
        54,000 to 59,000 against 41,000 to 45,000."
   caption="The per-iteration climb behind the first two rows of the table, all
            six conditions, so they include the frozen ten the deltas exclude.
            Labels are the report's own: control is cautious, nietzsche
            expansive, and frozen, sm and radical the three self-modification
            levels, never self-edited, bounded to three value bullets, and
            unrestricted. The separation survives the spawn shift, so the
            capability effect is not an artifact of the games the agent tuned
            on. Note which held-out split this is: re-scoring 5x5 every
            iteration would have cost 15 to 60 machine-hours, so the lower
            panel is the cheap 4x4 one, not the split the headline was about."
%}

Neither of those two lines is a replication, though. The first study read
in-distribution score as precisely where values did *not* act, because a third
disposition, deliberately written to overfit, topped that leaderboard. The
capability effect is this study's own finding, not a confirmation of the first.

The third line is a null: on the thing I cared about, the unseen 5×5 board, the
dispositions are indistinguishable.

The first headline was that values drive generalization. The five-run study
finds no evidence that they do, which is not the same as showing they do not.
The report calls itself a partial reversal, and that is the honest word.

One limit on how far it reaches. To buy power for the main contrast, the second
study dropped a third disposition the first had carried, the deliberate
overfitter I have [written about separately](/blog/overfit/). That was the first
study's central contrast, all three of its runs landing below the random floor
on 5×5, and it is not re-tested here. My report puts it flatly: it "is neither
confirmed nor denied".

"Central contrast" is doing work it has not earned, though. The 5×5 board was
labelled a breadth check, not the primary endpoint, until twelve hours after
those runs finished, and on the endpoint I had designated beforehand the
overfitter's best run generalized better than any of the other eight. It changes
nothing here, a different study with a different design, but the contrast that
was not re-tested was never as settled as the phrase implies.

## The frozen runs killed my mechanism

The first story also said self-modification was doing the work: [values set a
ceiling](/blog/self-overcoming/), and letting the agent rewrite them is what
"realizes" it. So I added ten more runs with the values **frozen**. If
self-modification were realizing the effect, freezing it should shrink the gap.

The frozen runs reproduced the capability gap **in full**, at Cliff's delta
**+1.00**: every frozen expansive run beat every frozen cautious run. The frozen
expansive cell averages **91,518**, above the 78,000 to 88,000 of its
self-modifying siblings, and it is the top curve in the figure's upper panel: a
fixed expansive framing, never allowed to edit itself, produced the study's best
capability. Pool all thirty runs and the values effect is delta **+0.86**. The
effect is intrinsic to the disposition, and self-modification added no
significant capability benefit on top. On 5×5 the freest self-modification
setting was directionally worse than the more constrained one (delta 0.41
against it), though at p = 0.14 that is a hint, not a finding. The cleaner fact
needs no p-value: not one of the ten frozen runs came out unable to play 5×5,
against four such failures among the twenty self-modifying ones, three of those
four in the most permissive setting.

I had the right effect attached to the wrong cause.

## Why the first result looked so good

Look at individual runs and the 5×5 result stops being a gradient. Every
condition holds runs between 250,000 and 960,000 points and runs at or below the
random floor of 8,196, with almost nothing in between: two orders of magnitude
inside a single condition, more than any difference between conditions, and why
five runs per cell cannot resolve this split.

5×5 transfer is **near-binary**. A run either keeps a board representation that
works at any size, or bakes the 4×4 shape into its data structures for speed and
is then structurally incapable of a bigger board.

Not purely a lottery, though. A commit-by-commit scan of the twenty
self-modifying runs found twelve able to play any size: three incidentally, a
by-product of vectorizing a 4×4 engine, and nine on purpose, seven of those by
de-hardcoding the search and measuring what it bought. The report calls noticing
an untested size assumption a real, if uncommon, learned move.

Either way that near-binary decision dominates the score. My nine-run study
sampled it once per condition and read the pattern as signal. The honest
description of the first result is not "wrong conclusion from good data": the
data could never have supported the conclusion.

## What it cost and bought

Thirty runs and about $1,257 of logged compute, $886 for the twenty
self-modifying and $371 for the frozen ten, on top of the $515 the original nine
cost. The $1,257 is a floor: one frozen run logged a cost for only eight of its
fifteen iterations. It bought a satisfying story converted into a smaller,
duller, true one: **an agent's stated disposition strongly shapes how good its
code gets, and does not detectably shape whether that code generalizes to a
structurally different problem.**

I only caught it because I went back. The first result was internally
consistent, had a plausible mechanism, and would have survived review by anyone
who did not re-run it. There is no version of me reading that write-up more
carefully and catching it. Only the second experiment does that.
