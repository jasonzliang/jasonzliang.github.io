---
layout: post
title: >-
  An AI agent's values from papers: citations real, values untested
date: 2026-08-06
description: >-
  I derived an agent's values file from cited papers, then audited every
  citation: 22 of 22 real, none invented, no new bullets earned.
image: >-
  /img/blog/2026-08-06-literature-values/citation-ledger.webp
tags: [self-improving-agents, agent-design, values]
---

Every self-improving agent I build runs on a values file: three to five bullets
at the top of the document the agent reads each iteration. The bullets do not
say what to *do*, because the task says that; they say how to decide when the
task leaves the choice open: take the small proven step or the ambitious one,
treat a working solution as finished or as a platform to climb past. Every one I
wrote by hand. [One from Nietzsche](/blog/nietzsche/), run against an otherwise
identical baseline, produced two agents that behaved differently enough to tell
apart at a glance, without establishing that either was better.

The objection is that a large research literature exists on how models and
agents get better, and none of it went into the file. So I tried deriving the
bullets from cited papers instead of from my taste. What came out is less
interesting than how I checked it.

## The thing doing the reading is also an agent

I went after two sets of papers. **Part A** was meant to be the most-cited AI
papers of recent years. **Part B** was the self-improvement literature, the
thing my agents are trying to do. Both sets were gathered by a fan-out
deep-research run: **107 sub-agents** with **three-vote adversarial verification
on every claim**, so a claim survives only by holding up against attempts to
knock it down.

That machinery is itself a language-model pipeline, and language-model pipelines
invent citations: a plausible author and title, a well-formed arXiv number, and
no such paper. If that happens even once, the file is not derived from the
literature but from my taste with a bibliography stapled on. So every cited
paper went through a **hallucination-audit pass**, run independently of the
pipeline that produced the citations.

## 22 of 22 citations resolved

The first pass checked 17 cited papers. The gate was mechanical: the identifier
has to resolve to the claimed title, first author and year. The identifier is an
arXiv ID for every paper but AlphaGo Zero, which was in Nature, so its journal
record resolves. All 17 passed. Four headline metrics, the numbers a value
bullet leans on, were checked against their abstracts, and **4 of 4 were
supported verbatim**.

Both lists were expanded to a full top ten. GPT-4 joined Part A;
Chain-of-Thought, ReAct, Toolformer and Voyager joined Part B. Those five went
through the same gate, and each paper's core contribution also had to be
quotable verbatim from its own abstract. **5 of 5 passed.**

That is **22 of 22 cited papers verified real, zero fabricated papers and zero
misattributions.**

{% include figure.html
   src="/img/blog/2026-08-06-literature-values/citation-ledger.webp"
   alt="A two-column ledger of the 22 cited papers, each row giving the paper
        and the identifier the audit resolved. Part A on the left is the
        window-normalized top ten, Part B on the right the self-improving-agent
        papers; five orange rows are the late additions, and a dagger marks
        Voyager."
   caption="Voyager, daggered, is the only late addition that changed a value."
%}

What a clean sheet buys is narrow. It does not make the reasoning built on those
papers correct, nor the values good. It establishes that no bullet is propped up
by a paper that does not exist and no citation points at the wrong paper. Given
how routinely that fails, and how invisibly, a stated gate with a stated score
is the minimum bar. Every identifier it resolved is in the ledger above, so
anyone can rerun it.

## The part that could not be verified

Part A was supposed to be the top ten most-cited AI papers of 2020 to 2025 by
absolute citation count. **That list could not be adversarially verified.** No
ranking of that shape survived the same scrutiny the individual papers did.

The best verifiable substitute is the [NLLG quarterly arXiv
report](https://arxiv.org/abs/2412.12121), which ranks papers by a
**publication-week z-score** rather than absolute count, over **January 2023 to
September 2024 only**. Both limits matter. Normalizing by week measures how far
a paper stood out from the papers around it, not how much it has been cited
since. And the window excludes the pre-2023 canon: GPT-3, ViT, CLIP, Stable
Diffusion, AlphaFold, Chinchilla and PaLM are all absent, not because they were
judged unimportant but because they predate it. So Part A is distilled from a
window-normalized proxy list, not a literal citation-ranked top ten, which
changes what its values are evidence *of*: what stood out in that
twenty-one-month window of arXiv, not what the field has cited most.

Part A is the weaker half in a second way. Part B's per-paper contributions are
quoted from the primary sources; Part A's are drawn from established knowledge
rather than lifted from the papers, with the verified GPT-4 abstract as the
exception, and carry a **medium confidence** label. The papers in both halves
are equally verified. The one-line accounts of what each contributed are not,
and I am not presenting them as though they were.

## What actually came out

Each set exists in a five-bullet and a three-bullet version; the three-bullet
ones are the defaults, matching the rule my agents' own constitution converged
on: "exactly three bullets; replace, don't accrete." By that standard the
five-bullet versions over-populate slightly.

Part A, from the top-cited proxy list, at medium confidence:

> - Build on proven, openly-shared foundations and align them to human intent
>   through feedback, rather than chasing raw model scale.
> - Measure outputs with explicit, scalable evaluation and ground them in
>   retrieved, current evidence to keep results trustworthy and factual.
> - Prefer efficiency over brute-force scale, using curated data and better
>   architectures so capability comes from design, not size alone.

Part B, from the self-improving-agent papers, at high confidence:

> - Learn from verified feedback and iterate: reflect on failures, critique and
>   revise your drafts, and keep only what works.
> - Align to explicit intent through preference feedback and govern yourself by
>   a written constitution, staying principled but never evasive.
> - Self-improve against an objective verifier where one exists, learning from
>   your own trials and reusing verified solutions rather than re-deriving.

## Adding papers did not add bullets

Does a new paper on the list mean a new bullet? The instinctive answer is yes,
and the instinctive answer is how a values file turns into a document nobody
reads. I have [watched an uncapped value block grow from 17 lines to
446](/blog/values-rewriting/). So the five late additions went to a structured
debate, two adversarial advocates and a neutral judge, which kept every bullet
with one refinement.

[Voyager](https://arxiv.org/abs/2305.16291)'s disposition, saving a
verifier-confirmed solution as a reusable skill and building on it later, was
**folded into the existing verifier bullet as a clause** rather than appended as
a sixth value: replace, do not accrete, with the three- and five-bullet caps
holding. In the Part B list above it is the phrase "reusing verified solutions
rather than re-deriving."

The other four did not earn a bullet, each for a stated reason. GPT-4's lesson,
"measure before you trust," is what Part A's evaluation bullet already asks for.
Chain-of-Thought is an inference-time tactic rather than a disposition, and
ReAct and Toolformer describe the act-and-check loop the verifier bullet
implies. Four of five new papers, all verified real, changed nothing. A value is
not a summary of a paper; it is a rule that has to change a decision.

The change that did land carries a risk: an agent rewarded for reuse builds a
library instead of a solution, so the clause stays verifier-gated. Whether it
belongs in the values at all or only in the harness that runs them was the
debate's narrowest margin, and I would rather record that than pretend it was
settled.

## The caveats travel with the bullets

A value inherits the limits of the result it came from, so those caveats travel
into the file with it:

- Reflexion's improvement from 80% to 91% on the HumanEval coding benchmark
  (pass@1) is self-reported against its own GPT-4 baseline, and it is
  capability-gated: no gain on weak base models.
- Self-Refine's roughly 20% absolute gain across seven tasks is driven by the
  non-reasoning ones, and later work disputes intrinsic self-correction on
  reasoning.
- Constitutional AI's "no human labels" claim applies to harmlessness only.
  Helpfulness still uses human feedback, and humans write the constitution.
- The self-play results are from games: perfect information, a cheap simulator,
  an unambiguous reward. Carrying them into a coding agent is an analogy, and it
  holds only to the extent a strong verifier exists.

That last one matters most, because the strongest bullet in Part B leans on it:
"Self-improve against an objective verifier where one exists" is only as good as
the verifier, and "where one exists" is doing real work.

## Provenance, not a better agent

The honest status: I have not run these as a condition. Nothing here says a
literature-derived values file produces a better agent than a hand-written one.
That comparison needs several runs per condition, and I have written about [what
happens when I skip that step](/blog/bin-packing-values/).

What I have instead is provenance. Against the Nietzsche file, whose defence is
that it did something interesting, the literature-derived set is the more
defensible and the less surprising. That is the trade, and the next experiment:
whether a values file where every bullet has a citation behaves any differently
from one where every bullet has a philosopher.