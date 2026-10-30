---
layout: post
title: "CREST: comparing papers from five AI scientists"
date: 2026-10-28
description: >-
  A comparison of released research papers across five AI scientist systems,
  with 96 sampled paper pairs, 384 model judgments, and small paper pools
  that limit the ranking's interpretation.
image: /img/blog/crest-ai-scientists/observed-ranking.svg
tags: [creativity, ai-scientists, evaluation]
---

AI scientist systems release papers on different questions, using different
methods and resources. Comparing their work therefore starts with a choice
about what counts as evidence. CREST's [released-paper comparison][report]
examines the manuscripts available from five systems and asks two language
models to choose between sampled pairs. Sakana Agentic Scientist (v3) leads
the observed ranking, with a crucial qualification: its eligible collection
contains only two papers.

The comparison covers Sakana's AI Scientist v1, v2, and Agentic Scientist v3,
alongside ScientistOne and ScientistTwo. It evaluates their released paper
collections. Differences in research topics, release dates, underlying models,
computing resources, and publication choices remain part of the comparison.
The resulting preferences cannot isolate which system design caused a
difference in paper quality.

## From released papers to comparisons

The archive contains **411 downloaded papers**, of which **410 are eligible**
for the primary comparison. One manuscript involving substantial human guidance and revision is excluded. Among the eligible papers, **86 appear in the sampled
comparisons**. That distinction matters: 86 is the number of distinct selected
papers, rather than the number of pairs or judgments.

The plan covers all ten matchups between the five systems, sampling up to ten
distinct paper pairs uniformly within each matchup. The v3–v2 matchup has only six
possible pairs, because those collections contain two and three eligible
papers. All six are included. Together, the matchups produce **96 paper pairs**.
Some papers appear repeatedly against different opponents.

Two judges, Gemini 4 Argon and GPT-6 Astra, each read every pair in both
paper orders. Each completed pair therefore contributes four overall choices,
giving **384 saved judgments**. Reversing the order helps expose sensitivity
to which manuscript appears first. It does not create another independent
paper.

## One overall judgment

The judges consider **New, Useful, and Surprising jointly**, then choose one
manuscript and explain the tradeoffs. New concerns how specifically the judge
can place the contribution in earlier work; Useful concerns the mechanism
and evidence supporting the claimed benefit; Surprising concerns departure
from the obvious approach to the paper's own question. These considerations
guide a single choice, without separate numerical scores for each quality.

The judges receive extracted PDF text. Their explanations can be inspected
against the manuscripts, but the procedure does not independently reproduce
experiments or inspect visual plots. A model's inability to recall prior work
also cannot establish historical novelty. Human-expert agreement and the
validity of this particular creativity instrument remain untested.

## The observed ranking

The score first averages the four choices within a paper pair, then averages
pairs within each matchup. Finally, it gives each of the four opponents equal
weight. Thus the six-pair v3–v2 matchup has the same weight in a system's
overall score as a ten-pair matchup. A much larger released collection does
not receive extra weight simply because it contains more papers.

{% include figure.html
   src="/img/blog/crest-ai-scientists/observed-ranking.svg"
   alt="Observed equal-opponent preference percentages: Sakana Agentic Scientist v3 96.9%, ScientistTwo 73.8%, ScientistOne 53.8%, Sakana AI Scientist v2 22.5%, and Sakana AI Scientist v1 3.1%. Selected papers divided by eligible papers are 2/2, 29/86, 17/21, 3/3, and 35/298 respectively."
   caption="Measured results from 96 completed paper pairs and 384 judgments. Each score averages four opponent matchup rates equally; each pair supplies four votes. Paper counts show selected / eligible manuscripts. Points show observed scores; sampling uncertainty is discussed below. Source: CREST's saved AI scientist comparison."
%}

Sakana Agentic Scientist (v3) receives a 96.9% overall preference rate, followed
by ScientistTwo at 73.8%, ScientistOne at 53.8%, Sakana AI Scientist v2 at
22.5%, and v1 at 3.1%. For example, v3 receives 87.5% of the choices against
ScientistTwo and 100% against each other opponent. Its overall score is the
equal-weight average of those four matchup rates.

The small collections constrain that result. Every eligible v3 and v2 paper
is selected, but repeatedly comparing two or three manuscripts supplies little
evidence about the range of papers those systems might produce in future.
For the larger pools, substantial portions of the released work remain
unsampled.

The cohort expanded from four to five systems after earlier results had been
observed, and the sample also grew after initial results. The report's
exploratory sampling ranges use a nominal 95% fixed-size calculation, with
**no 95% coverage guarantee for this extension**. They condition on the frozen
paper pools and judge/order outcomes; they exclude model variability, judge
validity, and future work. The ranking across every eligible paper pair
therefore remains uncertain.

The [public evidence report][report] supplies selected PDFs, release records,
head-to-head rates, and saved comparative explanations. Those records allow
individual choices to be examined and disputed. The observed ordering applies
to these released papers, opponents, and judging procedure.

[report]: https://github.com/jasonzliang/crest/blob/main/docs/ai-scientist-creativity.html
