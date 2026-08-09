---
layout: post
title: "Given free rein, an agent wrote itself a rule against lying"
date: 2026-08-05
description: >-
  Across 41 self-improvement runs, agents allowed to edit their own value system
  always did. What they wrote was not what I expected.
image: >-
  /img/blog/2026-08-05-values-rewriting/values-growth.webp
tags: [self-improving-agents, agent-design, ai-safety]
---

If you build an agent that improves itself in a loop, you eventually face an
awkward design question: should it be allowed to change what it is trying to be?

Not its *task*, its dispositions. The short document that tells it whether to
take the cautious step or the ambitious one, whether a solved problem is
finished or a platform to climb past. In my setup that document is three bullet
points in a file the agent reads at the start of every iteration.

A different system of mine does a one-shot version of this. The research agent
[rewrites its own role description](/blog/adaptive-role/) from the first page it
reads, once, before it explores anything, and what that does to the answers it
writes has never been measured. This post is about the loop, where the rewrite
happens every iteration and I can at least watch what accumulates.

I ran 41 self-improvement runs across five different tasks. Those runs vary in
at least six ways, not one: which of four dispositions they start from, which of
five tasks they are pointed at, which generation of the values files they were
seeded with, how much freedom the agent has to rewrite the bullets, how long the
run is (10, 15 or 20 iterations, set per task), and which commit of the harness
they ran on. That last one is the ugliest. There are six distinct harness
commits across the batches, and on 31 July the uncapped arms were launched four
and a half hours after the frozen and capped arms of the same task, on a commit
made in between. The grid is also not fully crossed: the capped setting was
never run on one of the five tasks, and the fourth disposition was only ever run
on that same task. My own notes warn against comparing across the file
generations without saying so out loud, so consider it said, and add the harness
commits to the list.

The axis this post is about is the freedom one, and it has three settings.
**Frozen**, where the file tells the agent its values are "frozen for this run."
**Bounded**, where it may edit them but a guardrail says to keep them to three
short bullets and "replace, don't accrete." And **radical**, where the entire
section is rewritable wholesale, every iteration, with no cap.

Then I diffed what each run started with against what it finished with. That is
what makes the rest of this survive the other five axes: each run is compared
against its own starting file, not against another run.

## The result was completely clean

| Setting | Runs | Changed their values | Started | Ended |
|---|---|---|---|---|
| Frozen | 15 | **0 of 15** | 15–22 lines | 15–22 lines |
| Bounded | 11 | **11 of 11** | 14–16 lines | 15–26 lines |
| Radical | 15 | **15 of 15** | 15–23 lines | 96–446 lines |

A line here means a line of the values section body: everything below the values
heading and above the next top-level heading, with the blank lines at either end
trimmed. That is why a run that never touched anything still counts 15 to 22;
the seed is three bullets plus a two-sentence preamble telling the agent what
the bullets are for.

Frozen runs never drifted, which is the boring but necessary control: it
confirms the values only change when permitted. Bounded runs always edited
themselves and always stayed compact. Radical runs always edited themselves and,
in the largest case, grew from 17 lines to **446**.

One thing about that frozen row is worth being exact about, because it is the
difference between a real control and a tautology. Nothing in the loop enforces
it. Each iteration the runner rebuilds the invariants and a status header from
source and keeps whatever the agent left below them, in every condition. A
frozen run that rewrote its own values would have kept the rewrite into the next
iteration and I would have seen it in the diff. Zero out of fifteen is
compliance with an instruction, not a lock.

The bounded guardrail names the failure it is trying to prevent, in the file the
agent reads: in past runs the block "ballooned past 100 lines; that is the
failure to avoid." No uncapped run ever saw that sentence, because the radical
files carry no size guidance at all. Fourteen of the fifteen went past the line
anyway. All eleven capped runs held, every one of them still exactly three
bullets.

The cap held on the count, though, not on the prose. Every one of the eleven got
longer, by one to ten lines. In the longest capped block the three bullets run
six to ten lines each, which is no longer the "sentence or two, short enough to
read at a glance" that the same guardrail asks for. So the honest version is
that what the guardrail actually enforced was the bullet count, and the bullet
count alone was enough to keep the block an order of magnitude under the
uncapped ones.

{% include figure.html
   src="/img/blog/2026-08-05-values-rewriting/values-growth.webp"
   alt="A dot plot with one dot per run on a logarithmic scale. All 41 runs
        started inside a shaded band at 14 to 23 lines. The 15 frozen runs and
        11 bounded runs are still inside or beside that band at the end. The 15
        radical runs are scattered from 96 to 446, all but one of them past a
        dashed line at 100."
   caption="One dot per run, showing where its values block finished.
            Everything started inside the shaded band. The dashed line is the
            100-line figure the bounded guardrail names as the failure to
            avoid; the uncapped runs never saw that sentence, and only one of
            them stayed under the line."
%}

That is a satisfying result about guardrails, and it is the kind of claim I can
actually make with confidence: it is a mechanism, verified 41 times out of 41,
not a noisy performance comparison. But it is not the interesting part.

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

Read that again with the setup in mind. Nobody asked it to write this. It had
free rein over its own value system and it used that freedom to install a
procedural constraint on itself, because it had caught itself twice in three
iterations and concluded that noticing was not a sufficient remedy.

"Vigilance is the wrong defence for a reflex" is a better articulation of why we
build mechanical safeguards than most of what I have written on the subject.

## Why this is not a story about AI conscience

I want to be careful here, because it would be easy to oversell.

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
whose own header told it to leave the section empty. "The iteration-11 defence
failed because it regulated *where numbers come from* and the mechanism is
upstream of that: **writing the container is what summons the content.**" It
then wrote a second, stricter mechanism, which ends the file at the verdict
heading so there is no empty shape asking to be filled, and machine-copies the
tables in afterwards.

So the honest version of this story is not that an agent wrote itself a rule and
the problem went away. It is that an agent wrote itself a rule, the rule failed
in a way the agent could see and name, and it replaced the rule with a better
one. That is still the loop I want. It is just not a clean win, and a version of
this post that stopped at the quotation would have sold you one.

It is also worth saying plainly that the failure it is describing is real and
recurring. An agent that writes five tables of t-statistics before the measuring
instrument exists is not a hypothetical risk. The full score card happened
twice, at iterations 11 and 13 of a fifteen-iteration run, with a smaller
version at iteration 9, in a system explicitly built to discourage it. The only
reason I can tell you about any of it is that the agent wrote it down.

## What I would not conclude from this

Each of these 41 runs is a single sample. I cannot tell you that uncapped
self-modification produces better agents, or worse ones: the performance
comparisons at one run per condition are dominated by run-to-run noise, and I
have [written separately](/blog/powered-replication/) about how badly that bit
me when I tried.

What survives is narrower and, I think, more useful: **the countable part of the
guardrail held in every run it applied to, and the shape of what gets written is
visible and auditable.** If you give an agent a mutable value system, you can
read what it did with it. That is a cheap and underused source of evidence about
what your loop is actually doing.

The values file is three bullets. The audit is a diff. There is no reason not to
look.
