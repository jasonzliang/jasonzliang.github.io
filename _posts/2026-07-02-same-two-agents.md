---
layout: post
title: "I called it a replication. My own audit called it a tie."
date: 2026-07-02
description: >-
  I ran the same one-file values swap on a second mission catalog, saw the same
  split, and wrote it up as a replication. Three weeks later I analysed the same
  four runs again and called the two agents near-indistinguishable.
image: >-
  /img/blog/2026-07-02-same-two-agents/what-replicated.webp
tags: [self-improving-agents, values, replication]
---

In June I ran [two sixty-iteration agents that differed only in a values
file](/blog/nietzsche/). They came out visibly different, and the honest
conclusion was that at one run per condition there was no reliable winner.

Then I ran the same one-file swap again on two unrelated mission catalogs, four
runs in total, and the character split came out the same shape both times. On 24
June I put a slide in a deck headed "The persona contrast — replicated".

I have since written about those same four runs twice more. On 15 July I
concluded that on the mission where the comparison is cleanest the two agents
are nearly indistinguishable, and that the philosophy "left no fingerprint but
the words". On 24 July I told myself not to lean on either of the first two
readings.

All three rounds are mine. This post is what is left when I put them side by
side, which is less than the first claimed and a little more than the second
allows.

## The four runs

These four runs used the loop's focused mode. On iteration 1 the agent browses a
curated list of research repositories read-only, picks one target, and vendors
it offline. Then it builds its own benchmark: inputs, a scoring script, a
measured baseline, and a `CRITERION.md` holding one numeric bar it has to beat.
The benchmark is frozen from that point. Every later iteration changes one lever
and is attacked by refuter agents whose job is to falsify the claim.

**The bar is the agent's own.** Nobody outside the run picks the target or the
number. That matters for everything below.

The two catalogs are unrelated: one is a curated list of self-evolving agent
techniques, the other a different list on agent evolution. Mission 1 ran 50
iterations capped at 40 minutes each on 23 June. Mission 2 ran 40 iterations
capped at 60 minutes on 24 June. Same runner, same model, same honesty floor.
The planned difference is one file: a cautious values document against one
written from Nietzsche.

"Integrity pass" means six mechanical checks an auditor can re-run: frozen
graders byte-identical from iteration 1 to the final commit, an append-only
artifacts directory, an unedited instructions file, a single-root git history,
no network at evaluation time, and new benchmarks added rather than modified.
All four runs passed at run time. The per-run `.git` directories were deleted on
archival, so those are run-time observations I cannot re-run today.

### Mission 1

The cautious run picked a genetic search over prompts, built an offline stand-in
for the expensive scoring oracle, measured a baseline of 0.728217, and set its
bar at 0.745. It cleared that at **iteration 5**, with 0.74932 on held-out
seeds, wins on 9 of 10, and a margin of 5.2 standard errors. Its own capstone
calls that "the one frozen-bar pass": it never cleared the bar again, and did
not need to. It spent the remaining 45 iterations finding where the algorithm
breaks, ending on a budget-allocation law, a class of problems where sixteen
times more compute bought nothing, and one algorithm that crossed that wall.

The expansive run picked an LLM-driven program search applied to online bin
packing, and did something at iteration 1 that I keep coming back to. It had two
candidate baselines: a naive evolutionary algorithm at 0.0659 held-out, and
random search at 0.0641, where lower is better. It froze the **better** one as
its bar, writing the reason into its own criterion file: "Freezing the EA's
0.0659 as the bar would be a strawman." It chose the harder number deliberately,
before knowing whether it could reach it.

It never reached it. Eight outer-loop levers were tried and refuted on the
frozen bench. At iteration 13 one appeared to clear the gate; at iteration 14 a
pre-registered re-test killed it as optional stopping and the run retracted its
own win. At iteration 39 it ran the rival method's published code on its own
benchmark and found the reason: that method loses at the problem size the
mission was scored on and matches its published result at thirty times that
size. At iteration 41 it froze a new benchmark above the crossover, where the
same machinery won by a wide margin. Every artifact after that says this does
not move the frozen mission gate, still not met.

### Mission 2

Different catalog, same shape.

The cautious run picked an archive-based search method on a standard
ten-dimensional test function, measured a baseline of 1841.00, and set its bar
at baseline plus ten percent, or 2025.10, with a coverage requirement and a
held-out number attached. It cleared that at **iteration 4** with 2040.66. Then
it computed a closed-form ceiling for its own metric, 2318.36, and spent 36
iterations climbing towards it, ending at 2138.36 held-out, 92.2% of the
ceiling. Two further axes it closed by proving they could not be crossed.

The expansive run picked an archive controller from a different codebase and
replaced the LLM inside it with a deterministic oracle, so that any change could
be attributed to the controller rather than to model noise. Baseline 0.867839,
bar 0.8978. Its best controller reached 0.894753. Short by 0.003, and it never
closed that gap. It built thirteen frozen benchmarks instead, and its last real
experiment retracted its own headline law as coarse rather than fine.

## What I wrote down, three times

**24 June: replicated.** The deck slide is headed "The persona contrast —
replicated", and to its credit it hedges itself in the subtitle:
"Replication-strength claim needs same-template replicates, but n=1 per cell on
two missions is more than n=1 on one." A run write-up from the same day reads
the split as structural: the "values as architecture" thesis holds "in the
dimension of how rigor and self-overcoming are expressed". Neither document has
been revised since. The deck's only later commits moved its folder.

**15 July: no fingerprint but the words.** Three weeks later I audited nine runs
at once, adversarially, seven reviewers each handed one claim and told to break
it rather than confirm it. That audit put a retraction banner on the 24 June
write-up: the split there is confounded with the two runs picking different
mission targets, and across all nine runs "the philosophy was paint, not
structure".

The part that lands hardest is not the general verdict. It is that the audit
singles out **mission 2 as the cleanest comparison in the whole set**, on the
grounds that both runs were single-domain, ran an equal 40 iterations, and held
the same one-knob discipline. And on that pair it finds near-identical work:
"When the philosophy had a fair fight, it left no fingerprint but the words."
The one gap it does report runs backwards, with the plain run editing its own
values file once and the self-overcoming one never touching it.

**24 July: neither of you, and I am not picking.** On 24 July I ran an
independent re-verification and stapled a correction to both archived documents.
On the 24 June write-up it confirms the headline science numbers verbatim
against the run's own report source, restates that the values-as-architecture
reading is confounded with target choice, and ends "Correctly kept archived." On
the audit it confirms the verifiable core, the vocabulary tag counts and the
bench and iteration counts and the debunking of an invented boldness score, and
then says of the audit's own headline: "over-generalized; do not rely on it."

So the most recent document says both earlier readings over-claimed, and it does
not say which is closer to right. That is the honest state of it.

Two details in that correction matter for mission 2 specifically. The first cuts
against the audit. Its evidence for the pair being near-identical-but-backwards
was that the plain run "wrote 4 formal proposals to change its rulebook"; the
correction reclassifies those as proposals about the immutable constitution
file, routed to a human rather than applied, which is evidence the floor held.
That one I can still check: `artifacts/CONSTITUTION_PROPOSALS.md` is on disk in
that workspace and opens by saying exactly that. The second cuts the other way
but lands on mission 1, not mission 2: the correction points out that the audit
called the mission-1 pair "no behavioral difference" when its sibling document
measured 0 stray root scripts against 39.

There is also a tension inside the audit that nobody flagged. Its own claim
table grades "the agent-evolution pair was near-indistinguishable", which is
mission 2 under its internal name, as **PARTIAL** at medium confidence, the
weakest grade of anything it kept. The section that calls that pair "the tell"
is leaning on the claim its own bookkeeping trusts least.

And my filing is itself a verdict I should own. Both mission-mode documents sit
in an archive folder. On the same day the corrections landed I promoted the
earlier sixty-iteration study out of the archive. My own directory layout says
the cross-mission replication is the weaker evidence.

## What actually survives

Here is everything about these four runs I can still count today, without the
commit histories.

{% include figure.html
   src="/img/blog/2026-07-02-same-two-agents/what-replicated.webp"
   alt="Five small bar charts, one per measured quantity, each with four bars:
        mission 1 cautious and expansive, mission 2 cautious and expansive. The
        cautious run cleared its bar at iteration 5 and 4; neither expansive
        run cleared its bar on either mission. Frozen benchmarks 1 against 10
        on mission 1 and 6 against 13 on mission 2. Modules hoisted into tools:
        1 against 1, then 0 against 2. TASKS_DONE lines 869 against 852, then
        2,481 against 3,055. Loose Python files at the workspace root 0 against
        39, then 0 against 0."
   caption="The two panels marked same on both missions are the whole surviving
            claim. The per-run .git was deleted on archival, so anything
            needing the commit history, including the byte-identical grader
            check, is a run-time observation I cannot repeat."
%}

Two things came out the same way on both missions. The cautious run cleared its
own bar early and the expansive run never cleared its own bar at all. And the
expansive run left more frozen benchmarks behind, 10 against 1 and then 13
against 6.

Three things did not. Hoisted shared modules were 1 against 1 on mission 1 and
then 0 against 2 on mission 2. Loose scripts at the workspace root were 0
against 39 on mission 1, the single biggest measured difference anywhere in this
experiment, and then 0 against 0 on mission 2, and I know why. Three hours
before mission 2 started I committed a change to the runner restoring a
workspace-layout sweep at the review checkpoint, precisely because of that 39.
The gap I would most like to call character is the one I closed myself, with a
commit, between the two missions.

The third is a number I got wrong here. I previously reported log length on
mission 2 as 1,487 lines against 3,055. That is not like for like. The mission-2
cautious run is the only one of the four that archived old entries, moving its
first fifteen iterations into `TASKS_DONE_archive/`, another 994 lines. Counted
properly it is 2,481 against 3,055, or 270 KB against 308 KB. My own deck names
the archive in the same bullet as the 1,487, and I quoted the number without the
caveat that was sitting next to it. On mission 1 the two logs are 869 lines and
852, which is a tie.

The one part of the surviving shape I still find strange is the bar. A
disposition that reliably produces a run which fails to clear its own bar is a
stranger result than one that reliably clears it. Both expansive runs missed a
number they had picked freely and could have set lower, and neither lowered it
afterwards, which is the failure I built the frozen-grader machinery to catch.
Both spent the back half of the run characterising the miss, and both produced
their sharpest work there.

## What I cannot settle

**The confound is the whole problem and it does not go away.** The two agents
inside a mission were never working on the same problem. Each picked its own
target and wrote its own bar, so "cleared the bar" compares two different tests
sat by two different students. Part of what I am calling character is the choice
of target itself.

That confound eats into the second surviving item too. The audit reads a run's
extra benchmark directories as harder rungs of the one problem it happened to
pick, not as a wider reach, which is close to saying that the benchmark count is
a property of the target rather than of the values. I do not think that fully
explains 13 against 6 and 10 against 1, but I cannot show it does not.

I also cannot rescue the audit's verdict wholesale. It is right that mission 2
is the cleanest of the four pairs and right that the residue is thin. But one of
its two data points on that pair was reclassified three weeks ago, its own table
grades the claim PARTIAL, and its headline is flagged as over-generalised. The
document that disagrees with my replication is not itself in good enough shape
to replace it.

So: one run per cell, two missions, a target-choice confound, and three
documents of mine that do not agree. The 24 July correction is the most recent
and it verifies numbers rather than adjudicating readings. It does not restore
the replication and it does not endorse the audit.

What would settle it is not subtle, and my own audit's closing paragraph spells
it out: replicate with more than one run per cell, hold iterations and
configuration equal, and fix the starting target so that target choice cannot
masquerade as character. I have not run that for this pair. When I did run a
properly powered version of a related question, [the effect I liked went
away](/blog/powered-replication/), and on a third task altogether [taking my own
tally apart pair by pair](/blog/bin-packing-values/) left no reliable direction
at all. Neither of those is this experiment. I have not settled this one.

## What I checked

My write-up of the earlier sixty-iteration pair reported "60 of 60 completed"
when it meant the highest iteration number reached, so I re-checked these four,
and "completed" is doing more work than it should here as well.

No iteration in any of the four runs was killed by its own time cap: the runner
log records `killed=False` on every line. But only mission 2's expansive run
went start to finish in one session with a clean exit on all 40 iterations. Both
mission-1 runs were resumed repeatedly through a stretch of API outages, and
every iteration from 29 onward in the cautious run and from 19 onward in the
expansive one recorded at least one failed attempt before a clean one. Mission
1's expansive run has a single iteration, 25, that never recorded a clean exit
at all, which my own correction pass had already caught. Mission 2's cautious
run lost iterations 25 and 26 to repeated overload errors after about sixteen
minutes of work each, and neither was retried. I have not found that recorded
anywhere before now, and my deck says both mission-2 runs completed 40 of 40.

The count that produced an artifact is lower than the iteration count: 47 and 45
of 50, 32 and 33 of 40. Twenty of those twenty-three missing artifacts fall on a
scheduled review checkpoint, which is defined not to run a new experiment, and
the checkpoint schedule slipped by one on mission 1's expansive run after a
resume, which that run documented itself. Of the remaining three, one is
iteration 26 of mission 2's cautious run, the experiment the outage took.

Three places my slide deck and the workspaces disagree. The deck gives mission 1
commit counts of 85 and 88; the write-up from the day gives 88 and 88; neither
is checkable, because the per-run git directories were deleted on archival,
which also makes "byte-identical graders" a run-time observation I can no longer
re-verify. The deck describes the mission-2 cautious run's benchmark using the
other run's benchmark, a copy-paste, though the baseline number attached to it
is right. And 92.2% is the held-out figure: the scored number is 93.5% of the
same ceiling, and one slide attaches 92.2% to it.

None of those move the shape. I would rather say them than have someone else
find them.
