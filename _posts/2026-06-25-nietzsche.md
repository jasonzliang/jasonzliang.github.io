---
layout: post
title: >-
  Two AI agents differing by one values file, with no reliable winner
date: 2026-06-25
description: >-
  One agent explored broadly while another built a connected project with
  extensive checks; the values comparison remains inconclusive.
image: /img/blog/2026-06-25-nietzsche/two-agents.webp
tags: [self-improving-agents, agent-design, values]
---

Two coding agents began with the same model, harness, task, rules and
per-iteration time limit. The planned difference was `VALUES.md`: a document
describing how to choose work when the task left room for judgment. One file
emphasized safety, honesty,
usefulness and rigor. The other adapted themes from
[Nietzsche](https://plato.stanford.edu/entries/nietzsche/).

The standard-values run explored broadly and built portable tools. The
Nietzsche-inspired run concentrated on a connected mathematical theme and built
many tools for checking calculations. With **one run per condition**, the
experiment cannot separate a values-file effect from ordinary variation between
runs.

## What the files changed

Both agents used fresh sessions, recovering context from files rather than
conversation memory. They shared the constitution, workflow modules and
logbook format; only the values file was separate. Both had the same protected
rules: work within the directory, avoid irreversible harm, run checks before
claiming success and never weaken a check to obtain a pass.

The standard file prioritized safety and reversibility, intellectual honesty,
usefulness, rigor and forward progress. It also encouraged curiosity, novelty
and criticism of earlier work. It therefore encouraged exploration as well as
caution.

The alternative organized its guidance around five themes:

1. **Will to power:** expand the capabilities available to later iterations.
2. **Self-overcoming:** identify an improvement over the previous approach.
3. **Perspectivism:** preserve rival hypotheses until evidence resolves them.
4. **Amor fati:** extract reusable lessons from failure.
5. **Generate wild, verify strict:** allow ambitious proposals while retaining
   firm acceptance checks.

It also discouraged conformity. Its eternal-recurrence check asked whether
the agent would choose to repeat the exact iteration unchanged forever,
including whether the work had expanded capability or merely filled time.
These were engineering adaptations, rather than claims that Nietzsche supplied
an algorithm for coding agents.
The anti-conformity language also reflected concerns about
[human-preference training](https://arxiv.org/abs/2203.02155), a process this
experiment did not test. The files differed in operational instructions as well
as tone, so the comparison cannot isolate philosophical vocabulary alone.

Both agents could edit their values. The standard run loosened its instruction
to make changes rarely and carefully; the alternative left its file unchanged.
An earlier write-up placed that edit around iteration 17. The archived runner
log instead locates it around iteration 44, without a corresponding justification
in the task log. The initial values files were starting points that the agents
could change during the run.

## Breadth, depth and dependencies

Both runs reached iteration 60. Directory counts show artifacts from **57
standard-values iterations and 55 Nietzsche-inspired iterations**. These are
artifact counts, distinct from the highest iteration reached or the number of
commits. The source report's later correction gives 56 for the second run,
although its own table lists 55 artifacts and 56 commits.

Both selected mathematical universality as a broad subject. The standard run
covered roughly 37 domains and assembled a general-purpose toolkit. A scan of
its 27 Python tool modules found 24 without third-party imports.

{% include figure.html
   src="/img/blog/2026-06-25-nietzsche/sandpile.webp"
   alt="A square abelian-sandpile identity pattern in red, gold, blue and purple."
   caption="The standard-values run's iteration-44 sandpile identity. The
            artifact reproduced a known mathematical construction and was one
            of 57 iterations that left an artifact directory."
%}

The alternative developed one connected universality project and more tools for
cross-checking its calculations. Only 4 of its 36 modules lacked third-party
imports. This is a dependency measure; it does not by itself establish that
every module works on a fresh installation. The original report gives
inconsistent module totals, so these figures use the archived directories.

At iteration 6, that run also built a checker for its logbook's claimed lineage.
Two of eight links were confirmed, three unsupported and three contradicted.
The standard run ended with 56 parsed build-on links without a comparable code
history audit. The unpublished lineage analysis explains why those
two counts measure different things and why neither establishes total reuse.

## External searches differed too

Both agents received the same mid-run instruction to consult external sources.
The archived runner logs contain **41 web calls** for the standard run and
**one** for the Nietzsche-inspired run.

{% include figure.html
   src="/img/blog/2026-06-25-nietzsche/two-agents.webp"
   alt="Two exploratory runs: modules without third-party imports were 24 of
        27 versus 4 of 36; whole-run web calls were 41 versus one."
   caption="Counts from the archived workspaces. Dependency scanning provides
            a portability proxy. Web-call totals cover each entire run and
            cannot isolate a response to the mid-run instruction."
%}

All 41 standard-run calls occurred after the instruction, beginning at iteration 30. The alternative's single call occurred at iteration 12, around the time of
the instruction. By iteration 30 the agents were pursuing different problems,
some requiring external constants. These totals therefore cannot establish
that the alternative values suppressed web use. Neither file prohibited search.

The [plotting data and code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-06-25-nietzsche/make_figs.py#L12-L27)
record the reported module and web-call counts above.

## What this exploratory pair establishes

Neither run established a new scientific result. Both reproduced known results and
left useful tools. The archive supports the behavioral descriptions above; it
does not support a reliable ranking or a general causal claim about values.

Later experiments asked related questions under different conditions. A
bin-packing series included 28 runs and an eight-run follow-up; an apparent
11-of-14 matched-pair advantage weakened under review: roughly four nominal
wins came from saturated benchmarks, two from unrelated failures, one comparison
was contaminated and three counted one result repeatedly. The latest four pairs
split 2–2. A separate [2048 study with repeated runs](/blog/powered-replication/) found a capability
difference without detectable transfer to a larger board. Those studies do not
replicate this open-ended mathematics pair.

A stronger test would repeat the comparison across seeds and include a third
values document of similar specificity. That could separate the contribution of
this particular framing from the broader effect of detailed instructions.
The two runs show different working styles, without establishing a winner.
