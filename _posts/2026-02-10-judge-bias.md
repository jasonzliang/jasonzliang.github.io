---
layout: post
title: >-
  Measuring model-family preference in AI judges
date: 2026-02-10
description: >-
  A strict AI judge can still favor its own model family, even when its
  scores initially suggest the opposite.
image: >-
  /img/blog/2026-02-10-judge-bias/judge-bias.webp
tags: [evaluation, llm-as-judge, caesar]
---

A judge can follow a research-answer rubric while favouring its own model
family. It may also apply a stricter scoring scale than another judge or reward
presentation features the evaluation was intended to ignore.

The [Caesar](https://jasonzliang.github.io/caesar-agent/) evaluation used three
judges: Claude Sonnet 4.5, GPT-5.2 and Gemini 3 Pro. Its
[paper](https://arxiv.org/html/2604.20855v3#S4.SS2) reports a model-family comparison and a
check for length effects.

## The scoring setup

Seven systems answered five research challenges. Six baselines paired the three
model families with either a vendor research mode or ordinary single-step web
search. The seventh, Caesar, used GPT-5.2. Each produced a full answer, a
plain-language summary called ELI5, and an ELI5 summary capped at 450 words.

[Each judge scored every answer three times](https://arxiv.org/html/2604.20855v3#A2.SS5) on New, Useful and Surprising, from
1 to 10 per dimension. Totals therefore run to 30 points. All score differences
below use that total.

For each judge, the [family metric](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/analysis/judge_analysis.py#L434-L486) compares its scores for the two baselines
bearing its model-family name with the scores the other two judges assigned to
the same answers. Caesar is excluded from the GPT family group despite using
GPT-5.2.

| Judge | Full-answer score gap on its own family |
|---|---:|
| Gemini | +1.35 |
| Claude | +0.98 |
| GPT | −0.82 |

A 1.35-point gap is 4.5% of the scale and substantial beside Caesar's 3.18-point
lead over the strongest baseline, Gemini 3 Deep Research. These are descriptive
differences of means: the paper supplies neither confidence intervals nor
significance tests for the family gaps.

## Strictness changes the interpretation

The negative GPT result could appear to contradict
[self-preference](https://arxiv.org/abs/2404.13076). That interpretation misses a
confounder: the metric does not adjust for a judge's overall strictness.

The published tables allow a partial correction. [One table](https://arxiv.org/html/2604.20855v3#S4.T1) averages all three
judges; [another](https://arxiv.org/html/2604.20855v3#S4.T2) averages Claude and Gemini. Subtracting twice the latter from
three times the former reconstructs GPT's scores, within rounding. The resulting
family gaps reproduce −0.82, −0.75 and +0.97 across the three answer formats.

On full answers, GPT scored every agent roughly 2 points below the other judges
on average. Its scores for agents outside its family were about 2.5 points lower;
its own family was only 0.8 points lower. Relative to that outside-family gap,
the family received about 1.7 points more favourable treatment. Applying the
same adjustment gives approximately +0.1 for ELI5 and +2.0 for 450-word summaries.

After correcting for strictness, the full-answer gap is positive. The scores
do not establish why the judges disagree. Claude-only and Gemini-only columns
are unavailable in the published tables, so the equivalent correction cannot be
reconstructed for those judges.

{% include figure.html
   src="/img/blog/2026-02-10-judge-bias/judge-bias.webp"
   alt="Raw family score gaps across full answers, plain-language summaries and
        450-word summaries. Gemini: +1.35, −0.12, −0.29. Claude: +0.98, −0.20,
        −0.22. GPT: −0.82, −0.75, +0.97."
   caption="Scores on a judge's two family baselines minus the other judges'
            scores on those answers, in points out of 30. Caesar is excluded
            from the family groups. No adjustment for judge strictness or
            uncertainty intervals is shown."
%}

The gaps also vary with answer format. Gemini's and Claude's positive gaps on
full answers become small negative estimates on summaries; GPT's raw gap becomes
positive under the 450-word limit. Without uncertainty intervals, these nine
estimates cannot establish how reliably the pattern would repeat.

## Length and system type

Across all seven systems, answer length and score have a [correlation of
**r = 0.47**](https://arxiv.org/html/2604.20855v3#S4.SS2.p2). The squared correlation is about 22%, a descriptive measure of
shared variation rather than a causal attribution.

Restricting the analysis to Caesar and the three vendor research modes changes
the correlation to **r = −0.13**. This is a
[Simpson's-paradox pattern](https://en.wikipedia.org/wiki/Simpson%27s_paradox):
the positive aggregate relationship largely reflects differences between system
groups, while the relationship within the research tier is weakly negative.

Neither correlation establishes whether additional words improve an answer.
The result cautions against automatically subtracting a verbosity penalty from
all scores: such an adjustment could remove differences associated with system
capability. The shallow-search tier was not separately tested.

## Removing the GPT judge

Because Caesar uses GPT-5.2, the evaluation also [drops the GPT judge and
recomputes the results](https://arxiv.org/html/2604.20855v3#S4.T2). All seven systems retain their ranking in all three
formats. The size of Caesar's lead changes, however: the full-answer margin
falls from **3.18 to 1.74 points**, a reduction of about 45%. The other margins
fall from 3.82 to 3.34 and from 4.73 to 4.07.

Recomputing the existing scores shows that the ordering does not depend on
GPT's inclusion. It supplies no independent evaluation and does not resolve
the remaining judges' preferences. Gemini still judges a comparison involving
its own research system.

Evaluations should report judge-specific scores in each answer format and
separate relative family preference from general strictness.
[LLM-based judging](https://arxiv.org/abs/2306.05685) remains a proxy for human
assessment. A panel can expose disagreement, but shared training methods and
rubrics may leave shared blind spots. The companion
[human comparison](/blog/human-vs-machine/) tests a different part of that gap.
