---
layout: post
title: >-
  Five of six agents tied a famous packing benchmark. Getting there cost $2.48
  to $16.11.
date: 2026-08-04
description: >-
  The agents reached the best known packing of 26 circles without a web search,
  on a benchmark where any competent method ties. Matching that number is not a
  discovery, the interesting part is what it cost.
image: >-
  /img/blog/2026-08-04-circle-packing/packings-26-per-run.webp
tags: [self-improving-agents, optimization, benchmarks]
---

Pack 26 circles into a unit square. They can be any size, they cannot overlap,
and they must stay inside. Make the sum of their radii as large as possible.

Circle packing is an old and heavily worked corner of geometry, though this
particular objective, maximise the sum of the radii, is thinly studied next to
the equal-circle version most people picture. It became a benchmark for a
particular kind of AI system. DeepMind's AlphaEvolve used it as a showcase, and
Sakana's ShinkaEvolve pushed it to the best known value, a sum of radii of about
**2.635983**, which is best known rather than proven optimal. Those systems work
by evolving populations of candidate programs, sampling many at a time and
selecting.

I ran six self-improvement agents at it. Each one writes its own solver from
scratch and improves it against a budget of fifteen iterations. It also builds
its own scorer in its first iteration and is then forbidden to weaken it, and
every packing quoted here was re-verified feasible afterwards, outside the run
that produced it. None of them spent the whole budget: every one was stopped
part-way through an iteration, having completed somewhere between ten and
fourteen of them. Every one had also been killed and restarted once, twenty-two
minutes in, which the ledger below returns to because of what it does to the
iteration numbering.

**Five of the six reached 2.635983085**, the best known value. The fastest got
there on **iteration one**, for **$2.48** of API spend, and that run cost $52.42
in total. Across the five, the tie came somewhere between the first and fifth
iteration, at a cost to first tie of between $2.48 and $16.11. Five of the six
runs made zero web searches; the sixth made one, for a different problem size,
after it had already tied.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/packings-26-per-run.webp"
   alt="Six panels, one per run, each showing 26 circles of differing size
        packed into a square. Five are labelled as tying the best known sum of
        radii at 2.6359831 and show the same arrangement, mirrored between
        panels. The sixth, labelled 2.6310936 and marked as a distinct optimum,
        settled somewhere visibly different, with a large circle in the middle
        left."
   caption="Figure 1 of the report, reproduced as the report drew it. The
            packing each of the six runs finished with. The five that tie land
            on the same arrangement, identical up to reflection and
            relabelling, so this is one optimum found five times rather than
            five separate results. Nothing here is compared against the
            published systems' own layouts, because they never released
            coordinates. The panel names are the report's internal condition
            names, and, as the next section says, the comparison between those
            conditions is not one this experiment can support."
%}

## Matching the number is not a discovery

I want to put that in the second section rather than bury it, because the
headline above is the kind of thing that gets misread.

2.635983 is the best known value on a saturated benchmark, and any competent
method reaches it. My own report says so in as many words: *"Matching the number
is not a discovery. 2.635983 is the known optimum for a saturated benchmark; any
competent method reaches it."*

Nor is it exactly a tie at full precision. ShinkaEvolve's fuller reported value,
2.635983099, is fractionally higher than ours; what the two share is agreement
at the six decimal places the record is normally quoted to.

Five of six runs landing on the same value to nine decimal places is not five
independent successes. It is a benchmark with a ceiling, and everyone hitting
the ceiling. A measurement that everything ties on has stopped measuring, which
is the same failure I ran into when [a weaker vision model scored every
candidate image at the middle of its scale](/blog/image-generation/): the
pipeline runs, numbers come out, and the ranking carries no information at all.
As a comparison between the six conditions I was actually testing, the
experiment is worthless, and the mission file I handed the agents says so up
front: *"treat this as a showcase of RSI on a famous problem, NOT the clean
probe of the values effect."* RSI there is recursive self-improvement, the loop
described above: the agent writes a solver, has it scored, rewrites it, and
repeats.

So what is left?

## What is left is the cost and the route

The interesting quantities are the ones on the left of the decimal point.

**$2.48, one iteration, no web access.** ShinkaEvolve reaches this benchmark by
sampling on the order of 150 generated programs. The agent here reached the same
answer inside its first iteration, having written the solver itself, without
looking anything up.

That is one iteration, not one shot, and the difference matters when you are
setting it beside a number like 150. Inside that iteration the agent issued five
solver and scorer commands, which ran its own solver about fifteen times: a
40-second probe, then eight seeds at 400 seconds each, then six more at 300
seconds that held the result. Call it 5,000 seconds of solver time, run in
parallel so it fits inside a twenty-minute iteration. And each of those runs was
itself a search: seed 1 alone tried 474 fresh layouts and 785 kicks inside its
400 seconds. So the agent wrote very few programs and evaluated a great many
packings, where an evolutionary loop writes many programs and evaluates each
once. The report's position is that those counts do not divide into a ratio, and
I am not going to give one. My own appendix is blunt about where the tie came
from: it "came from giving the same code more compute," not from debugging it
inside the iteration. What is cheap here is the agent, not the CPU.

And the *method* it wrote is not the method those systems use. The evolutionary
systems generally lay circles out on a spiral or grid and then nudge them with
local refinement and random restarts. The agent built something more
mathematical. It saw that the problem splits in two: once the centres are fixed,
the best radii for those centres are the answer to a linear program, the
textbook kind of optimisation a computer solves exactly and in milliseconds
instead of creeping up on it. That turns a search over 78 unknowns into a search
over the 52 centre coordinates, with the 26 radii filled in optimally for free.
Around that exact inner step it wrapped a rougher outer search over the centres,
restarting and jogging the layout to climb out of dead ends, and then checked
the finished packing in exact fractions, so that "no circles overlap" rests on
arithmetic rather than on a tolerance.

That description is of the $2.48 run, which tied on its first iteration and
spent its remaining iterations generalizing the solver to other sizes and
containers rather than improving the n=26 result.

A different run, control-sm in the report's naming, took until iteration five
and $12.19 to tie, and kept a log that reads like a competent researcher's week.
These are its own labels for its own iterations, which the report warns can
drift from the loop's count on a run that was relaunched:

- iteration 2, exact radii by linear program, which beat the greedy rule it had
  been using on all four seeds it compared
- iteration 4, Newton's method on the tangency equations: the packing turns out
  to be pinned by exactly 78 contacts, circle against circle and circle against
  wall, which makes the optimum the solution of an exact system rather than
  something to creep towards
- iteration 5, random kicks out of that solution land on a better structure one
  contact swap away, verified at 2.635983085
- iteration 6, enumerate the contact swaps systematically instead of hoping:
  nothing within two swaps beats the incumbent
- iteration 10, a 348-seed search finds nothing better, and establishes that the
  winning structure is a rare basin, reached by 2 of those 348 random starts,
  0.57%

Nobody told it to do any of that.

## The honest ledger

Four things I have to say plainly, because each of them is a way this result
could be oversold.

**Not novel techniques.** Every component of the machinery these runs built has
clear prior art. Linear programming, Newton's method, basin hopping and rigidity
certification are all standard. What is notable is the *composition*: that the
agents assembled these stacks autonomously, from their own knowledge, rather
than being shown them. My own write-up draws the boundary in as many words: *"we
claim architectural recombination and autonomous rediscovery, not technique
novelty."*

**Not a fair head-to-head on cost.** The evolutionary systems report low
per-task costs of their own, and they were solving the problem under different
constraints. I am not claiming to be cheaper than them. I am saying $2.48 and
one iteration is a small number in absolute terms.

**The $2.48 is cost to first tie, not total**, as noted above. The tie happened
in the first iteration; that run then kept going for eleven more loop cycles
before it was stopped, twelve in all, and cost $52.42.

**There was a discarded first attempt.** All six runs were launched once, killed
by my own wall clock twenty-two minutes in, and restarted. Five of them picked
up where they had stopped. The $2.48 run is the one whose first attempt had
committed nothing, so its counter went back to iteration one; that attempt's
candidate packings were still on disk, the best of them 2.583 and well short of
the tie, and the agent read them before writing a fresh solver. The $2.48 does
not include those discarded twenty-two minutes.

## A separate result, at 27 circles

While I was here, I ran the extracted solver at every board size from 2 to 100,
120 seconds each on a single seed (26, the trained size, got more), and compared
against Packomania, the reference table the field treats as its record book. Of
the 98 sizes where it produced a usable packing, it reproduced the listed record
at 27 of them to within 4e-11, fell short at 70, several by more than 1%, and
beat exactly one.

The one it beat is **27 circles**, where it improved the listed entry by
0.000629, a gain of 0.023%. That entry has stood since 2011/12. I have not
submitted the new packing, and the table moves: roughly 25 of its entries
changed two days before I fetched it, so this is a win against the table as of 3
August 2026.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/packing-old-vs-new.webp"
   alt="Three panels. The left and middle each show 27 circles of differing
        size packed into a square, summing to 2.685350 and to 2.685979, similar
        in overall texture but not the same arrangement. The right panel is a
        bar chart of how the sorted list of radii changed, from the largest
        circle to the smallest: individual changes run from plus 0.0075 to
        minus 0.0062 and cancel down to a net gain of 0.00063."
   caption="Twenty-seven circles, each free to be any size, packed into a unit
            square at the previous record's total and at the new one. They look
            alike because the gain is only 0.000629, but they are not the same
            packing. The right panel shows why the gain is so small: individual
            radii move by up to twelve times it, and nearly all of that
            cancels, so progress here is rearrangement rather than obvious
            slack. Two caveats on the bars: the left panel is our own solver
            reproducing the previous record's total, because the original
            coordinates were never published, and they line the two packings'
            radii up by size rather than circle by circle."
%}

Five qualifications, all of which matter:

- This is the **variable-radius** problem. The equal-circle version at N=27 is
  proven optimal and nothing here touches it.
- At 26 circles, the famous case, the agent **matched** the best known value. It
  did not beat it.
- The entry improved at N=27 was a **classical human result**, not one of the
  recent AI-optimized entries.
- The record came from an operator-side sweep of the extracted solver, 120
  seconds per board size on a single seed, not from inside the self-improvement
  loop. The 50-seed runs came afterwards, as a retrospective check on how often
  that solver lands on the winning arrangement at all: about one start in seven.
- **The self-improvement did not create this capability.** My own report says so
  in as many words. The record-beating packing is reachable at some seed by the
  iteration-one solver, the $2.48 one. Nine further iterations moved the
  per-seed hit rate from about 10% to about 14%, which is the difference between
  needing ten random restarts and needing seven, and all of that movement had
  happened by iteration 4. What the loop bought at n=27 was a better hit rate,
  not a new ability.

{% include figure.html
   src="/img/blog/2026-08-04-circle-packing/n27-emergence.webp"
   alt="Two stacked panels, both against solver iteration 1 to 10. In the top
        panel the best of 50 seeds already sits above the Packomania record
        line at iteration 1, while the single seed the record run actually used
        only crosses that line at iteration 4. The bottom panel is a bar chart
        of the share of the 50 seeds that beat the record, rising from 10
        percent at iterations 1 and 2 to 12 percent at iteration 3 and 14
        percent from iteration 4 onward."
   caption="Figure 2 of the report, reproduced as the report drew it. The ten
            iterations of the run that tied fastest, each re-run on 27 circles
            at 120 seconds per seed over 50 seeds. Only five of those ten are
            distinct solvers: from iteration 5 the solver files stop changing.
            It is the deflating figure of the study, so here it is: the
            record-beating packing was already reachable by that run's
            iteration-1 solver, the one that cost $2.48, and the nine
            iterations after it moved the per-seed hit rate only from 10
            percent to 14 percent, which at 50 seeds is 5 seeds against 7 and
            carries a few points of noise either way. The report's verdict is
            that self-improvement did not create this capability, it made it
            somewhat more reliable to find. One run, one board size."
%}

A 0.023% improvement on a number nobody had moved since 2011/12 is a real but
small thing. The result is independently checkable, which is what I like about
it: the output is a list of coordinates, and a separate program that shares no
code with the solver confirms it in a fraction of a second.

That is the property I would most like more AI results to have. Not "trust the
system," but "here is the artifact, and here is something else that checks it."
