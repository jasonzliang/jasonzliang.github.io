---
layout: post
title: >-
  An AI-generated solver improved the 27-circle packing record
date: 2026-08-24
description: >-
  Five of six agents matched the six-decimal benchmark for 26 unequal circles.
  A separate sweep improved the listed 27-circle result by 0.023%.
image: /img/blog/2026-08-04-circle-packing/packings-26-per-run.webp
tags: [self-improving-agents, optimization, benchmarks]
record: Record
---

Packing unequal circles into a unit square means choosing their centres and
radii so that every circle fits and none overlap. The objective is to maximize
the sum of radii. A solver written by a self-improving agent produced a
27-circle packing with total **2.685978684198**, improving the previous listed
value of **2.685350025228** by **0.023%**. Packomania credited the result on
3 August 2026.

The result came from a separate sweep of a solver developed on 26 circles.
It provides a checkable optimization artifact, while the agent experiment
itself offers limited evidence about the benefits of self-improvement.

## Six runs on the 26-circle benchmark

[AlphaEvolve](https://arxiv.org/abs/2506.13131) and
[ShinkaEvolve](https://arxiv.org/abs/2509.19349) used the 26-circle problem as a
program-evolution benchmark. Its best-known total was approximately
**2.635983**; global optimality had not been proved.

Six agents each received a fifteen-iteration budget to write and improve a
solver. Each built a scorer in its first iteration and could not weaken it
later. Separate verification checked the resulting packings. The runs stopped
mid-iteration after completing ten to fourteen iterations.

**Five of six reached 2.635983085**, in iterations one through five. API spend
to the first match ranged from **$2.48 to $16.11**. Five made no web searches;
the sixth searched another problem size after reaching the benchmark.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/packings-26-per-run.webp"
   alt="Six 26-circle packings. Five have total radius 2.6359831 and the same
        arrangement up to reflection; the sixth totals 2.6310936."
   caption="Five runs recovered one arrangement up to reflection and relabelling.
            Panel labels combine cautious (control) or expansive (nietzsche)
            dispositions with three levels of permission to rewrite values.
            The published comparison systems supplied no coordinates for a
            direct comparison of arrangements."
%}

These were matches at the benchmark's quoted six-decimal precision.
ShinkaEvolve's fuller value, **2.635983099**, is slightly higher. Repeatedly
recovering the same arrangement also left little room to distinguish
[the experimental conditions](/blog/bin-packing-values/). This task therefore
served mainly as a demonstration of autonomous solver construction.

## Low API cost, substantial solver compute

The fastest match occurred in the first completed iteration, but that iteration
contained substantial search: about fifteen solver executions, including eight
400-second seeds and six 300-second seeds. Roughly **5,000 solver-seconds** ran
in parallel within about twenty minutes. One 400-second seed tried 474 layouts
and 785 perturbations.

ShinkaEvolve reports about 150 generated programs for this benchmark. Those
program counts cannot be compared directly with iterations or packing
evaluations. The **$2.48** measures agent API spend to the first match, rather
than CPU cost or a matched-budget advantage over another system.

It also excludes a discarded launch. All six runs were interrupted after
22 minutes and restarted; five resumed their previous state. The fastest run
had committed nothing, so its iteration counter reset, although it read saved
candidates reaching about 2.583 before writing a fresh solver. Its eventual
twelve-cycle run cost **$52.42**.

The solver separated centre placement from radius selection. With centres
fixed, a linear program finds the best radii, reducing the outer search from
78 variables to 52 coordinates. Perturbations helped escape local optima, and
exact-fraction checks certified feasibility. In control-sm, LP radii beat
greedy radii on all four seeds compared. That run added Newton refinement of
the 78 contact equations and enumerated contact swaps, finding no improvement
within two swaps of the incumbent. It later recovered the winning structure
in only **2 of 348** fresh starts. These are examples of autonomous
recombination and rediscovery of established techniques.

## The separate 27-circle result

An operator-side sweep ran the extracted solver from **N=2 through N=100**,
using one seed and 120 seconds per size, with extra compute for the training
size N=26. Against the historical
[Packomania table](https://www.packomania.com/csqv/csqv.html), it produced
98 usable packings: **one improvement, 27 matches within 4e-11, and 70 below
the listed value**. Several shortfalls exceeded 1%.

The improvement was at N=27, over David Cantrell's 2011/12 entry. Packomania
listed the new total with D1 symmetry. This is the variable-radius problem;
the separate equal-circle problem is unaffected.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/packing-old-vs-new.webp"
   alt="Two 27-circle packings with totals 2.685350 and 2.685979, followed by
        changes in their sorted radii, which sum to approximately 0.00063."
   caption="The previous coordinates were unavailable, so the left panel is a
            solver-generated packing reproducing the old total. Bars compare
            radii by size, without identifying corresponding circles. Large
            positive and negative changes mostly cancel."
%}

The winning packing was found outside the self-improvement loop. Later tests
also showed that **the iteration-one solver already had this capability**:
5 of 50 seeds exceeded the old N=27 record. By iteration four, 7 of 50 did.
The loop improved the observed success rate from 10% to 14%, rather than
creating the ability to exceed that value. With only 50 seeds per version,
that small change remains uncertain.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/n27-emergence.webp"
   alt="Best total and fraction beating the historical 27-circle record across
        ten solver versions, each evaluated on 50 seeds at 120 seconds per seed."
   caption="The best of 50 seeds exceeds the old record at iteration one;
            the sweep's seed first does so at iteration four. Success counts
            are 5 of 50 at iterations one and two, 6 at three, and 7 from four
            onward. There are five distinct solver files; versions five
            through ten are unchanged."
%}

The result improves one historical human-contributed entry. It establishes
neither a global optimum nor superiority to recent AI systems on equal
budgets. Its strongest evidence is the artifact itself: saved coordinates and
[a separate verifier](https://github.com/jasonzliang/circle-packing-sota)
allow the geometry and total to be checked independently of the agent's account.
