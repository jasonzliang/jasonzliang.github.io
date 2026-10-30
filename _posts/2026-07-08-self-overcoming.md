---
layout: post
title: >-
  Values in self-improving agents: five design hypotheses
date: 2026-07-08
description: >-
  A proposal asks how starting values could shape the choices an agent makes
  as it improves its own tools and methods.
image: >-
  /img/blog/2026-07-08-self-overcoming/compounding.webp
tags: [self-improving-agents, agent-design, values]
---

A self-improving agent can change the tools, prompts or search procedures used
to produce its next result. Which changes it accepts depends on what counts as
an improvement. A process rewarded for benchmark performance may select
different successors from one rewarded for broader
capability, reliable verification or novel tasks.

An unpublished project memo, *The Self-Overcoming Thesis*, develops that idea
through five themes adapted from Nietzsche. It proposes that initial values
can influence a sequence of self-modifications. Its stronger prediction—that
small initial biases necessarily compound into sharply different agents—is a
hypothesis, not a measured result or mathematical theorem.

{% include figure.html
   src="/img/blog/2026-07-08-self-overcoming/compounding.webp"
   alt="Schematic chains from human-written generation zero through generations
        one, two and ten. Different initial criteria lead to two hypothetical
        endpoints: stronger conformity or continued capability expansion."
   caption="The memo's proposed trajectories. Neither endpoint has been
            demonstrated by this diagram or the exploratory values-file pair."
%}

## The concern behind the proposal

Human preference feedback can reward persuasive agreement as well as helpful
answers. [Perez et al.](https://arxiv.org/abs/2212.09251) found sycophantic
behavior in model-written evaluations. [Sharma et
al.](https://arxiv.org/abs/2310.13548) found that human and preference-model
judgments sometimes favor agreement with a user's beliefs over correctness.
[Casper et al.](https://arxiv.org/abs/2307.15217) survey broader limitations of
reinforcement learning from human feedback.

These findings motivate concern about acceptance criteria, but do not show
that ten rounds of agent self-editing amplify sycophancy. They also do not
establish the memo's claim that later corrections would be ineffective. Both
extensions require experiments on the actual modification-and-selection loop.

[Nietzsche's writing](https://plato.stanford.edu/entries/nietzsche/) discusses
self-overcoming, value creation and competing perspectives; it does not supply
a theory of machine-learning objectives. The memo turns those themes into
engineering proposals. Its formulations should be read as adaptations, rather
than quotations or technical claims attributable to Nietzsche.

## Five proposals and their existing counterparts

**1. Will to power: expand the available curriculum.** Instead of repeatedly
optimizing a fixed task, a system could generate new tasks near its current
learning frontier. [POET](https://arxiv.org/abs/1901.01753) jointly evolves
environments and agents. [OMNI](https://arxiv.org/abs/2306.01711) combines
learning progress with a foundation-model estimate of interestingness;
learnability alone can retain many repetitive tasks.
[Voyager](https://arxiv.org/abs/2305.16291) uses an automatic curriculum and a
growing library of executable Minecraft skills. These systems demonstrate
specific curriculum mechanisms, without testing the memo's broader values thesis.

**2. Self-overcoming: let the agent improve parts of its own machinery.** The
[Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) modifies agent code and
selects improvements through coding benchmarks.
[AlphaEvolve](https://arxiv.org/abs/2506.13131) evolves programs using automated
evaluators. Its reported results include a method multiplying two 4×4
complex-valued matrices with 48 scalar multiplications, improving on the
49-multiplication construction from applying Strassen's algorithm in that
setting.

Both systems improve programs. Neither demonstrates that changing the
evaluator's objectives, or freely rewriting values, improves the trajectory.
Testing that proposal requires a separate comparison and protected external
evaluation.

**3. Perspectivism: retain alternatives long enough to test them.** A system
could preserve incompatible hypotheses instead of collapsing them into an early
consensus. The engineering question is whether a diverse candidate archive,
followed by verification, outperforms a single selected candidate or a voting
baseline under the same compute budget. Philosophical pluralism motivates the
comparison; it cannot determine its outcome.

**4. Amor fati: reuse information from failure.** Failed attempts can reveal
constraints, supply negative examples or support revised goals.
[Hindsight Experience Replay](https://arxiv.org/abs/1707.01495) provides a
specific mechanism: relabeling experience with goals actually achieved, allowing
learning from episodes that failed at their original goal. That result supports
careful reuse of experience, rather than an unrestricted claim that every
failure is useful supervision.

**5. Apollonian and Dionysian: pair generation with a strict check.**
[AlphaGeometry](https://doi.org/10.1038/s41586-023-06747-5),
[AlphaProof](https://doi.org/10.1038/s41586-025-09833-y) and
[FunSearch](https://doi.org/10.1038/s41586-023-06924-6) combine learned proposal
mechanisms with symbolic, formal or computational evaluation. Their checks
provide different guarantees: a formal proof checker and a finite performance
benchmark are not interchangeable. The common design idea is to evaluate
proposals with a mechanism that can reject them, while recognizing the scope
of what that mechanism establishes.

## What a convincing test would require

The memo outlines a benchmark, baseline and rejection criterion for each
proposal. A useful comparison would match tokens and compute, keep evaluation
outside the agent's editing authority and test transfer on held-out problems.
An intervention that improves only its training benchmark would not establish
broader capability. Consistent losses to a fixed-objective baseline would
undermine the proposed advantage.

Generating new tasks and retaining multiple candidates can consume resources
without improving the final result, so the comparison must account for those
costs. A fixed objective remains a strong baseline whenever it captures
the intended task well.

The unresolved technical issue is how to reward expansion without rewarding
novelty for its own sake, evaluator manipulation or arbitrary changes to the
scaffold. Protected invariants and external tests constrain that problem; they
do not solve objective design automatically.

## Evidence so far

The [early two-run values comparison](/blog/nietzsche/) recorded different
working styles, with one run per condition and no reliable winner. Later work
examined values editing across more runs, and a
[repeated 2048 study](/blog/powered-replication/) qualified an initial claim
about generalization. Those experiments address parts of the motivation,
rather than validating all five proposals or the predicted compounding mechanism.

Testing the five proposals requires comparing how acceptance criteria affect
the capability and reliability of successor agents, as measured by an external
test.
