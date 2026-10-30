---
layout: post
title: >-
  Thirty 2048 runs separated a capability effect from generalization
date: 2026-08-23
description: >-
  Instructions encouraging exploration improved 2048 performance on the
  familiar board size, without a detectable advantage on a larger board.
image: /img/blog/2026-08-07-powered-replication/cliffs-delta.webp
tags: [self-improving-agents, replication, evaluation]
---

A nine-run experiment suggested that an agent's stated values improved
transfer to unfamiliar tasks, especially when the agent could rewrite those
values. A thirty-run follow-up narrowed that conclusion: **the expansive
instructions improved 2048 performance on 4×4 boards, but produced no detectable
advantage on an unseen 5×5 board**. Allowing values to change added no
significant capability benefit beyond the initial instructions.

## Task and conditions

Each agent wrote a program to play
[2048](https://en.wikipedia.org/wiki/2048_%28video_game%29), the game in which
matching tiles merge and contribute to a running score. The agent improved its
solver, committed changes, and received a new score each iteration. The first
experiment allowed twenty iterations; the replication allowed fifteen.

A [short disposition document](/blog/nietzsche/) varied the guidance. The
cautious condition emphasized small verified steps and reuse. The expansive
condition encouraged exploration, removing constraints, and developing broader
capabilities. A second factor controlled whether the agent could rewrite only
three value bullets, rewrite the document freely, or leave it frozen.

Evaluation covered the standard **4×4** games used during development and two
held-out tests. One kept the board size but increased the chance of a new
4-tile from 10% to 25%. The other changed the board to **5×5**, testing whether
code developed for 4×4 could handle a different shape.

The initial experiment had nine conditions with **one run each**. Its best
expansive solver scored roughly 800,000 on 5×5, revised to about 720,000 after
a truncation-free evaluation. On that board, random play scores about 8,000 and
greedy play about 80,000. The same greedy strategy scores about 4,500 on 4×4;
raw scores across board sizes therefore have different reference points.

## The replication results

The [pre-specified analysis](/blog/pre-registration/) covered twenty runs:
five per cell in a two-disposition by two-self-modification design. A follow-up
added ten frozen-value runs, five per disposition.

Cliff's delta compares pairs of **runs**: the fraction where the expansive run
scores higher minus the fraction where it scores lower. It ranges from −1 to
+1. A delta of +1 means every expansive run beats every cautious run; zero
means equal rates of higher and lower scores, allowing for ties. The
[unit of analysis](/blog/hub-vs-leaf/) is the run, rather than individual games.

| Evaluation, first twenty runs | Cliff's delta | p |
|---|---|---|
| Standard 4×4 development games | **+0.80** | 0.001 |
| Held-out 4×4, harder tile spawn | **+0.60** | 0.024 |
| Held-out 5×5 board | **−0.05** | 0.86 |

The [reported effect sizes and plotting code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-08-07-powered-replication/make_figs.py) record these comparisons.

The p-values are exact two-sided permutation tests. On development games,
expansive conditions averaged approximately **78,000–88,000**, compared with
**53,000–65,000** for cautious conditions. The harder spawn test retained a
substantial advantage. The 5×5 result supplied no evidence of an advantage;
it does not establish that the true effect is zero.

{% include figure.html
   src="/img/blog/2026-08-07-powered-replication/both-curves.webp"
   alt="Mean scores across fifteen iterations for six conditions, with
        standard-error bands and five runs per condition. Expansive conditions
        finish above cautious conditions on both standard and harder-spawn
        4×4 games."
   caption="All thirty runs appear here, including the ten frozen runs excluded
            from the table. Control means cautious; nietzsche means expansive.
            Frozen, sm and radical denote fixed, bounded-edit and unrestricted
            values. The lower panel tests a 4×4 spawn shift; 5×5 was evaluated
            separately at the endpoint."
%}

The capability advantage was a new finding, rather than a replication of the
original interpretation. That study had emphasized generalization and included
a third, deliberately [overfitting disposition](/blog/overfit/), which the
replication omitted. Its three runs had scored below the random baseline on
5×5, so that contrast remains untested here.

In the original study, 5×5 remained labelled a breadth check until about twelve
and a half hours after launch, when it was promoted to the primary endpoint.
On the endpoint designated beforehand, the best overfitting run generalized
better than the other eight runs. Selecting the endpoint after scoring made
the later broad claim about generalization exploratory.

## Frozen values retained the capability gap

The ten frozen runs tested the proposed
[self-modification mechanism](/blog/self-overcoming/). If rewriting values
were necessary to realize the performance advantage, freezing them should have
reduced it.

Instead, every frozen expansive run beat every frozen cautious run:
**delta +1.00**. The expansive cell averaged **91,518**, exceeding the means
of its self-modifying counterparts. Pooling all thirty runs gave a disposition
effect of **+0.86**. These results support an effect of the initial instructions
without evidence that value rewriting adds a further capability gain.

On 5×5, unrestricted rewriting was directionally worse than bounded rewriting
(delta 0.41 against it), but **p=0.14** does not establish a difference. None of
the ten frozen solvers was unable to play 5×5, compared with four of the twenty
self-modifying solvers; three failures occurred under unrestricted rewriting.
Those counts describe this sample rather than proving a general failure rate.

## Why five runs still leave uncertainty

Within every condition, 5×5 scores ranged from roughly **250,000–960,000**
to values at or below the random baseline of **8,196**, with little between.
Some strong solvers reached the CPU limit before their games ended. Those
games retained their partial scores, making the affected 5×5 results lower
bounds; this does not change the reported lack of a detectable disposition effect.
Board transfer depended heavily on representation: code that supported
variable board sizes could continue playing, while specialized 4×4 data
structures could prevent it entirely. This large within-condition variation
limits what five runs per cell can resolve.

A commit-level inspection found twelve of the twenty self-modifying runs
capable of arbitrary board sizes. Three acquired that ability incidentally;
nine added it deliberately, including seven that removed hardcoded assumptions
and measured the result. Such behavior occurred, but its frequency did not
produce a detectable disposition advantage on 5×5.

Logged spending was approximately **$1,257** for thirty runs: $886 for the
self-modifying twenty and $371 for the frozen ten, in addition to the original
study's $515. The replication total is a lower bound because one frozen run
logged costs for only eight of fifteen iterations.
