---
layout: post
title: >-
  Deriving agent values from research papers and auditing their sources
date: 2026-09-23
description: >-
  A literature-derived values file had 22 verified citations. Its paper ranking
  remained a proxy, and its effect on agent performance had not been tested.
image: >-
  /img/blog/2026-08-06-literature-values/citation-ledger.webp
tags: [self-improving-agents, agent-design, values]
---

A values file supplies behavioral guidance where an agent's task leaves choices
open: cautious improvement or ambitious revision, stopping at a working
solution or continuing to explore. Earlier experiments used hand-written
values, including a [Nietzsche-derived set](/blog/nietzsche/). Those exploratory
runs produced different artifacts without establishing a reliable performance
advantage.

This historical exercise instead derived values from research papers. It
separated two questions: whether the cited sources existed and whether those
sources justified useful agent instructions. The citation audit addressed the
first. No agent comparison had tested the resulting values at the time of this
exercise.

## The literature pipeline and citation audit

The research had two parts. **Part A** sought highly cited recent AI papers.
**Part B** covered self-improvement and agent research. A deep-research pipeline
used **107 sub-agents** and three-vote adversarial verification of claims. Those
procedures still depended on language models, so citation verification ran
separately from the pipeline that produced the lists.

The initial audit checked seventeen cited papers. Each identifier had to
resolve to the claimed title, first author and year. Sixteen used arXiv records;
AlphaGo Zero used its Nature record. All seventeen passed. Four headline
metrics used to support values were also checked against abstracts, with all
four reported as supported verbatim.

The lists were then expanded to ten papers apiece. Five additions—GPT-4,
Chain-of-Thought, ReAct, Toolformer and Voyager—passed the same identifier gate.
Each addition's core contribution also had to be supported by a quotation from
its own abstract. All five passed.

Across the exercise, **22 of 22 cited papers resolved**, with no fabricated
papers or misattributions found by those checks. That result establishes
bibliographic provenance within the audit's scope. It does not validate every
interpretation, establish a complete literature search or show that the
derived instructions improve an agent.

{% include figure.html
   src="/img/blog/2026-08-06-literature-values/citation-ledger.webp"
   alt="Two-column ledger of 22 citations and their resolved identifiers,
        grouped by research list. Orange rows mark five late additions;
        a dagger identifies Voyager."
   caption="The citation audit's ledger. Voyager was the only late addition
            that changed the wording of a value."
%}

## A verified source list with an unverified ranking

Part A originally aimed to identify the ten most-cited AI papers from
2020–2025 by absolute citation count. That ranking did not survive adversarial
verification. The replacement was the
[NLLG quarterly arXiv report](https://arxiv.org/abs/2412.12121), using a
publication-week z-score over **January 2023–September 2024**.

This proxy measures how strongly a paper stood out among papers published
around the same time. It does not rank cumulative citations across the intended
six-year period. Its twenty-one-month window excludes earlier work such as
GPT-3, ViT, CLIP, Stable Diffusion, AlphaFold, Chinchilla and PaLM because of
publication date, without judging their importance.

Part A also had weaker contribution summaries. Apart from GPT-4's verified
abstract, those summaries drew on established knowledge rather than quotations
checked against each primary paper, and carried a medium-confidence label.
Part B's contribution summaries were quoted from primary sources and received
a high-confidence label. These were the exercise's confidence assessments;
the bibliographic checks alone do not establish them.

## The proposed values

Each part produced five-bullet and three-bullet versions. The three-bullet
versions were defaults, following the existing instruction to retain exactly
three bullets and replace material rather than accumulate it. Their proposed
decision rules were:

Part A:

- Build on proven, openly shared foundations and align them to human intent
  through feedback, rather than chasing raw model scale.
- Measure outputs with explicit, scalable evaluation and ground them in
  retrieved, current evidence to keep results trustworthy and factual.
- Prefer efficiency over brute-force scale, using curated data and better
  architectures so capability comes from design, not size alone.

Part B:

- Learn from verified feedback and iterate: reflect on failures, critique and
  revise drafts, and keep only what works.
- Align to explicit intent through preference feedback and follow a written
  constitution, staying principled but never evasive.
- Self-improve against an objective verifier where one exists, learning from
  trials and reusing verified solutions rather than re-deriving.

These are proposed decision rules distilled from the selected literature.
They are not conclusions that the source papers directly tested as a combined
values document.

## Updating a capped values file

The five late additions went through a structured debate with two adversarial
advocates and a neutral judge. No new bullet was added. The resulting change
folded [Voyager](https://arxiv.org/abs/2305.16291)'s reuse of verifier-confirmed
skills into the existing verifier bullet. Both the three- and five-bullet caps
held.

The other four additions were judged redundant or too tactical. GPT-4 reinforced
existing evaluation guidance; Chain-of-Thought described an inference method;
ReAct and Toolformer overlapped with the act-and-check loop. The selection
criterion was whether a proposed value changed a decision, rather than whether
every paper received a separate summary.

Reuse also introduced a possible failure mode: maintaining a library could
displace solving the immediate task. The clause therefore retained its
verification requirement. The debate did not settle whether this guidance
belonged in values or in the agent runner. The related
[values-rewriting audit](/blog/values-rewriting/) documented why a size limit
was useful: an uncapped block had grown from seventeen to 446 lines.

## Limits inherited from the papers

The supporting findings retained their original scope:

- Reflexion reported HumanEval pass@1 rising from 80% to 91% against its own
  GPT-4 baseline. The exercise recorded capability dependence and no gain for
  weak base models.
- Self-Refine's roughly 20% absolute gain across seven tasks was driven by
  non-reasoning tasks. Later work disputes intrinsic self-correction on
  reasoning problems.
- Constitutional AI's absence of human labels applied to harmlessness;
  helpfulness still used human feedback, and people wrote the constitution.
- Game self-play results relied on simulators, clear rewards and perfect
  information. Applying them to coding agents was an analogy dependent on a
  strong verifier.

At this stage, the output was a sourced instruction set, not a demonstrated
improvement. Comparing it with hand-written values required independent runs
per condition and a fixed evaluation, following the limitations exposed in the
[earlier bin-packing study](/blog/bin-packing-values/). Later values research
constitutes separate evidence and should not be read back into this audit.
