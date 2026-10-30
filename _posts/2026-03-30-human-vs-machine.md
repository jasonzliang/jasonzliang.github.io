---
layout: post
title: >-
  Human and AI evaluations gave different pictures of Caesar's advantage
date: 2026-03-30
description: >-
  People showed a modest preference for Caesar's summarized answers, offering
  weaker and less consistent support than AI judges gave its full reports.
image: >-
  /img/blog/2026-03-30-human-vs-machine/human-vs-machine.webp
tags: [evaluation, human-evaluation, caesar]
---

[Caesar](https://jasonzliang.github.io/caesar-agent/) led the automated research
answer evaluation, but the human comparison was much closer. Raters preferred
it to Gemini 3 Deep Research in [**63 of 112 comparisons: 56.25%**](https://arxiv.org/html/2604.20855v3#A9.T12). Their choices
also reversed the automated ordering on two of five challenges.

The people and the models evaluated the same systems and challenges, but saw
different versions of the answers and used different response formats. The
[judge-bias analysis](/blog/judge-bias/) adds another reason to examine the
automated margin rather than treating it as a direct measure of human preference.

## What the raters saw

Gemini 3 Deep Research was Caesar's strongest baseline in the automated study.
For each of five challenges, a human rater saw a blinded pair and selected the
more creative answer under the same New, Useful and Surprising rubric used by
the AI judges.

Before presentation, an LLM [rewrote both answers into a common two-paragraph
schema](https://arxiv.org/html/2604.20855v3#A9.SS1): two or three sentences summarizing the core idea, followed by three or
four explaining its creativity. The normalization reduced distractions from
length and structure, while also removing much of the original evidence,
citations and exposition.

The [paper](https://arxiv.org/html/2604.20855v3#A9.SS1) reports 23 raters. The underlying
vote table contains 21 distinct names across 23 sittings, with two people
submitting twice. Seven votes repeat a pair the same rater had already judged;
one repeated judgment changes direction. There are only five distinct answer
pairs, each receiving roughly 22 judgments.

Caesar's summary was longer in all five pairs, by 5 to 42 words, about 16% on
average. The longest difference occurred on a challenge Caesar lost, and the
smallest on one it won. With only five pairs,
that pattern cannot establish whether length influenced preference.

## The aggregate comparison

The 63-to-49 result gives preference odds of 1.29. The paper calls this an odds
ratio, but no second odds quantity is being compared. An exact binomial 95%
interval for the preference share runs approximately **47% to 66%**
([calculation and plotting code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-03-30-human-vs-machine/make_figs.py#L67-L108)), including
50%.

That interval assumes 112 independent votes. Repeated judgments from the same
people and repeated assessment of the same five pairs make it an incomplete
account of uncertainty. It does not support a precise population-level estimate
of preference across research tasks.

The repeated-rater counts and summary-length checks use unpublished run records.

On full answers, the automated judges gave Caesar a **3.18-point lead on a
30-point scale**. Its matching effect size against Gemini was
[Cliff's delta](https://en.wikipedia.org/wiki/Cliff%27s_delta) [**0.84**](https://arxiv.org/html/2604.20855v3#S4.T1), above
the paper's 0.47 threshold for a large effect. The broader statement that all
deltas were at least 0.76 covers other baselines and formats too; 0.84 is the
relevant value for this particular comparison.

{% include figure.html
   src="/img/blog/2026-03-30-human-vs-machine/human-vs-machine.webp"
   alt="Human preference for Caesar is 56.25 percent, with a binomial 95 percent
        interval spanning 50 percent. The automated full-answer comparison has
        Cliff's delta 0.84 over five challenge means, with no interval shown."
   caption="The same systems and five challenges, evaluated on different
            stimuli. Humans compared normalized summaries; AI judges scored
            full answers. The human interval assumes independent votes."
%}

The delta uses five per-challenge means for each system. It compares every
Caesar challenge mean with every Gemini challenge mean, measuring the share of
higher pairings minus the share of lower pairings. A value of 1 would mean that
Caesar's lowest challenge mean exceeded Gemini's highest. It would not mean
that every individual judgment favoured Caesar; individual score distributions
overlap.

The paper [reports effect sizes rather than p-values](https://arxiv.org/html/2604.20855v3#A2.SS5), describing them as
estimates of [stochastic dominance](https://en.wikipedia.org/wiki/Stochastic_dominance).
Run artifacts also contain Mann–Whitney U statistics calculated over 45
individual judge scores per system and format. Those use a different unit from
the five means underlying the delta, and repeated scoring should not be mistaken
for additional independent challenges.

## Preference depends on the challenge

| Challenge | Votes preferring Caesar |
|---|---:|
| Constrained synthesis | 5 of 23 |
| Counterfactual reasoning | 18 of 23 |
| Cross-domain synthesis | 20 of 22 |
| Meta-creativity | 13 of 22 |
| Open-ended synthesis | 7 of 22 |

{% include figure.html
   src="/img/blog/2026-03-30-human-vs-machine/human-by-challenge.webp"
   alt="Human preference for Caesar ranges from 5 of 23 votes on constrained
        synthesis to 20 of 22 on cross-domain synthesis. Caesar wins three
        challenges and loses constrained and open-ended synthesis."
   caption="The 112 votes by challenge, from the paper's Table 12. Only five
            distinct answer pairs underlie these judgments."
%}

[Caesar led the automated full-answer scores on all five challenges](https://arxiv.org/html/2604.20855v3#A3.T5). The paper's
statement that the human pattern mirrors those results therefore needs
qualification. Cross-domain synthesis produced the largest automated lead and
the strongest human preference; open-ended synthesis produced the narrowest
automated lead and a human loss. But constrained synthesis had the
second-largest automated margin, **3.33 points**, while humans preferred Gemini
by 18 votes to 5.

## What can explain the gap

AI judges assigned separate numerical scores to complete answers, repeating the
process across three judges and three trials. Humans made binary choices on
compressed ideas. A win rate records preference frequency, not the size of an
individual preference, so it cannot be translated directly into a score margin.

Normalization may also have removed material contributing to the automated
lead. That is an untested explanation: the rubric asks about novelty,
usefulness and surprise, and the research-tier length–score correlation was
weakly negative, **r = −0.13**. The experiment cannot distinguish a benefit from
supporting exposition from an inflated automated assessment.

The human result supports a modest aggregate preference in the same direction
as the automated ranking. It does not corroborate the automated margin's size
or its consistency across challenges. A stronger comparison would give humans
and models matched stimuli, include more independent tasks, and account for
repeated raters.

Source: [Caesar paper, revised version](https://arxiv.org/abs/2604.20855v3).
