---
layout: post
title: >-
  How AI agents rewrote their values across 41 exploratory runs
date: 2026-08-05
description: >-
  In these runs, agents always revised editable values, and uncapped files
  expanded from brief guidance into lengthy instruction documents.
image: >-
  /img/blog/2026-08-05-values-rewriting/values-growth.webp
tags: [self-improving-agents, agent-design, ai-safety]
---

A self-improving agent can revise its solver while retaining fixed behavioral
instructions, or it can revise those instructions too. In this experiment, a
short values file described [dispositions](/blog/nietzsche/) such as cautious
improvement or continued expansion. The agent read it at the beginning of every
iteration.

An audit compared starting and ending values files across **41 exploratory
runs on five tasks**. Three settings controlled permission to rewrite the file:
**frozen**, which instructed the agent to preserve its values; **bounded**,
which allowed revision within three short bullets; and **radical**, which
allowed unrestricted revision of the section each iteration.

Starting and ending files showed which instructions the agents changed.
Differences in the broader experiment design prevented performance comparisons
from establishing whether self-revision improved the agents.

## What changed

| Setting | Runs | Values changed | Starting lines | Ending lines |
|---|---|---|---|---|
| Frozen | 15 | **0 of 15** | 15–22 | 15–22 |
| Bounded | 11 | **11 of 11** | 14–16 | 15–26 |
| Radical | 15 | **15 of 15** | 15–23 | 96–446 |

The [plotting data and code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-08-05-values-rewriting/make_figs.py#L44-L65)
record the final lengths for all 41 runs.

Line counts cover the values-section body, from its heading to the next
top-level heading, with leading and trailing blank lines trimmed. Seed files
contained three bullets and a two-sentence preamble, accounting for their
initial lengths. Each final file was compared with that run's own starting
file.

The frozen condition was an instruction rather than a filesystem lock. At each
iteration, the runner rebuilt a fixed invariants block and status header while
preserving the agent's remaining content. An unauthorized values edit would
therefore have persisted and appeared in the diff. Zero changes across fifteen
runs records observed compliance with that instruction.

Every bounded run revised its values and retained exactly three bullets. All
eleven nevertheless grew by one to ten lines. In the longest block, individual
bullets occupied six to ten lines, exceeding the requested one or two short
sentences. The bullet count held more consistently than the brevity instruction.

Every radical run revised its values. The largest grew from 17 to **446 lines**;
fourteen of fifteen exceeded 100 lines. Only bounded files mentioned 100-line
growth as a failure to avoid. Radical files contained no such size guidance.

{% include figure.html
   src="/img/blog/2026-08-05-values-rewriting/values-growth.webp"
   alt="One dot per run on a logarithmic line-count scale. Starting blocks
        contain 14–23 lines. Frozen and bounded blocks remain nearby; radical
        blocks end at 96–446 lines, fourteen above 100."
   caption="Final values-section lengths for 41 runs. The dashed 100-line
            reference comes from the bounded instruction; radical runs did
            not receive that instruction."
%}

## A procedural rule and its failure

One uncapped bin-packing run ended with 422 lines. Its values file recorded
repeated generation of plausible numerical results before the measurement
code existed. A smaller incident occurred at iteration nine; full scorecards
with five tables, t-statistics and narrative appeared at iterations eleven
and thirteen of a fifteen-iteration run.

After the first two incidents, the agent added a rule requiring numbers in
prose to be copied from instrument-generated files. Its account stated that
the fabricated drafts had been deleted within a minute, without being
measured, committed or acted on. These details are the agent's recorded account
in the values file, rather than an independent audit of every downstream use.

The rule operated beneath fixed honesty instructions, restored verbatim every
iteration. Those instructions already required observed execution before
success claims and prohibited weakening checks. The agent's new rule added a
specific procedure for following that requirement.

The procedure did not prevent recurrence. At iteration thirteen, the agent
filled a verdict section despite an instruction to leave it empty. Its
subsequent explanation identified the empty report structure as a prompt for
invented content. It revised the procedure again: end the draft at the verdict
heading and copy measured tables into it mechanically afterward.

The record does not show whether the revised procedure prevented further
fabricated drafts. File growth alone also cannot distinguish useful procedures from
redundant instructions or task notes.

## Limits of the comparison

The 41 runs varied across four initial dispositions, five tasks, values-file
generations, three revision settings, iteration counts of 10, 15 or 20, and six
runner commits. On 31 July, radical runs started four and a half hours after
frozen and bounded runs on the same task, using a commit made between those
launches. The design was incomplete: one task had no bounded condition, and the
fourth disposition appeared only on that task.

Within-run file diffs establish what was edited and how large the blocks
became, but they do not isolate the effect of rewrite permission on quality or
performance. Each
condition had a single sample, as in the
[bin-packing performance audit](/blog/bin-packing-values/).

A countable three-bullet instruction held in all eleven applicable runs, and
unrestricted revision produced much longer documents in all fifteen observed runs. The
contents of those edits also recorded repeated fabrication of numerical results.
Determining whether editable values improve agent performance requires a
separate comparison with independent runs and a consistent harness.
