---
layout: post
title: Values Shape What Self-Improving Coding Agents Build
date: 2026-09-26
description: >-
  A controlled study across six coding tasks finds that persistent value
  statements affect both solver performance and the algorithms agents develop.
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

Four statements adapt the higher-order categories in Schwartz's theory of human
values. **Openness** favors new representations, algorithms, and continuing
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

## Different values produce different solvers

Openness has the highest final mean on five tasks; self-enhancement leads on 2048. Pooling scores after standardizing within each task, openness outperforms
the no-values control, while conservation and self-transcendence score below it.
The clearest opposing pair is openness versus conservation.

That overall pattern has exceptions and uncertainty. Openness's individual
advantages over the no-values control reach statistical significance on
ALE-Bench and Circle Packing, rather than all six tasks. No value statement
differs significantly from that control on Symbolic Regression.

{% include figure.html
   src="/img/blog/values-shape-agents/value-findings.svg"
   alt="Qualitative comparison of the four value statements. Openness favors
        transformation and leads mean scores on five tasks. Conservation favors
        proven incremental changes and has the lowest average rank.
        Self-enhancement emphasizes achievement and leads on 2048.
        Self-transcendence emphasizes shared usefulness and has mixed results,
        including a gain on Circle Packing. These are summaries, not score bars."
   caption="Qualitative findings from the fixed-values experiment. Ranking by
            mean score does not establish a statistically significant advantage
            on every task. Source: manuscript Sections 3–4 and Appendices D–E."
%}

The code reveals differences beyond scores. Every openness run on ALE-Bench
uses general free-cell or graph-cut search, allowing a broader range of polygon
shapes. Every conservation run retains column-based search. Circle Packing
solvers often share a local optimizer, but openness runs more often add methods
for generating and recombining candidate packings.

Openness also produces larger, more complex solvers on average than the
no-values control on every task. Across tasks, code size and complexity track
performance more closely than evaluation count, API cost, or elapsed time. These
correlations do not establish that adding code causes better performance.

## Editing values is a separate experiment

An ALE-Bench extension lets the agent revise its values between sessions while
retaining fixed safety rules. The range of final condition means shrinks to
about one-third of the fixed-values range: openness declines and conservation
improves. Revised statements become longer and more task-specific in a
preliminary reading; their transfer to other tasks was not tested.

Another extension derives values from selected AI research papers. Neither
derived statement provides a detectable improvement on ALE-Bench or 2048.
Ten runs per condition leave smaller effects unresolved.

The findings concern particular instruction texts, models, tasks, and budgets.
Rewording statements changes results, and the openness–conservation gap
disappears on the weakest tested model. Numerous statistical comparisons use unadjusted
significance thresholds. Higher benchmark scores also establish neither ethical
superiority nor agent safety. The practical result is narrower: persistent
guidance can influence which solutions a coding agent develops, so its wording
deserves evaluation alongside the task and scoring function.
