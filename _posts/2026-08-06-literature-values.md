---
layout: post
title: "I tried deriving an agent's values from the literature"
date: 2026-08-06
description: >-
  My self-improving agents run on a values file of three to five bullets. One I
  wrote from Nietzsche. This one I derived from cited papers, and then audited
  every citation to see whether any of them were invented.
image: >-
  /img/blog/2026-08-06-literature-values/citation-ledger.webp
tags: [self-improving-agents, agent-design, values]
---

Every self-improving agent I build runs on a values file. It sits at the top of
the document the agent reads at the start of each iteration, and it is three to
five bullets long. The bullets do not say what to *do*, because the task says
that. They say how to decide when the task leaves the choice open: take the
small proven step or the ambitious one, treat a working solution as finished or
as a platform to climb past.

Every one of those files, so far, I wrote by hand. [One of them I wrote from
Nietzsche](/blog/nietzsche/), which produced two agents that behaved differently
enough to tell apart at a glance, without establishing that either was better.

There is an obvious objection to writing them by hand. A large research
literature exists on how models and agents actually get better, and none of it
went into the file. So I tried the other thing: derive the bullets from cited
papers rather than from my taste, and see what comes out.

What came out is less interesting than how I checked it. This post is mostly
about the checking.

## The thing doing the reading is also an agent

I went after two sets of papers. **Part A** was meant to be the most-cited AI
papers of recent years, on the theory that what the field has actually built on
is evidence about what works. **Part B** was the self-improvement literature
specifically, which is the thing my agents are trying to do.

Both sets were gathered by a fan-out deep-research run: **107 sub-agents**, each
chasing a slice of the question, with **three-vote adversarial verification on
every claim**, so a claim survives only by holding up against deliberate
attempts to knock it down, not on one reader's say-so.

All of that machinery is itself a language-model pipeline, and language-model
pipelines invent citations. Not occasionally, and not obviously: a plausible
first author, a plausible title, a well-formed arXiv number, and no such paper.
If that happens even once in a values file, the file is no longer derived from
the literature. It is derived from my taste with a bibliography stapled on.

So every cited paper went through a separate **hallucination-audit pass**, run
independently of the pipeline that produced the citations.

## The audit result is the finding

The first pass checked 17 cited papers. The gate was mechanical: the paper's
identifier has to resolve to the claimed title, the claimed first author, and
the claimed year. For every cited paper but one that identifier is an arXiv ID;
the exception is AlphaGo Zero, which appeared in Nature and never went to arXiv,
so what resolves for it is the journal record. All 17 passed. Four headline
metrics, the specific numbers a value bullet leans on, were additionally checked
against the abstracts they came from, and **4 of 4 were supported verbatim**.

Both lists were then expanded to a full top ten. GPT-4 joined Part A;
Chain-of-Thought, ReAct, Toolformer and Voyager joined Part B. Those five went
through the same gate, and this time each paper's core contribution also had to
be quotable verbatim from its own abstract. **5 of 5 passed.**

That is **22 of 22 cited papers verified real, zero fabricated papers and zero
misattributions.**

{% include figure.html
   src="/img/blog/2026-08-06-literature-values/citation-ledger.webp"
   alt="A two-column ledger of the 22 cited papers, each row showing the paper
        and the identifier the audit resolved. The left column is Part A, the
        window-normalized top ten plus the ranking report it came from, its
        per-paper contributions drawn from established knowledge at medium
        confidence. The right column is Part B, the self-improving-agent
        papers, its contributions quoted from the primary sources at high
        confidence. Five rows are orange, marking the five late additions."
   caption="Every paper the report cites, with the identifier the audit
            resolved, so anyone can repeat the check. Blue rows went through
            the first audit, 17 of 17 real with 4 of 4 headline metrics
            verbatim-supported. Orange rows are the five late additions, 5 of 5
            real with each core contribution quoted verbatim. Voyager,
            daggered, is the only late addition that changed a value."
%}

It is worth being precise about what a clean sheet buys, because it would be
easy to oversell. It does not make the reasoning built on those papers correct.
It does not make the values good. It establishes one narrow thing: no bullet in
the document is propped up by a paper that does not exist, and no citation
points at the wrong paper. Given how routinely that fails, and how invisible the
failure is to a reader, a stated gate with a stated score strikes me as the
minimum bar for a document like this.

The gate being mechanical is the point. Every identifier it resolved is in the
ledger above, so anyone can rerun it.

## The part that could not be verified

Part A was supposed to be the top ten most-cited AI papers of 2020 to 2025 by
absolute citation count. **That list could not be adversarially verified.** No
ranking of that shape survived the same scrutiny the individual papers did.

The best verifiable substitute is the NLLG quarterly arXiv report, which ranks
papers by a **publication-week z-score** rather than by absolute count, over
**January 2023 to September 2024 only**. Both halves of that matter. Normalizing
by week measures how far a paper stood out from the papers around it, which is
not the same quantity as how much it has been cited since. And the window
systematically excludes the pre-2023 canon: GPT-3, ViT, CLIP, Stable Diffusion,
AlphaFold, Chinchilla and PaLM are all absent, not because they were judged
unimportant but because they were published before the window opens.

So Part A is distilled from a window-normalized proxy list, not from a literal
citation-ranked top ten. I am putting that in the body rather than a footnote
because it changes what the Part A values are evidence *of*: they reflect what
stood out inside that twenty-one-month window of arXiv, not what the field has
cited most.

There is a second asymmetry between the two halves, and it runs the same way.
Part B's per-paper contributions are quoted from the primary sources. Part A's
are drawn from established knowledge rather than lifted from the papers, with
the verified GPT-4 abstract as the exception, and they carry a **medium
confidence** label. The papers in both halves are equally verified. The one-line
accounts of what each one contributed are not, and I am not presenting them as
though they were.

## What actually came out

Each set exists in a five-bullet and a three-bullet version. The three-bullet
versions are the recommended defaults, for a reason I will come back to.

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

Part B is the more useful of the two to me, because it is about how to run a
loop rather than how to build a model.

## A structured debate decided what changed

The five late additions raised a question I wanted answered properly: does a new
paper on the list mean a new bullet in the values?

The instinctive answer is yes, and the instinctive answer is how a values file
turns into a document nobody reads. I have [watched an uncapped value block grow
from 17 lines to 446](/blog/values-rewriting/).

So the question ran as a structured debate: two adversarial advocates, one
arguing each side, and a neutral judge. The verdict was to keep every bullet,
with exactly one refinement.

Voyager's disposition, which is to save a solution a verifier has confirmed as a
reusable skill and build on it later, was **folded into the existing verifier
bullet as a clause**. Not appended as a sixth value: folded in, replace rather
than accrete, with the three- and five-bullet caps holding. In the Part B list
above, that fold is the phrase "reusing verified solutions rather than
re-deriving."

The other four were judged not to have earned a bullet, each for a stated
reason. GPT-4's lesson already sits inside Part A's evaluation bullet, "measure
before you trust." Chain-of-Thought is an inference-time tactic rather than a
disposition. ReAct and Toolformer describe the act-and-check loop the verifier
bullet already implies.

I find that more interesting than the values themselves. Four out of five new
papers, all verified real, all good enough to complete a top-ten list, changed
nothing. A value is not a summary of a paper; it is a rule that has to change a
decision. If a candidate bullet does not change something an existing bullet was
not already changing, it is a citation, not a value.

The closest call was the one change that did land. Reuse is exactly the sort of
instruction that can go wrong, because an agent rewarded for reuse builds a
library instead of a solution. The clause stays verifier-gated, so reuse is
scored rather than rewarded for its own sake. Whether it belongs in the values
at all or only in the harness that runs them was the debate's narrowest margin,
and I would rather record that than pretend it was settled.

## The caveats travel with the bullets

A value derived from a result inherits that result's limits, so the caveats
attached to the sources travel into the file with them:

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

That last one deserves emphasis, because the strongest bullet in Part B leans on
it. "Self-improve against an objective verifier where one exists" is only as
good as the verifier, and the clause "where one exists" is doing real work.

On the question of how many bullets: three to five distinct, decision-changing
ones, with three as the target. That is not an aesthetic preference. My agents'
own constitution rule, "exactly three bullets; replace, don't accrete," is the
empirically converged target, and by that standard the five-bullet versions here
over-populate slightly. The three-bullet lists are the defaults.

## What I think this was worth

The honest status: I have not run these as a condition. Nothing here says a
literature-derived values file produces a better agent than a hand-written one.
That comparison needs several runs per condition, and I have [written about what
happens when I skip that step](/blog/powered-replication/).

What I have is a provenance story I did not have before. The Nietzsche file was
chosen for a disposition I could not find in any paper, and its defence is that
it did something interesting. This file's defence is that every bullet traces to
a paper an independent audit confirmed is real and correctly cited, that the
ranking behind half of it is labelled as the proxy it is, and that a new bullet
had to argue its way past a standing bias toward keeping the file short.

Side by side, the literature-derived set is the more defensible and the less
surprising. That is the trade, and it is the experiment I would like to run
next: whether a values file where every bullet has a citation behaves any
differently from one where every bullet has a philosopher.
