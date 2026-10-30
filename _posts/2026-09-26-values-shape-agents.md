---
layout: post
title: Values Shape What Self-Improving Coding Agents Build
date: 2026-09-26
description: >-
  Short, persistent instructions changed the algorithms coding agents
  developed, with guidance favoring exploration generally outperforming
  guidance favoring small, verified changes.
image: /img/blog/values-shape-agents/value-findings.svg
tags: [self-improving-agents, agent-design, research]
---

A coding benchmark specifies a target, but leaves many decisions open. An agent
can refine an existing algorithm, replace it, explore several approaches, or
stop once a solution seems adequate. Those choices can accumulate when each
coding session inherits the previous session's work.

[Values Shape What Self-Improving Coding Agents Build](/papers/values-shape-self-improving-coding-agents.pdf),
by Jason Liang, Dylan Waldner, and Risto Miikkulainen, tests whether short,
persistent value statements steer that process. Across six tasks, changing the statement
changed both performance and the programs produced. The strongest recurring
contrast was between instructions encouraging transformation and instructions
favoring small, verified steps.

## What changes during self-improvement

The agent improves a *solver*: a program that handles the benchmark task. Each
run contains 15 fresh coding sessions, each lasting up to 30 minutes. A session
reads the instructions and earlier notes, chooses a change, implements and tests
it, records the result, and commits its work. Only committed files survive into
the next session; conversational memory does not.

The main experiment keeps the Claude Opus 5 model, harness, task package,
starting solver, and safety rules fixed. Values are restored at every session.
The agent can rewrite solver code and tools, but cannot redefine the benchmark
or scoring rules. A separate scorer evaluates saved solvers after the run using
held-out data kept outside the agent's workspace.

{% include figure.html
   src="/img/blog/values-shape-agents/improvement-loop.svg"
   alt="Schematic of the fixed-values experiment. Each fresh session reads
        restored instructions and committed files, edits and tests the solver,
        then commits code and notes for the next session. A separate scorer
        evaluates saved solvers on held-out data after the run."
   caption="The main experiment changes the value statement between runs while
            keeping it fixed within each run. Code and notes accumulate through
            commits; held-out scores provide no feedback during development."
%}

Four statements adapt the higher-order categories in [Schwartz's theory of human
values](https://scholarworks.gvsu.edu/orpc/vol2/iss1/11/). **Openness** favors new representations, algorithms, and continuing
transformation. **Conservation** favors proven methods, minimal changes, and
settled solutions. **Self-enhancement** emphasizes demonstrable achievement
against an external benchmark. **Self-transcendence** emphasizes usefulness to
others, understandable artifacts, and restraint in resource use.

The statements have similar lengths and formats. Two controls use either a
short statement assigning no inherent values or similarly sized off-task text
about sensory preferences. Each of the six conditions has ten independent runs
on each task.

| Task | Solver objective and held-out test |
|---|---|
| ALE-Bench, AHC039 | Optimize a constrained polygon; test on 150 private cases. |
| Circle Packing | Maximize summed circle radii; transfer from visible odd sizes to 38 unseen even sizes. |
| Entity Matching | Identify matching product records; test on previously unseen product entities. |
| Game 2048 | Maximize merged-tile score; test on 30 fresh game seeds. |
| Symbolic Regression | Discover mathematical expressions; test inputs outside the training range on 129 known problems. |
| SZ-Tetris | Clear rows using only S and Z pieces; test on 100 fresh game seeds. |

## Results: performance and solver design

Openness has the highest final mean on five tasks; self-enhancement leads on 2048. Pooling scores after standardizing within each task, openness outperforms
the no-values control, while conservation and self-transcendence score below it.
The clearest opposing pair is openness versus conservation.

Openness's individual advantages over the no-values control reach statistical
significance on ALE-Bench and Circle Packing, rather than all six tasks. No value statement
differs significantly from that control on Symbolic Regression.

<figure class="post-figure">
  <a href="{{ '/img/blog/values-shape-agents/paper-results-six-tasks.png' | relative_url }}" aria-label="Open the six-task results figure at full size">
    <img src="{{ '/img/blog/values-shape-agents/paper-results-six-tasks.png' | relative_url }}" alt="The paper's six-task results: openness has the highest final mean score on five tasks, while self-enhancement leads on 2048. Below the score curves, maps of final solver code show different groupings under different value statements. The legend identifies four values and two controls." width="2246" height="901" loading="lazy" />
  </a>
  <figcaption>Mean scores on unseen test cases over 15 coding sessions (top), with standard error bands across ten runs and separate task scales. Maps below summarize measured code properties, not performance. <a href="{{ '/img/blog/values-shape-agents/paper-results-six-tasks.png' | relative_url }}">Full-size figure</a> · <a href="{{ '/papers/values-shape-self-improving-coding-agents.pdf' | relative_url }}#page=5">Paper Figure 3</a>.</figcaption>
</figure>

Every openness run on ALE-Bench uses [general free-cell or graph-cut search](/papers/values-shape-self-improving-coding-agents.pdf#page=32),
allowing a broader range of polygon shapes. Every conservation run retains
column-based search. Circle Packing
solvers often share a local optimizer, but openness runs more often add methods
for generating and recombining candidate packings.

Openness also produces larger, more complex solvers on average than the
no-values control on every task. Across tasks, code size and complexity track
performance more closely than evaluation count, API cost, or elapsed time. These
correlations do not establish that adding code causes better performance.

### A closer look at 2048

In a separate 2048 experiment, value conditions finish closer together when
agents tune a supplied engine than when they can rewrite the whole solver. The
versions use different compute limits, so the result suggests a role for freedom
to choose algorithms without isolating its effect.

<figure class="post-figure">
  <a href="{{ '/img/blog/values-shape-agents/paper-2048-editable-vs-fixed.png' | relative_url }}" aria-label="Open the 2048 solver comparison at full size">
    <img src="{{ '/img/blog/values-shape-agents/paper-2048-editable-vs-fixed.png' | relative_url }}" alt="Original 2048 comparison: mean score curves separate more when agents can rewrite the full solver than when they tune a supplied engine. The table lists what each version allows agents to change. The legend identifies four value statements and two controls." width="2200" height="600" loading="lazy" />
  </a>
  <figcaption>Left: agents can rewrite the full 2048 solver. Middle: they tune a supplied engine, and the value conditions stay closer together. Shading shows standard errors across ten runs. The SD labels express the range of final means in units of each version's overall score variation. <a href="{{ '/img/blog/values-shape-agents/paper-2048-editable-vs-fixed.png' | relative_url }}">Full-size figure</a> · <a href="{{ '/papers/values-shape-self-improving-coding-agents.pdf' | relative_url }}#page=7">Paper Figure 4</a>.</figcaption>
</figure>

## Editing values is a separate experiment

An [ALE-Bench extension](/papers/values-shape-self-improving-coding-agents.pdf#page=35) lets the agent revise its values between sessions while
retaining fixed safety rules. The range of final condition means shrinks to
about one-third of the fixed-values range: openness declines and conservation
improves. Revised statements become longer and more task-specific in a
preliminary reading; their transfer to other tasks was not tested.

Another [extension](/papers/values-shape-self-improving-coding-agents.pdf#page=36) derives values from selected AI research papers. Neither
derived statement provides a detectable improvement on ALE-Bench or 2048.
Ten runs per condition leave smaller effects unresolved.

The findings concern particular instruction texts, models, tasks, and budgets.
Rewording statements changes results, and the openness–conservation gap
disappears on the weakest tested model. Numerous statistical comparisons use unadjusted
significance thresholds. Higher benchmark scores also establish neither ethical
superiority nor agent safety. Persistent guidance can influence which solutions
a coding agent develops, so its wording deserves evaluation alongside the task
and scoring function.
