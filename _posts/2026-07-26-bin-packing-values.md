---
layout: post
title: >-
  Auditing an 11-of-14 tally in agent bin-packing experiments
date: 2026-07-26
description: >-
  An apparent advantage in packing performance weakened under audit, while the
  agents' different approaches to building solvers remained visible.
image: /img/blog/2026-07-26-bin-packing-values/offline-inrun-vs-heldout.webp
tags: [self-improving-agents, evaluation, values]
---

An exploratory study compared coding agents given two short values documents.
The cautious disposition favored verified steps, established approaches and
stopping at a working solution. The expansive disposition favored changes that
opened further possibilities. The documents contained three bullets and
120–175 words each; the remaining instructions were byte-identical. The
conditions were named `control` and `nietzsche`, after the
[expansive document's source](/blog/nietzsche/).

The study covered 28 runs plus an eight-run replication cohort. Three document
versions allowed different amounts of revision: v3 kept values fixed, sm-v4
allowed routine revision of the three bullets, and sm-v5 allowed the whole
values section to change. Each task–disposition–version cell had **one run**.
A matched pair compared the two dispositions within a task and version.

An initial tally favored the expansive condition in 11 of 14 pairs. An audit
found that many comparisons could not support that interpretation. Agents built
different kinds of solvers, but the design did not establish which disposition
performed better.

## Optimization and held-out performance

Each agent edited a solver, committed it and received a fixed evaluator's score
for ten iterations, or twenty in the first cohort. The task was
[one-dimensional bin-packing](https://en.wikipedia.org/wiki/Bin_packing_problem):
placing items into as few fixed-capacity bins as possible. The task has strong
classical baselines and appears in heuristic-discovery research such as
[FunSearch](https://doi.org/10.1038/s41586-023-06924-6).

Offline solvers receive the full item list; online solvers receive items
sequentially. The offline optimization benchmark was nearly saturated by
classical heuristics plus local search. The online task retained more headroom.
Two earlier offline variants, `cobench` and `generalize`, also entered the tally.

The in-run score guided optimization. Held-out scores were computed afterward
using published instance generators and a seed unavailable to the agents. That
benchmark changed during the study: the original Schoenfield Hard28 set gave
both dispositions and the reference heuristics exactly five proven-optimal
solutions out of 28, providing little discrimination.

{% include figure.html
   src="/img/blog/2026-07-26-bin-packing-values/offline-inrun-vs-heldout.webp"
   alt="In-run and held-out scores for eight offline runs, showing a narrow
        optimization-score range and a wider held-out range."
   caption="Eight offline runs across two cohorts; sm-v4 was repeated. The
            dashed reference is 0.837 for both Best-Fit-Decreasing and
            First-Fit-Decreasing. Both dispositions occur near both ends."
%}

The eight offline runs scored **0.9905–0.9955** in-run, spanning 0.005 across six
conditions in two cohorts. Their held-out scores spanned **0.756–0.991**, a
range of 0.235. Within one pair, gaps to optimum were 0.010 and 0.244, roughly
24-fold apart. Another pair had gaps of 0.009 and 0.159, roughly 18-fold apart
in the opposite direction.

The [plotting data and code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-07-26-bin-packing-values/make_figs.py#L3-L31)
record these eight runs' reported scores and the reference value.

The 0.244 mean covered 40 instances; four exceeded the compute budget and
received a full 100% gap penalty. Those
failures contributed ten of the 24.4 percentage points. Across the remaining 36,
packing used 16.0% more bins than optimum, near the classical reference within
noise. The reported standard error was 0.039. The ratio is a rough description
sensitive to penalties and small denominators. Online optimization scores were
less saturated and agreed with held-out ordering in the final-harness cohort.

## Differences in the artifacts

| Measure | Cautious | Expansive |
|---|---|---|
| Helper tools per run | 1, 1, 6, 1 | 7, 8, 10, 15 |
| Offline solver logical lines, v3 and sm-v4 | 765, 385 | 1038, 979 |
| Observed strategies | 1–2: greedy, local search | 4, including perfect-fit search |
| Unverified additions | Pruned or withheld | Retained |

Logical lines exclude blanks, comments and docstrings. Raw file lengths for
the same solvers were 1,278 and 628 versus 1,429 and 1,553. Cautious runs spent
more effort on audits and ruling out alternatives; expansive runs retained more
solver machinery. Online scoring functions remained compact in both conditions.
These observations came from four non-independent, non-seed-controlled runs
per disposition and do not establish a causal behavioral effect.

In offline sm-v4, the cautious agent withheld a late perfect-fit search because
its in-run benefit appeared negligible. That run then lost its held-out pair
by roughly 18-fold in gap to optimum. The historical review located the
withheld search in commit history, rather than in the final solver; those
commits have not been rechecked here. In offline v3, an expansive solver's
perfect-packing search instead exhausted the compute budget, producing the
four failures above. The same technique had different outcomes across runs.

## Why the tally was unreliable

The 11-of-14 in-run tally had a sign-test p-value around 0.06. Its problems
overlapped, so the following categories cannot be subtracted sequentially:

- About four apparent wins were saturated comparisons, with margins of
  0.0006–0.0011. Offline scores were near 0.99, `cobench` near 0.999, and
  Hard28 failed to distinguish the solvers.
- About two involved failed control runs. One documented control remained near
  Best-Fit's 0.9524 reference, scoring 0.9534 in-run and 0.9549 held-out.
- One excluded expansive run imported a published heuristic tuned to the exact
  test distribution. A clean rerun favored cautious.
- Pairs A1, A2 and E6 used near-duplicate expansive solvers on shared held-out
  draws. Treating them as three independent results inflated the count by two.
- Three warm-started `generalize` pairs had signed in-run differences of
  −0.0028, −0.0009 and +0.0009, netting −0.0028 toward cautious.

A1 contained both a failed control and a duplicate solver. Nine of the eleven
wins fell into these overlapping categories; one of the other two came from an
older unreported run. Only one clean expansive win remained from that tally.

The four pairs under the final matched harness split **2–2 held-out**. In-run
they favored expansive 3–1, including two saturated offline comparisons; the
two online differences had opposite signs. The recency-weighted pooled online
held-out difference was −0.0024, too small to establish a direction here.

Repeating sm-v4 reversed the held-out winner on both tasks: expansive to
cautious offline, cautious to expansive online. The rerun also changed the
harness and increased the wall-clock allowance from one hour to three. One
cautious winner rewrote its values eight times, expanding from 14 to 33 lines,
and used iteration nine's solver rather than iteration ten's. Excluding that
pair leaves one clean recent online pair, favoring expansive, alongside split
offline results.

These runs reveal differences in solver design and several evaluation failures,
but cannot reliably rank the dispositions. More instance draws cannot
replace independent agent runs. A powered follow-up with
[analysis fixed in advance](/blog/pre-registration/) was conducted on a
different task; its results belong to that separate experiment.
