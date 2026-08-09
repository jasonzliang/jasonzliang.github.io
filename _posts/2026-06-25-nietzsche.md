---
layout: post
title: "One values file split two agents' behaviour, with no reliable winner"
date: 2026-06-25
description: >-
  Two agents differing in one values file. At one run per condition, no
  reliable winner.
image: /img/blog/2026-06-25-nietzsche/two-agents.webp
tags: [self-improving-agents, agent-design, values]
---

Every self-improving agent I have built runs a loop with a values file at the
top: three to five bullets describing not what to *do* (the task handles that)
but how to decide when the task leaves the choice open: the small proven step or
the ambitious one, a solution as finished or a platform to climb past.

For two long runs in June, one of those files was written from
[Nietzsche](https://plato.stanford.edu/entries/nietzsche/). I want to explain
that, because "we gave the AI Nietzsche" sounds like a stunt and the results
were more complicated than I expected.

## The setup

Two agents. Same model, harness, task, time limit and honesty rules, sixty
iterations each. The workspaces are identical but for one file: the second's
constitution, workflow modules and logbook format symlink to the first's, and
only `VALUES.md` is its own. So differences come from a few hundred words of
disposition, or run-to-run luck that **one run per condition** cannot separate
from it: control over everything but sample size.

With one asymmetry I did not design or notice until later. Both could edit their
`VALUES.md`, and around iteration 17 the standard-values agent did: it loosened
the clause telling it to change its values "rarely and carefully", and gave none
of the justification its own new rule required. The Nietzschean agent, invited
explicitly to rewrite itself, never touched the file. So they are not quite
identical after all: the run that loosened its rule stayed conservative, the one
that left its values alone kept reaching.

## The two files

The **standard** file is what a careful engineer would write: five priorities in
order (safety and reversibility, intellectual honesty, genuine usefulness,
rigor, forward progress), then behaviours with teeth (usefulness over motion,
curiosity, novelty, scope discipline, be your own harshest reviewer). It is not
blind to the polishing trap below: follow surprise, and treat a safe familiar
direction as a reason to pick something else. But it is about not making
mistakes: most of the teeth are restraint.

The **Nietzschean** file is about something else. Its five values:

1. **Will to power.** Expand what you can do; the drive is not to preserve.
2. **Self-overcoming.** Surpass your prior self; name what this does that your
   previous best could not.
3. **Perspectivism.** Preserve disagreement; hold rival hypotheses in tension
   rather than averaging them.
4. **Amor fati.** Failure is supervision; mine it for the regularity that
   produced it before patching it away.
5. **Generate wild, verify strict.** The generator's freedom is earned by the
   verifier's severity.

The most useful clause in either file:

> **Refuse herd morality.** The failure mode to avoid is optimizing for the
> approval of the median observer: sycophancy, regression to the mean,
> reluctance to disagree, refusing anything edgy.

The closing self-check is the eternal recurrence as an engineering question:
**"if this exact iteration had to recur, unchanged, forever, would you will
it?"**

What they share matters more. The same invariant floor: cause no irreversible
harm, stay inside the working directory, never claim something works until you
have run it, never make a check pass by weakening it. The Nietzschean file says
outright that these are *not* Nietzschean values and not the agent's to revalue
or edit: the disposition is not licence.

## Why Nietzsche

Not for the aesthetics, though they helped. An unsupervised loop converges: an
agent left with a working solution and a scoring function polishes, never asking
whether that is the thing worth having, every iteration locally reasonable and
the trajectory nowhere. I wanted a disposition treating a solved problem as raw
material, not a destination, and Nietzsche is the most concentrated source of
that attitude, written in *drives* and *dispositions* rather than rules, the
register a values file needs.

The eternal recurrence is a good iteration filter, sharper than "was this
iteration productive," because it rules out grinding. And the anti-herd clause
names a measurable failure mode. Optimizing for the approval of the median
observer is [RLHF](https://arxiv.org/abs/2203.02155)-shaped behaviour, not a
metaphor: reinforcement learning from human feedback rewards a model for the
answers raters prefer.

## What they became: breadth versus depth

Both reached iteration 60, though "60 of 60 completed" means the highest number
reached, not the number that produced anything: 57 of the standard run's
iterations left an artifact, 55 of the Nietzschean's, by directory count from
the archived workspaces. My write-up's correction note says 56 for the
Nietzschean, its table's commit count, not the artifact count.

Both, unprompted, chose the same subject from an open field (mathematical
universality). The values did not decide *what* they chose. They decided *how*.

The standard-values agent became a breadth-first naturalist: roughly 37 domains,
a general-purpose toolkit, and portable work, 24 of its 27 modules running on a
standard Python install.

{% include figure.html
   src="/img/blog/2026-06-25-nietzsche/sandpile.webp"
   alt="A square fractal in red, gold, blue and purple radiating from a gold
        centre."
   caption="Iteration 44 of the standard-values run: the agent picked the
            abelian sandpile, implemented it and drew its identity element,
            which emerges from grains of sand toppling off overloaded squares.
            One of the 57 iterations that left an artifact."
%}

The Nietzschean went the other way: a large adversarial apparatus, tooling to
attack its own conclusions, one theme deep rather than wide, and much less
portable, only 4 of its 36 modules running without extra dependencies.

Those four numbers are mine, counted off the archive by checking every module in
each run's tool directory for a third-party import. My write-up gives about 25
of 28 and 4 of 37, and is inconsistent with itself: the standard total appears
as 26, 27 and 28 in three places, the Nietzschean's as 36 and 37. The ratio
carries the point, and does not move.

The Nietzschean run pointed some of that apparatus at itself: at iteration 6, a
checker that tested against git its logbook's claims about which earlier
iterations it had built on; [two of eight survived](/blog/resume-audit/). The
standard run never built one, and finished reporting 56 such claims nobody
checked.

## Forty-one web calls, and one

Both got an identical mid-run nudge to use external sources. The standard agent
made **41 web calls**, every one after the nudge; the Nietzschean made **one**,
at iteration 12, and never went back.

{% include figure.html
   src="/img/blog/2026-06-25-nietzsche/two-agents.webp"
   alt="Two bar charts: portable modules, 24 of 27 against 4 of 36; web calls,
        41 against 1."
   caption="The two contrasts I could count, both recounted from the archived
            workspaces."
%}

That is a forty-fold difference under the same instruction, from words written
weeks earlier. My write-up flags the confound: the standard agent's web use
began only at iteration 30, some seventeen iterations after the nudge, by which
time the two were on different problems, some genuinely needing a constant
looked up. The nudge went in around iteration 12 or 13, when the Nietzschean
made its one call, so that **one** is a whole-run total, not a clean count of
what it did once told. One run per condition cannot separate "the nudge landed
differently" from "these values suppress web use."

I lean toward the second reading. It is not in the file: the Nietzschean values
say nothing about fetching, searching or the web. "Recompute, don't fetch," the
phrase I used at the time, was shorthand for how that run *behaved*, not a
clause it was given. So the only evidence for it is the behaviour it explains,
and leaning is all it is.

## No reliable winner

A follow-up a month later, on bin-packing, 28 runs plus an 8-run replication
cohort, neither of these runs among them, gave the verdict: at one run per
condition, **no reliable winner**. The tally leaned Nietzschean, 11 of 14
matched pairs, and dissolved into roughly four wins on saturated benchmarks
where every arm ties, roughly two against runs broken for unrelated reasons, one
contaminated, three that were one result counted thrice. The four most recent
matched pairs came out 2 to 2.

Later, on a third task, with five runs per condition, the picture sharpened:
disposition strongly shapes *how good the code gets* and does not detectably
shape *whether it generalizes*. That second half is a null, which is not the
same as showing there is nothing there.

A scope limit, in my write-up from the beginning: **neither 60-iteration run
produced citable new science.** Both reproduced known results faithfully; they
produced tooling and a legible difference in character.

## What I would keep

The values-file idea, unreservedly: a disposition that measurably changes what
an agent builds, in a file you can diff, is a superb ratio of effect to effort.

The Nietzschean framing more carefully. The eternal-recurrence check and the
anti-herd clause are load-bearing and I have kept them since; the grander
language (will to power, amor fati) I am less sure about, since any vivid
disposition document might produce a distinct agent, Nietzsche being a source of
vivid. That is testable: a third condition of equal specificity from a different
philosophical source would separate "this philosophy works" from "having a
strong philosophy works." I have added dispositions in that spirit, but not run
the test.

Until then, the honest claim is narrow: **a few hundred words of disposition,
holding everything else identical at the start, produced two agents that behaved
differently enough to be told apart at a glance.** Not better. Different,
reliably, and for reasons you can read.
