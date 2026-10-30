---
layout: post
title: >-
  Comparing creative research answers with CREST
date: 2026-10-28
description: >-
  Three research workflows answered the same 50 questions. Balanced pairwise
  judging strongly favored Caesar, with clear limits on what that preference means.
image: >-
  /img/blog/crest-deep-research/ranking.svg
tags: [evaluation, creativity, research-agents]
---

CREST's [deep-research comparison](https://github.com/jasonzliang/crest/blob/main/docs/deep-research-creativity.html)
asks how three research workflows respond to the same creative tasks. Its
50 questions produced 150 saved answers, followed by 600 pairwise judgments
from two AI judges. Caesar received the strongest preference, followed by
OpenAI's Sol workflow with web search and Google Deep Research.

The result concerns the creative quality those judges perceived in those
answers. It does not establish that human readers or domain experts would
agree, or that the answers' factual claims are correct. The useful contribution
is an inspectable comparison: the report preserves every question, answer,
comparative explanation, and recorded configuration alongside the ranking.

## Three workflows, shared questions

The questions demand concrete artifacts under unusual constraints. Examples
include a zero-electricity cooling system using materials available in
14th-century Mali, a story whose sentences alternate positive and negative
sentiment, and a tabletop combat system that resolves actions through dice
positions without arithmetic. These tasks require invention together with
attention to the requested constraints.

Caesar combines Sol for research answers with Luna for exploration and its
knowledge base. The OpenAI workflow uses Sol with web search. Google uses its
managed Deep Research service.

These are comparisons of complete workflows. Their research processes and
resource use differ, so the results do not isolate a single model capability
or the effect of one architectural change.

{% include figure.html
   src="/img/blog/crest-deep-research/comparison-design.svg"
   alt="Study design: 50 shared questions generate three answers each, giving 150 answers. For each question, three pairs are judged by two judges in both answer orders, giving 12 decisions per question and 600 total. Each system appears in 400 decisions."
   caption="Comparison design, shown schematically. Each system faces both opponents with equal weighting across questions, judges, and answer orders."
%}

## One creative preference per comparison

NUS means **New, Useful, and
Surprising**: the original contribution, its fit and support, and its departure
from an expected approach. These qualities guide one joint A/B choice with a
comparative explanation. They do not receive separate scores or equal votes.
That lets a judge weigh a serious weakness in usefulness against a modest
advantage in novelty, although the tradeoff remains the judge's judgment.

GPT-6 Astra and Gemini 4 Argon judged each pair in both orders. Neither judge
used tools. Provider names were hidden, although writing style could still
reveal a system's identity.

Each question yields three pairs × two judges × two orders: 12 decisions.
Each system participates in eight, giving **400 comparisons per system**
across the 50 questions. Wins divided by 400 determine its overall rate.

## The observed ranking

Caesar won **390 of 400 comparisons (97.5%)**, the OpenAI workflow won
**176 (44.0%)**, and Google Deep Research won **34 (8.5%)**. In direct
matchups, Caesar beat OpenAI in 96.0% of 200 decisions and Google in 99.0%;
OpenAI beat Google in 84.0%.

{% include figure.html
   src="/img/blog/crest-deep-research/ranking.svg"
   alt="Observed AI judge win rates: Caesar 97.5 percent, 390 of 400 wins, with a question-bootstrap interval of 95.2 to 99.2 percent; OpenAI Sol with web search 44.0 percent, 176 of 400, interval 41.0 to 47.0; Google Deep Research 8.5 percent, 34 of 400, interval 5.8 to 11.5."
   caption="Measured preferences in the published report. Lines show 95% question-bootstrap intervals; each rate uses 400 comparisons, including both opponents."
%}

Both judges ranked Caesar first, but their other preferences differed. Astra
gave OpenAI a 52.0% overall win rate and Google 0.0%; Argon gave them 36.0%
and 17.0%. The judges disagreed on 40 of 300 matched presentations (13.3%).
Balancing the panel therefore makes its composition visible without removing
judge dependence.

The intervals come from 1,000 resamples of the 50 questions, keeping all
12 decisions for each sampled question together. This preserves the dependence
among judgments about the same answers. The ranges describe sensitivity to
the observed question mix while holding the saved answers, judges, and rubric
fixed. They exclude variation from generating new answers, choosing other
judges, and uncertainty about whether the rubric captures creativity well.

Caesar's lead is substantial within this evaluation. Establishing how far it
extends requires additional tasks, repeated generations, independent factual
checks, and comparison with human or domain-expert judgments. The saved
evidence supports that next assessment while keeping the present finding
specific: a strong preference from this balanced AI panel.
