---
layout: post
title: >-
  A values-file comparison repeated two patterns, with major confounds
published: false
date: 2026-07-02
description: >-
  Some behavioral differences recurred, but letting agents choose their own
  problems left the values comparison unresolved.
image: >-
  /img/blog/2026-07-02-same-two-agents/what-replicated.webp
tags: [self-improving-agents, values, replication]
---

Four June runs compared a standard values file with a
[Nietzsche-inspired alternative](/blog/nietzsche/) on two research mission
catalogs. An initial report called the comparison a replication. Two of five
recorded patterns did repeat, but the agents chose different problems and set
their own success criteria. A runner change also removed one of the largest
observed differences between missions.

These runs do not establish that either values file caused a distinctive
research style or better results.

## Four runs, four self-chosen tests

In focused mode, the agent selected a research repository from a curated list,
copied the relevant material into its workspace and built an offline benchmark.
It recorded a numeric target in `CRITERION.md`, then froze the benchmark.
Later iterations changed one lever at a time, with refuter agents instructed to
challenge the resulting claims.

Mission 1 used 50 iterations with a 40-minute cap on 23 June. Mission 2 used
40 iterations with a 60-minute cap on 24 June. Within each mission, both
conditions used the same model and protected honesty rules. The intended
intervention was the values file, but **each run selected its own target and
bar**.

All four passed a six-part integrity check at run time, including checks on
frozen graders and git history. Their per-run `.git` directories were
[removed during archival](/blog/resume-audit/), so the history-dependent
checks are historical observations that cannot now be repeated.

The standard-values run cleared its own bar at iteration **5** in mission 1
and iteration **4** in mission 2. The alternative never cleared its initial
bar in either mission. In mission 1 it selected the stronger of two candidate
baselines as its target; in mission 2 it missed the bar by 0.003.

A pass on one self-selected problem and a miss on another do not establish
relative capability. Target selection may itself be interesting behavior, but
this design does not separate its effects
from differences in the underlying problems.

## Which measurements repeated

{% include figure.html
   src="/img/blog/2026-07-02-same-two-agents/what-replicated.webp"
   alt="Five comparisons across two missions: clearing a self-set bar, frozen
        benchmark count, shared modules, task-log lines and root-level Python
        files. Only the first two repeat the same directional difference."
   caption="Two descriptive patterns repeated across missions. Each cell has
            one run, and the runs chose different targets. The chart does not
            establish an effect caused by the values file."
%}

The standard-values run cleared its own bar on both missions. The alternative
also left more frozen benchmarks on both: **10 versus 1** in mission 1 and
**13 versus 6** in mission 2. Neither alternative run lowered the initial bar
it failed to clear.

The other three measures did not show a consistent separation:

- **Shared tool modules:** standard versus alternative was 1 versus 1 on
  mission 1, then 0 versus 2 on mission 2.
- **Python scripts at the workspace root:** 0 versus 39 became 0 versus 0.
- **Task-log lines:** 869 versus 852 on mission 1, then 2,481 versus 3,055 on
  mission 2.

The [plotting data and code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-07-02-same-two-agents/make_figs.py#L13-L44)
record the five reported comparisons and their counting rules.

Three hours before mission 2, the runner regained a workspace-layout sweep at
review checkpoints, prompted by the 39 loose scripts from mission 1. That intervention prevents
attributing the disappearance of the gap to either agent's disposition.

The mission-2 log count also needed correction. The standard run archived its
first fifteen iterations, moving 994 lines into `TASKS_DONE_archive/`. Counting
only the current file gives 1,487, an incomplete total previously compared
with the alternative's 3,055. Including the archive gives 2,481. Log length
also measures verbosity and recordkeeping, rather than research quality.

Extra benchmarks may represent broader exploration, or harder variants of a
particular selected problem. With one run
per cell and different targets, the archive cannot distinguish those explanations.

## What remains unresolved

Later internal checks confirmed the recorded counts without identifying a
values effect. The initial replication claim remained confounded by target
choice, while a later claim that the values changed only vocabulary was also
too broad. Neither interpretation resolves what caused the observed differences.

Completion also differed. Both mission-1 runs were resumed through API outages.
Mission 2's standard run lost iterations 25 and 26 to overload errors without
retries. Only mission 2's alternative completed all 40 iterations cleanly in
one session, so equal iteration ceilings did not provide equal completed work.

A stronger replication would fix the starting problem and evaluation, hold the
runner and iteration budget constant, and repeat each condition across seeds.
The four runs document the benchmark choices and runner intervention, while
leaving the values comparison unresolved. Later studies on other tasks do not
resolve these confounds.
