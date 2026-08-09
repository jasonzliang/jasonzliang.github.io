---
layout: post
title: "We asked three AIs to grade seven AIs. Our bias test missed one."
date: 2026-02-10
description: >-
  Using language models as judges is now standard practice. We measured whether
  ours favoured their own model families. Two of three did. The test said the
  third did the opposite, and the test was wrong.
image: >-
  /img/blog/2026-02-10-judge-bias/judge-bias.webp
tags: [evaluation, llm-as-judge, caesar]
---

If you build a system that writes long-form answers, you have a measurement
problem. There is no accuracy score for "was this a good piece of research." So
the field has largely settled on a workaround: ask a language model to grade the
output.

This is convenient and it is obviously suspicious. The graders are the same
class of system as the things being graded, and often literally the same models.
So when we evaluated [Caesar](https://jasonzliang.github.io/caesar-agent/), our
research agent, we used a panel of three judges from three different families:
Claude Sonnet 4.5, GPT-5.2 and Gemini 3 Pro. Then we went looking for the
failure mode everyone worries about.

We found it. Then we found out that the way we measured it cannot distinguish
that failure mode from something much more boring.

## The scoring setup

Every answer was scored on three dimensions, each 1 to 10: New, Useful and
Surprising. Those sum to a **30-point total**, and every number below is in
points on that total.

Seven systems were graded. Six of them are the three judge models themselves,
each run twice: once in the vendor's own autonomous research mode ("deep"), once
with ordinary single-step web search ("shallow"). The seventh is Caesar, which
runs on GPT-5.2. Each system answered five research challenges under three
output formats: an unconstrained full answer, an unconstrained explain-it-simply
summary (the paper calls this ELI5, for "explain like I'm five"), and an ELI5
summary capped at 450 words. Every judge scored every answer three times.

## Measuring a judge's favouritism

The test is simple. For each judge, take the two baselines that carry its own
model name, and compare the scores that judge gave them against the scores the
*other two* judges gave the same answers. If a judge is neutral, those should
agree.

On full-length answers:

| Judge | Its own family, minus what the other two judges gave |
|---|---|
| Gemini | **+1.35** |
| Claude | **+0.98** |
| GPT | **−0.82** |

The Gemini judge scored its own family 1.35 points above what its colleagues
gave the same text, Claude +0.98. On a 30-point scale 1.35 is 4.5%: small in
absolute terms, and still large enough to matter, because the gap between Caesar
and the strongest baseline (Gemini 3 Deep Research) was 3.18 points on that same
scale.

Two things belong next to that table. There are no error bars: each cell is a
difference of two means, and the paper reports no interval and no significance
test for any of them. And Caesar is not counted in the GPT family, even though
it runs on GPT-5.2, so none of these numbers say anything about how the GPT
judge treated our own system. The family groups are the six named baselines and
nothing else.

## The GPT row does not mean what we said it meant

The GPT judge looks like it went the other way: −0.82, harsher on its own family
than the other two judges were. We originally read that as a nice result, a
counterexample showing self-preference has no universal direction.

It is not that. The number is a raw difference of means, and it does not control
for how strict a judge is in general. A judge that marks everyone down will look
unbiased toward its own family only if it marks its own family down by the same
amount.

You can check this from the paper's own tables without any new data. Table 1
gives each agent's score averaged over all three judges; the robustness table
gives the same agents averaged over Claude and Gemini only. Two equations, one
unknown: the GPT judge's own column falls straight out. Doing that reproduces
the published −0.82, −0.75 and +0.97, one per answer format, to within rounding,
which is the check that the reconstruction is right.

It also shows this. On full answers the GPT judge marked *every* agent about 2
points below the other two, and the agents outside its own family about 2.5
points below. Against its own family it was only 0.8 points below. Measured
against that 2.5, the GPT judge marked its own family **up** by about 1.7
points. The same correction gives +0.1 on ELI5 answers and +2.0 on 450-word
ones. Never negative.

So the honest statement is not "this judge dislikes itself." It is that our bias
metric mixes self-preference with overall strictness, and for the one judge
where we can pull those apart, doing so flips the sign. The paper publishes no
Claude-only or Gemini-only column, so the same correction cannot be computed for
the other two judges. Their +1.35 and +0.98 could be bigger or smaller than they
look, and we cannot say which.

## The gaps move with answer format

Whatever these numbers are measuring, they are not a property of the judge
alone. They are a property of the judge *and the task*.

Ask for an ELI5 summary instead of a full-length answer and the Gemini and
Claude gaps land at −0.12 and −0.20. That is a disappearance, not a reversal: on
a 30-point total those two values are not distinguishable from zero, and calling
them "negative" would be reading noise. GPT is the one that moves by an amount
worth naming, from −0.82 on full answers to +0.97 on 450-word ones.

So a single number for "this judge's bias" would be the wrong shape of thing to
report. But the evidence for the format effect is thin and should be described
that way: nine numbers, one per judge per format, from a single evaluation run,
with no error bars on any of them.

{% include figure.html
   src="/img/blog/2026-02-10-judge-bias/judge-bias.webp"
   alt="Grouped bar chart of each judge's gap on its own family across three
        answer formats: full-length, explain-like-I'm-five, and 450-word.
        Gemini is +1.35, then −0.12 and −0.29; Claude follows the same shape at
        +0.98, −0.20 and −0.22. GPT is the mirror image, −0.82 and −0.75 on the
        first two formats and +0.97 on 450-word ones."
   caption="Each bar is what a judge gave the two baselines from its own model
            family, minus what the other two judges gave those answers. Caesar
            is in no family group. These are raw differences, not adjusted for
            overall strictness, which is why the GPT bars are not
            self-criticism."
%}

## The verbosity trap, and why the obvious fix is wrong

The other standing worry about LLM judges is that they reward length. We
checked, and at first glance the worry looks confirmed: across all seven agents,
the correlation between answer length and score is **r = 0.47**. The paper calls
that moderate, which is the right word: it is about 22% of the variance in
score.

Then we restricted the comparison to the deep research tier, Caesar and the
three vendor research modes, which produce answers of comparable length. The
correlation went to **r = −0.13**.

This is Simpson's paradox. The overall correlation is real, but it is generated
by *between-group* differences: the systems that write longer answers happen to
also be the ones that write better ones. Inside the deep research tier, extra
length buys nothing. If we had stopped at r = 0.47 and "corrected" for
verbosity, we would have adjusted away a genuine quality signal.

The limit on that claim is that we only ran it inside one tier. "Length buys
nothing among peers" is established for the deep research group and untested for
the shallow one.

## What we did, and why it is not enough

Two things, neither of which fully solves the problem.

We report the panel rather than a single judge, so no one model's thumb decides
the outcome. And because Caesar is built on GPT-5.2, creating an obvious
circularity, the paper also reports every agent's total with the GPT judge
dropped. The ranking held, in all three formats, all seven positions.

What "the ranking held" does not tell you is what happened to the size of the
win. On full answers, Caesar's margin over the runner-up falls from 3.18 points
with all three judges to 1.74 with the GPT judge removed. The order survives;
45% of the margin does not. The other two formats move much less, 3.82 to 3.34
and 4.73 to 4.07, but the headline number is the one that moves most. And the
two judges left standing include the Gemini judge, which is the one carrying a
+1.35 thumb on Gemini 3 Deep Research, the exact system Caesar is being measured
against. Neither the three-judge margin nor the two-judge margin is clean.

That is a robustness check, not a fix. It is also a re-aggregation of scores we
already had, not a fresh evaluation run: it tests whether the GPT judge was
carrying the result, and nothing else.

The honest position is the one in our paper's limitations: LLM-as-judge "remains
an imperfect proxy for human creativity assessment," and judges trained by
similar procedures may share blind spots that no panel of them can detect,
because the panel is not independent in the way the word implies.

Which is why we also asked actual humans; the gap between what the humans said
and what the judges said is the subject of that post.

## If you are using LLM judges

Four things this experiment would suggest, none of them expensive:

**Measure the bias rather than assuming it.** One extra analysis pass found a
1.35-point thumb on the scale.

**Then work out what your bias metric is confounded with.** Ours was a raw
difference of means, which cannot separate self-preference from a judge being
strict with everybody. Pulling those apart reversed the sign of one of our three
headline numbers.

**Measure it per output format.** Ours moved a lot between long and short
answers.

**Check whether your confounder is between-group or within-group.** Our
verbosity correlation was 0.47 across all agents and −0.13 among deep research
peers. The naive correction would have made the evaluation worse.
