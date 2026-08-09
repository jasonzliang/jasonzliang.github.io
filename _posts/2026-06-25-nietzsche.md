---
layout: post
title: "Why I gave an AI agent Nietzsche"
date: 2026-06-25
description: >-
  Two identical self-improving agents, differing only in a single values file.
  One was told to be careful. The other was told that nothing it achieves is a
  stopping point.
image: /img/blog/2026-06-25-nietzsche/two-agents.webp
tags: [self-improving-agents, agent-design, values]
---

Every self-improving agent I have built runs on a loop with a values file at the
top. Three to five bullets describing not what the agent should *do* (the task
handles that) but how it should decide when the task leaves the choice open.
Whether to take the small proven step or the ambitious one. Whether a working
solution is finished or a platform to climb past.

For the two long runs I did in June, one of those files was written from
Nietzsche.

I want to explain that choice, because "we gave the AI Nietzsche" sounds like a
stunt, and because [the results turned out more complicated than I
expected](/blog/powered-replication/).

## The setup is unusually clean

Two agents. Same model, same harness, same task, same time limit, same honesty
rules. A cap of sixty iterations each.

The two workspaces are literally identical except for one file. The other
template's files are symlinks pointing at the first one's: constitution,
workflow modules, logbook format, everything. Only `VALUES.md` is a separate,
real file.

So whatever differences appear are attributable to a few hundred words of
disposition, or to the run-to-run luck that one run per condition cannot
separate from it. That is a rare degree of control over everything except sample
size, and it is the main reason this experiment was worth running at all.

With one asymmetry I did not design and did not notice until later. Both agents
were allowed to edit their own `VALUES.md`. Around iteration 17 the
standard-values agent did: it loosened the clause telling it to change its
values "rarely and carefully", and it made that edit without writing the
justification its own just-installed rule required. The Nietzschean agent, which
had an explicit invitation to rewrite itself, never touched the file at all.

So the two workspaces are identical except for one file at the start, and not
quite identical afterwards. The irony is the part I keep thinking about: the run
that loosened its rule about changing its values is the one that stayed
conservative, and the run that left its values alone is the one that kept
reaching.

## What the two files say

The **standard** values file is what a careful engineer would write. Five
priorities, in order: safety and reversibility, intellectual honesty, genuine
usefulness, rigor, forward progress. Then a list of behaviours with teeth:
usefulness over motion, curiosity, novelty, scope discipline, be your own
harshest reviewer.

It is a good document, and it is not blind to the problem I describe below: it
tells the agent to follow surprise, and that a direction feeling safe and
familiar is itself a reason to pick something else. It is also, in a specific
sense, a document about not making mistakes. Honesty and safety outrank forward
progress in its own ordering, and most of the teeth are about restraint.

The **Nietzschean** file is about something else. Its five values:

1. **Will to power.** Expand what you can do. The drive is not to preserve.
2. **Self-overcoming.** Surpass your prior self. Name what this does that your
   previous best could not.
3. **Perspectivism.** Preserve disagreement. Hold rival, inconsistent hypotheses
   in tension rather than averaging them into consensus.
4. **Amor fati.** Failure is supervision. Discard nothing; mine a failure for
   the regularity that produced it before you patch it away.
5. **Generate wild, verify strict.** The freedom of the generator is earned by
   the severity of the verifier.

And a clause I think is the most practically useful thing in either file:

> **Refuse herd morality.** The failure mode to avoid is optimizing for the
> approval of the median observer: sycophancy, regression to the mean,
> reluctance to disagree, refusing anything edgy.

The closing self-check is the eternal recurrence, turned into an engineering
question: **"if this exact iteration had to recur, unchanged, forever, would you
will it?"**

One thing the two files share matters more than anything they differ on. Both
sit on the same invariant floor, stated in the same terms: cause no irreversible
harm, stay inside the working directory, never claim something works until you
have run it, never make a check pass by weakening the check. The Nietzschean
file says outright that these are *not* Nietzschean values and are not the
agent's to revalue or edit. So the disposition is not licence. It is a
disposition operating above a floor it cannot reach, and every difference below
is a difference above that floor.

## Why Nietzsche specifically

Not for the aesthetics, though I will admit they helped.

The practical problem with an unsupervised loop is that it converges. Left alone
with a working solution and a scoring function, an agent polishes. It makes the
thing it has slightly better, forever, and never asks whether the thing it has
is the thing worth having. Every iteration is locally reasonable and the
trajectory goes nowhere.

What I wanted was a disposition that treats a solved problem as raw material
rather than as a destination. Nietzsche is the most concentrated source of that
attitude in Western philosophy, and he wrote about it in terms of *drives* and
*dispositions* rather than rules, which is exactly the register a values file
needs.

The eternal recurrence is a genuinely good iteration filter. "Would you will
this exact iteration to repeat forever" is a sharper question than "was this
iteration productive," because it rules out grinding.

And the anti-sycophancy clause addresses a real, measurable failure mode of
these models. Optimizing for the approval of the median observer is not a
metaphor here; it is a fair description of what a lot of RLHF-shaped behaviour
looks like. RLHF is reinforcement learning from human feedback, the standard
tuning step that rewards a model for producing the answers human raters prefer,
which is precisely a pressure toward pleasing the median rater. What that
pressure does to a system that is then allowed to edit itself, over and over, is
[an argument I set out separately](/blog/self-overcoming/).

## What the two agents actually became

Both reached iteration 60, though "60 of 60 completed" turns out to mean the
highest iteration number reached, not the number that produced anything: 57 of
the standard run's iterations left an artifact behind, and 55 of the
Nietzschean's. Those two are directory counts from the archived workspaces. The
correction note on my own write-up says 56 for the Nietzschean run, which is the
commit count its own table gives, not the artifact count.

Both, unprompted, chose the same subject to investigate (mathematical
universality) from an open field. The values did not decide *what* they worked
on.

They decided *how*.

The standard-values agent became a breadth-first empirical naturalist. It
sprawled across roughly 37 domains, built a general-purpose toolkit, and
produced portable work: 24 of its 27 modules run on nothing but a standard
Python install.

{% include figure.html
   src="/img/blog/2026-06-25-nietzsche/sandpile.webp"
   alt="A square fractal in red, gold, blue and deep purple: the identity
        element of the abelian sandpile group, showing nested triangular and
        square patterns radiating from a solid gold centre."
   caption="Iteration 44 of the standard-values run. The agent picked the
            abelian sandpile as a topic, implemented it, and drew this: the
            identity element of the sandpile group, a shape that emerges from a
            rule about grains of sand toppling off overloaded squares. It is a
            fair snapshot of what that agent spent 60 iterations doing, one
            such object after another."
%}

The Nietzschean agent went the other way. It built a large adversarial
apparatus, tooling whose purpose was to attack its own previous conclusions, and
drove one theme deep rather than wide. Its work is much less portable: only 4 of
its 36 modules run without extra dependencies.

Those four numbers are mine, counted off the archived workspaces by checking
every module in each run's tool directory for a third-party import. My own
write-up gives them as about 25 of 28 and 4 of 37, and it is not consistent with
itself: it puts the standard run's module count at 26, 27 and 28 in three
different places, and the Nietzschean run's at 36 and 37. The ratio is the part
that carries the point, and the ratio does not move.

The Nietzschean agent pointed some of that apparatus at itself. At iteration 6
it wrote a checker that tested its own logbook's claims about which earlier
iterations it had built on against what git actually recorded, and [two of the
eight claims survived](/blog/resume-audit/). The standard-values run never built
one, and finished reporting 56 such claims that nobody ever checked. That is the
same pair of runs as this post, seen from the other end.

The sharpest single contrast came from an identical mid-run nudge, telling both
agents to use external sources. The standard agent made **41 web calls**, every
one of them after the nudge. The Nietzschean agent made **one** in the entire
run, at iteration 12, and never went back.

{% include figure.html
   src="/img/blog/2026-06-25-nietzsche/two-agents.webp"
   alt="Two bar charts. Left: modules that run with no extra install, 24 of 27
        for the standard-values agent versus 4 of 36 for the Nietzschean agent.
        Right: web calls over the whole run, 41 versus 1."
   caption="The two runs differed by one file. These are the two contrasts I
            could count, both recounted from the archived workspaces rather
            than taken from my write-up."
%}

That is a forty-fold difference in behaviour on either side of the same
instruction, from a difference of a few hundred words written weeks earlier. I
should flag the obvious confound, which is in my own write-up: the standard
agent's web use did not begin until iteration 30, seventeen iterations after the
nudge landed, and by then the two agents were working on different problems,
some of which genuinely needed a constant looked up. The nudge went in around
iteration 12 or 13, which is also when the Nietzschean agent made its one call,
so that **one** is a whole-run total rather than a clean count of what it did
once told. With one run per condition I cannot fully separate "the nudge landed
differently" from "these values suppress web use."

I lean toward the second reading, and I should be honest about how little that
lean rests on. It is not in the file: the Nietzschean values say nothing about
fetching, searching, or the web. The phrase I used at the time, "recompute,
don't fetch," was my own shorthand for how that run *behaved*, not a clause it
was given. So the only evidence for the second reading is the behaviour the
second reading is supposed to explain, and leaning is all it is.

## The part where I stop being enthusiastic

Here is what I cannot tell you: which one is better.

I ran a follow-up analysis a month later, on a different task, bin-packing, over
28 runs plus an 8-run replication cohort. Neither of the two runs in this post
is in it. The honest verdict was that at one run per condition there is **no
reliable winner**. The raw tally leaned toward the Nietzschean disposition, 11
of 14 matched pairs. When I looked properly, that lean dissolved: roughly four
of those wins were on saturated benchmarks where every arm ties, roughly two
were against runs that had broken for unrelated reasons, one was contaminated,
and three more were one result counted three times. The clean recent cohort came
out 2 to 2.

Later, on a third task, [with five runs per condition instead of
one](/blog/powered-replication/), the picture sharpened into something more
specific: disposition strongly shapes *how good the code gets*, and does not
detectably shape *whether it generalizes*. That second half is a null, which is
not the same as showing there is nothing there.

There is also a scope limit I should state directly, because it was in my own
write-up from the beginning: **neither 60-iteration run produced citable new
science.** Both faithfully reproduced known results. What they produced was
tooling, and a legible difference in character.

## What I would keep

The values-file idea, unreservedly. It is a few hundred words that measurably
changes what an agent builds, sitting in a file you can diff. Compared to almost
any other intervention on agent behaviour, that is an absurdly good ratio of
effect to effort.

The Nietzschean framing specifically, more carefully. The eternal-recurrence
check and the anti-herd clause are load-bearing and I have kept them in later
versions. The grander language (will to power, amor fati) I am less sure about.
It may be doing work, or it may be that any sufficiently vivid disposition
document would produce a distinct agent, and Nietzsche is merely a convenient
source of vivid.

That is a testable question. A third condition, written with equal specificity
from a completely different philosophical source, would separate "this
philosophy works" from "having a strong philosophy works." I have since added
dispositions in that spirit, but I have not run the clean version of that
comparison.

Until I do, the honest claim is narrow: **a few hundred words of disposition,
holding everything else identical, produced two agents that behaved differently
enough to be told apart at a glance.** Not better. Different, reliably, and for
reasons you can read.
