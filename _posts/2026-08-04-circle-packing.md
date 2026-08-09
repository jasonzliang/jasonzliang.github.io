---
layout: post
title: >-
  My AI agent's solver beat a record for packing 27 unequal circles
date: 2026-08-04
description: >-
  Five of six runs tied the best known packing of 26 circles, a benchmark
  that measures little. At 27, one beat the listed record.
image: /img/blog/2026-08-04-circle-packing/packings-26-per-run.webp
tags: [self-improving-agents, optimization, benchmarks]
record: Record
---

Pack 26 circles into a unit square. Any sizes, no overlaps, nothing outside.
Maximise the sum of their radii.

This objective is thinly studied next to the equal-circle version most people
picture, and became a benchmark for a kind of AI system: DeepMind's
[AlphaEvolve](https://arxiv.org/abs/2506.13131) showcased it, Sakana's
[ShinkaEvolve](https://arxiv.org/abs/2509.19349) pushed it to about
**2.635983**, best known rather than proven optimal. Both evolve populations of
candidate programs.

I ran six self-improvement agents at it. Each writes its own solver, improves it
over a fifteen-iteration budget, and builds in iteration one a scorer it may not
weaken later; every packing here was re-verified feasible outside the run that
produced it. None spent the budget: each stopped mid-iteration, having completed
ten to fourteen.

**Five of the six reached 2.635983085**, the best known value, on iterations one
to five, at a cost to first tie of **$2.48** to $16.11 in API spend. Five made
zero web searches; the one that searched did so for a different problem size,
after it had already tied.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/packings-26-per-run.webp"
   alt="Six panels, one per run, 26 circles of differing size in a square; five
        labelled 2.6359831 sharing one mirrored arrangement, the sixth
        2.6310936 and marked a distinct optimum."
   caption="Figure 1 of the report. The five ties are one arrangement up to
            reflection and relabelling: one optimum found five times, not five
            results. The published systems never released coordinates, so
            nothing is compared with theirs. Panel names are the report's
            labels: cautious control or expansive nietzsche, each frozen,
            bounded (-sm) or radical."
%}

## A saturated benchmark

My report says so: *"Matching the number is not a discovery... any competent
method reaches it."* Nor is it a tie at full precision: ShinkaEvolve's fuller
value, 2.635983099, is fractionally higher; the two agree to the six decimals
the record is quoted to. Five runs landing on the same value to nine decimal
places is not five independent successes; it is a ceiling, and everyone hitting
it. A measurement everything ties on has stopped measuring, the same failure as
[a vision model scoring every image mid-scale](/blog/image-generation/). As a
comparison between [the six conditions I was actually
testing](/blog/bin-packing-values/) this experiment is worthless, and the
mission file says so: *"treat this as a showcase of RSI on a famous problem, NOT
the clean probe of the values effect."* RSI is recursive self-improvement, the
loop above.

## The cost and the route

ShinkaEvolve reaches this benchmark by sampling on the order of 150 generated
programs. The fastest run got there inside its first iteration, for **$2.48**,
from a solver it wrote itself.

One iteration is not one shot. Inside it the agent issued five solver and scorer
commands, running its solver about fifteen times: a 40-second probe, eight seeds
at 400 seconds each, six more at 300 that held the result, call it 5,000
solver-seconds parallelised into a twenty-minute iteration, each run itself a
search (seed 1 alone tried 474 layouts and 785 kicks in its 400 seconds). So:
few programs, many packings evaluated, where an evolutionary loop writes many
programs and evaluates each once; those counts do not divide into a ratio and I
will not give one. My appendix is blunt: the tie "came from giving the same code
more compute," not from debugging inside the iteration. What is cheap is the
agent, not the CPU.

The *method* is not theirs either. They lay circles on a spiral or grid and
nudge them with local refinement and random restarts. The agent saw that the
problem splits: with the centres fixed, the best radii are the answer to a
linear program, solved exactly in milliseconds. That turns a search over 78
unknowns into one over 52 centre coordinates, the 26 radii filled in optimally
for free. Around it went a rougher outer search over the centres, jogging out of
dead ends, and the packing was checked in exact fractions, so "no circles
overlap" rests on arithmetic rather than a tolerance. That run spent its
remaining iterations generalizing the solver to other sizes and containers
rather than improving N=26.

A different run, control-sm, took until iteration five and $12.19 to tie,
keeping a log like a competent researcher's week, numbered in its own iteration
labels, which the report warns can drift from the loop's count at the relaunch
below: exact radii by linear program at 2, beating greedy radii on all four
seeds compared; Newton's method on the tangency equations at 4, the packing
pinned by exactly 78 contacts, circle to circle and circle to wall, so the
optimum solves an exact system rather than being crept towards; random kicks at
5 landing on a better structure one contact swap away, verified at 2.635983085;
at 6, enumerating the swaps instead of hoping, nothing within two swaps beating
the incumbent; at 10, a 348-seed search finding nothing better and showing the
winning structure's basin rare, reached by 2 of those 348 starts, 0.57%. Nobody
told it to do any of that.

## Four ways this could be oversold

**Not novel techniques:** linear programming, Newton's method, basin hopping and
rigidity certification are standard prior art; what is notable is the
*composition*, assembled autonomously, so *"we claim architectural recombination
and autonomous rediscovery, not technique novelty."* **Not a fair head-to-head
on cost:** the evolutionary systems report low per-task costs, under different
constraints, so $2.48 and one iteration is small in absolute terms, not a claim
to be cheaper. **Cost to first tie, not total:** the tie came in iteration one,
and the run went eleven more loop cycles, twelve in all, before I stopped it, at
$52.42. **A discarded attempt:** all six runs were launched, killed by my wall
clock twenty-two minutes in, and restarted, five resuming where they stopped.
The $2.48 run's attempt had committed nothing, so its counter reset to iteration
one, though its candidate packings were on disk, the best 2.583 and well short
of the tie, and the agent read them before writing a fresh solver. The $2.48
excludes those twenty-two minutes.

## A separate result, at 27 circles

I ran the $2.48 run's extracted solver at every board size from 2 to 100, 120
seconds each on one seed (26, the trained size, got more), against
[Packomania](https://www.packomania.com/csqv/csqv.html), the record book. Of the
98 sizes where it produced a usable packing, it matched the record to within
4e-11 on 27 of them, fell short on 70, several by more than 1%, and beat exactly
one: **27 circles**, improving the listed entry by 0.000629, a gain of 0.023% on
a value standing since 2011/12. Packomania listed it on 3 August 2026, crediting
the improvement over David Cantrell's earlier record and noting the packing's D1
symmetry.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/packing-old-vs-new.webp"
   alt="Three panels: two 27-circle packings summing to 2.685350 and 2.685979,
        alike in texture, and a bar chart of sorted radii changes from plus
        0.0075 to minus 0.0062, netting 0.00063."
   caption="They look alike because the gain is so small, but are not the same
            packing: the radii changes are up to twelve times that gain and
            nearly all cancel, so progress here is rearrangement, not slack.
            Caveats: the 2011/12 coordinates were never published, so the left
            panel is our own solver reproducing that record's total, and the
            bars pair radii by size, not circle by circle."
%}

Five qualifications:

- This is the **variable-radius** problem; the equal-circle version at N=27 is
  proven optimal and nothing here touches it.
- At 26 circles, the famous case, the agent **matched** the best known value, it
  did not beat it.
- The N=27 entry improved was a **classical human result**, not one of the
  recent AI-optimized entries.
- The record came from an operator-side sweep of the extracted solver, not from
  inside the self-improvement loop; the 50-seed runs came after, a check of how
  often it lands on the winning arrangement, about one in seven.
- **The self-improvement did not create this capability**, as my report says:
  the iteration-one solver already reaches the record-beating packing at some
  seed. Nine further solver iterations moved the per-seed hit rate from about
  10% to about 14%, all of it by iteration 4. The loop bought a better hit rate,
  not a new ability.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/n27-emergence.webp"
   alt="Two stacked panels against solver iteration 1 to 10: best of 50 seeds
        against the Packomania record line, and the share of those seeds
        beating it."
   caption="Figure 2 of the report: ten solver iterations of the fastest-tying
            run, each re-run on 27 circles at 120 seconds per seed over 50
            seeds, only five distinct solvers, the files unchanged from
            iteration 5 on. Best-of-50 is above the record at iteration 1 while
            the record run's own seed crosses only at iteration 4, and the
            share beating it goes 10% at iterations 1 and 2, 12 at 3, 14 from 4
            on, or 5 of the 50 seeds against 7, a few points of noise either
            way. One run, one board size."
%}

It is small, but anyone can check it: the output is a list of coordinates, and a
separate program sharing no code with the solver confirms it in a second. That
is the property I would most like more AI results to have: not "trust the
system," but "here is the artifact, and here is something that checks it."
