---
layout: post
title: >-
  Pre-registering AI agent experiments at the run level
date: 2026-07-24
description: >-
  A four-run bin-packing case study fixed its held-out analysis before scoring.
  The result remained underpowered: each agent run was one data point.
image: /img/blog/2026-07-24-pre-registration/verdict-gate.webp
tags: [methodology, self-improving-agents, evaluation]
---

A small bin-packing experiment illustrates both the purpose and the limits of
pre-registration. Before four completed agent runs were re-scored on a rebuilt
held-out benchmark, a committed analysis document fixed the primary metric, its
calculation and the conclusions the sample could support. It classified the
experiment as a descriptive case study, with no hypothesis-testing threshold.

The agents improved an online bin-packing heuristic, placing arriving items
into bins without lookahead. A control values document and a
[Nietzsche-derived document](/blog/nietzsche/) were each tested at two document
versions. The later documents strengthened the contrasting instructions, and
the later Nietzsche-derived document explicitly encouraged values revision.
All four documents allowed edits below the protected invariants. There was
one run per condition: four runs in total, consuming about twenty hours of
agent time in one overnight batch.

This was a registration before held-out scoring, rather than before the whole
experiment. The runs were already frozen, their optimization scores were known,
and a pilot on an offline variant had ranked the dispositions in the opposite
order. Those observations ruled out treating a directional prediction as
independent of prior results. The registered comparison was two-sided.

## Fixing the analysis before scoring

[HARKing](https://en.wikipedia.org/wiki/HARKing), or hypothesizing after results
are known, can arise without deliberate misrepresentation. An experiment may
have a flat primary outcome and an appealing secondary result. Selecting that
result from twelve measurements creates a multiple-comparison problem, even
when its explanation sounds plausible. Both registrations in this project
specified Holm correction for the family of secondary measurements.

Three documents had distinct roles:

- `PREREGISTRATION.md` fixed the descriptive analysis. Its commit preceded the
  re-scoring commit by seven minutes.
- `PREREGISTRATION_POWERED.md`, written the next day, was a draft plan for a
  powered follow-up. Its tests and decision thresholds were not part of the
  frozen case study.
- A standing analysis playbook supplied the verdict gate used to interpret
  comparisons between runs.

Keeping those roles separate matters. A proposed confirmatory test cannot
retroactively turn an exploratory case study into a powered experiment.

## The endpoint and the experimental unit

Both registrations selected one primary endpoint: the evolved program's mean
percentage excess over a lower bound on the optimal number of bins, measured
on uniformly distributed item sizes after optimization on Weibull-distributed
sizes. Lower values indicate better packing under this distribution shift.

The primary held-out set contained 50 packing instances. **One agent run was
one experimental unit**, because all 50 instances were packed by the same
program produced by the same trajectory. Additional instances help estimate a
program's performance; they do not supply additional independent agent runs.
[Counting instances as runs](/blog/hub-vs-leaf/) would have inflated the sample
size fiftyfold.

The draft follow-up specified an exact two-sided
[permutation test](https://en.wikipedia.org/wiki/Permutation_test). It would
reassign condition labels across run scores and compare the observed difference
with the differences produced by those assignments. At five runs per condition,
there are 252 possible assignments. The implementation enumerates assignments
through ten runs per condition, then uses a fixed-seed sample of 200,000.

This test also exposes small-sample limits. With three runs per condition,
there are only 20 assignments, so the smallest attainable two-sided p-value is
0.1. Such a design cannot reach p below 0.05, regardless of the observed gap.

The draft defined one percentage point of the excess metric as the smallest
meaningful effect. That threshold could change before the pilot, never after
its data were examined. A positive decision required both p below 0.05 and a
difference exceeding one point. Otherwise, the report would state the minimum
detectable effect alongside the result. If that detectable effect exceeded the
meaningful threshold, the experiment would lack the resolution needed to
answer its intended question.

## Interpreting the result

The separate playbook required four possible verdicts:

- **Inconclusive by saturation:** ceiling or floor effects leave no room to
  detect a difference.
- **Underpowered:** the available runs cannot adequately bound the effect.
- **Effect:** an interval supports a difference beyond run-to-run noise.
- **Null:** the benchmark has room to move, and the report states its noise band.

{% include figure.html
   src="/img/blog/2026-07-24-pre-registration/verdict-gate.webp"
   alt="Decision flowchart checking benchmark saturation, the ability to bound
        an effect, and whether a difference exceeds measured run-to-run noise."
   caption="The standing playbook separates saturation and insufficient power
            from an effect or a null result."
%}

A score of 0.99 on a benchmark capped at 1.0 may reveal limited measurement
headroom. It does not establish that the intervention has no effect. Likewise,
“no detectable difference at this sample size” states a narrower conclusion
than a general claim that values do not affect performance.

The four-run case study was **underpowered**. One run per condition could not
separate a disposition effect from variation between agent trajectories. The
frozen document recorded that limit before held-out scoring.

The follow-up document remained headed “Draft for review” and prohibited
confirmatory work before freezing the plan. It did not assert a sample size;
that required a pilot and power analysis. Later powered work on a different
task was a separate experiment.

The frozen registration was 56 lines of Markdown. Five subsequent commits
changed paths or terminology without changing an analysis choice. Its value
was a reviewable record of the analysis decisions and their timing, including
what the experiment could not establish.
