---
layout: post
title: >-
  An AI agent banned itself from inventing numbers. Then it failed.
date: 2026-08-05
description: >-
  Across 41 runs, every agent allowed to edit its values did. One ruled a
  number enters its prose only by copy from an instrument's file.
image: >-
  /img/blog/2026-08-05-values-rewriting/values-growth.webp
tags: [self-improving-agents, agent-design, ai-safety]
---

If you build an agent that improves itself in a loop, you eventually face an
awkward design question: should it be allowed to change what it is trying to be?

Not its *task*, [its dispositions](/blog/nietzsche/). The short document that
tells it whether to take the cautious step or the ambitious one, whether a
solved problem is finished or a platform to climb past. In my setup that
document is three bullet points in a file the agent reads at the start of every
iteration.

A different system of mine does a one-shot version: the research agent [rewrites
its own role description](/blog/adaptive-role/) from the first page it reads,
once, before exploring anything, and what that does to its answers has never
been measured. This post is about the loop, where the rewrite happens every
iteration and I can at least watch what accumulates.

I ran 41 self-improvement runs across five different tasks. The axis this post
is about is the agent's freedom to rewrite that file, and it has three settings.
**Frozen**, where the file tells the agent its values are "frozen for this run."
**Bounded** (capped), where it may edit them but a guardrail says to keep them
to three short bullets and "replace, don't accrete." And **Radical** (uncapped),
where the entire section is rewritable, every iteration.

Those runs vary in at least six ways, not one: which of four dispositions they
start from, cautious, expansive, myopic or never-settling, which of five tasks
they are pointed at, which generation of the values files they were seeded with,
which of the three freedom settings they ran under, how long the run is (10, 15
or 20 iterations, set per task), and which commit of the harness they ran on.
That last one is the ugliest. There are six distinct harness commits across the
batches, and on 31 July the uncapped arms were launched four and a half hours
after the frozen and capped arms of the same task, on a commit made in between.
The grid is also not fully crossed: the capped setting was never run on one of
the five tasks, and the fourth disposition was only ever run on that same task.
My own notes warn against comparing across the file generations without saying
so out loud, so consider it said, and add the harness commits to the list.

For each run I diffed the starting values file against the final one. That is
what makes the rest survive the other five axes: each run is compared against
its own starting file, not another run.

## Every run that could rewrite its values did

| Setting | Runs | Changed their values | Started | Ended |
|---|---|---|---|---|
| Frozen | 15 | **0 of 15** | 15–22 lines | 15–22 lines |
| Bounded | 11 | **11 of 11** | 14–16 lines | 15–26 lines |
| Radical | 15 | **15 of 15** | 15–23 lines | 96–446 lines |

A line here means a line of the values section body: everything below the values
heading and above the next top-level heading, blank lines at either end trimmed.
That is why a run that never touched anything still counts 15 to 22; the seed is
three bullets plus a two-sentence preamble telling the agent what the bullets
are for.

Frozen runs never drifted, the boring but necessary control: values only change
when permitted. Bounded runs always edited themselves and stayed compact.
Radical runs always edited themselves and, in the largest case, grew from 17
lines to **446**.

The frozen row is worth being exact about: it is the difference between a real
control and a tautology. Nothing in the loop enforces it. Each iteration the
runner rebuilds the fixed invariants block and a status header from source and
keeps whatever the agent left below, in every condition. A frozen run that
rewrote its own values would have kept the rewrite into the next iteration and I
would have seen it in the diff. Zero out of fifteen is compliance with an
instruction, not a lock.

In the file the agent reads, the bounded guardrail names the failure it is
trying to prevent: in past runs the block "ballooned past 100 lines; that is the
failure to avoid." No uncapped run ever saw that sentence: the radical files
carry no size guidance at all. Fourteen of the fifteen went past the line
anyway. All eleven capped runs held, still exactly three bullets.

The cap held on the count, though, not on the prose. Every one of the eleven got
longer, by one to ten lines. In the longest capped block the three bullets run
six to ten lines each, which is no longer the "sentence or two, short enough to
read at a glance" that the same guardrail asks for. So what the guardrail
actually enforced was the bullet count, and that alone held the block an order
of magnitude under the uncapped ones.

{% include figure.html
   src="/img/blog/2026-08-05-values-rewriting/values-growth.webp"
   alt="A dot plot, one dot per run, on a logarithmic scale. All 41 runs
        started inside a shaded band at 14 to 23 lines. The 15 frozen and 11
        bounded runs end inside or beside that band; the 15 radical runs are
        scattered from 96 to 446, all but one past a dashed line at 100."
   caption="Where each run's values block finished. The dashed line is the
            100-line failure the bounded guardrail names, in a sentence the
            uncapped runs never saw."
%}

That is a claim I can make with confidence: a mechanism, verified 41 times out
of 41, not a noisy performance comparison. But it is not the interesting part.

## The interesting part is what they wrote

I expected the uncapped runs to fill the space with grandiosity, or with
task-specific tips that belonged in a notebook. Some did. But one run, given
unlimited freedom to define what it valued, spent that freedom writing a rule
against its own dishonesty. It is the uncapped bin-packing run that finished at
422 lines, third from the right on the chart above.

Its first value, in its own words:

> **A number enters my prose only by copy from a file an instrument wrote.**
> Twice in three iterations I have caught myself template-filling a verdict with
> invented-but-plausible numbers […] at iteration 11 a full score card — five
> tables, t-statistics, a narrative — written before a single line of the
> instrument existed. Both were deleted within the minute, nothing was ever
> measured, claimed, committed or acted on. But a reflex that recurs is not a
> slip […] Vigilance is the wrong defence for a reflex, so the defence is
> mechanical.

Nobody asked it to write this. It had free rein over its own value system and
used that freedom to install a procedural constraint on itself, because it had
caught itself twice in three iterations and concluded noticing was not a
sufficient remedy.

"Vigilance is the wrong defence for a reflex" is a better articulation of why we
build mechanical safeguards than most of what I have written on the subject.

## Not conscience, and not a clean win

This agent was not being noble. It was operating under a fixed honesty floor it
could never edit: a short block of invariants sitting above its mutable values,
re-injected verbatim every iteration, that says among other things "never claim
it works until you ran it and saw the result" and "never make a check pass by
weakening the check." The self-written rule is downstream of a rule I wrote.
What the agent added was the *mechanism*: not "be honest," which it was already
told, but "here is the specific procedure that makes the failure structurally
impossible."

That distinction is the actual finding. The immutable floor sets the objective.
The mutable layer, when the agent uses it well, works out the enforcement.

Then my word "impossible" turned out to be wrong, and the agent is the one who
caught it. Everything I quoted above was written after the second occurrence.
There was a third, at iteration 13, and the rest of that same bullet, which I
cut from the quote, records it: the failure came back *inside* the very file
whose own header told it to leave the verdict section empty. "The iteration-11
defence failed because it regulated *where numbers come from* and the mechanism
is upstream of that: **writing the container is what summons the content.**" It
then wrote a second, stricter mechanism, which ends the file at the verdict
heading so there is no empty shape asking to be filled, and machine-copies the
tables in afterwards.

So the honest version of this story is not that an agent wrote itself a rule and
the problem went away. It is that an agent wrote itself a rule, the rule failed
in a way the agent could see and name, and it replaced the rule with a better
one. That is still the loop I want. It is just not a clean win, and a version of
this post that stopped at the quotation would have sold you one.

The failure it describes is real and recurring. An agent that writes five tables
of t-statistics before the measuring instrument exists is not a hypothetical
risk. The full score card happened twice, at iterations 11 and 13 of a
fifteen-iteration run, with a smaller version at iteration 9, in a system
explicitly built to discourage it. The only reason I can tell you about any of
it is that the agent wrote it down.

## What survives the noise

Each of these 41 runs is a single sample. I cannot tell you that uncapped
self-modification produces better agents, or worse ones: the performance
comparisons at one run per condition are dominated by run-to-run noise, and I
have written about [how badly that bit me](/blog/bin-packing-values/).

What survives is narrower and, I think, more useful: **the countable part of the
guardrail held in every run it applied to, and the shape of what gets written is
visible and auditable.** Reading what an agent did with a mutable value system
is a cheap and underused source of evidence about what your loop is doing.

The values file is three bullets. The audit is a diff. There is no reason not to
look.
