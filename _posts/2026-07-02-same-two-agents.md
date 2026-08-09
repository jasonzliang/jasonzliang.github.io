---
layout: post
title: "I called it a replication. Two of five measures held."
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
file](/blog/nietzsche/). They came out visibly different, and at one run per
condition there was no reliable winner. Then I ran the same one-file swap on two
unrelated mission catalogs, four runs, and the split came out the same shape
both times. On 24 June I put a slide in a deck headed "The persona contrast —
replicated".

I have since written about those four runs twice more. On 15 July I concluded
that on the mission where the comparison is cleanest the two agents are nearly
indistinguishable, the philosophy having "left no fingerprint but the words". On
24 July I told myself not to lean on either reading. All three rounds are mine,
and this post is what is left of them side by side: less than the first claimed,
a little more than the second allows.

## The four runs

These runs used the runner's focused mode: on iteration 1 the agent picks one
target from a curated list of research repositories, vendors it offline, and
builds its own benchmark, ending in a `CRITERION.md` holding one numeric bar it
has to beat. The benchmark is frozen from there; every later iteration changes
one lever and is attacked by refuter agents paid to falsify the claim. **The bar
is the agent's own**: nobody outside the run picks the target or the number,
which matters for everything below.

The two catalogs are unrelated lists of agent-evolution research. Mission 1 ran
50 iterations capped at 40 minutes each on 23 June; mission 2 ran 40 iterations
capped at 60 minutes on 24 June. Same model, same honesty floor, and nearly the
same runner: one change I made in between turns out to matter. The planned
difference is one file, a cautious values document against an expansive one
written from [Nietzsche](https://plato.stanford.edu/entries/nietzsche/). All
four cleared a six-check integrity pass at run time, including byte-identical
frozen graders and a single-root git history. The per-run `.git` directories
were [deleted on archival](/blog/resume-audit/), so those are run-time
observations I cannot re-run now.

The shape was the same both times. The cautious run cleared its own bar early,
at **iteration 5** on mission 1 and **iteration 4** on mission 2, then spent the
rest of the run mapping the limits of what it built, ending on mission 2 at
92.2% of a ceiling it derived for its held-out metric. The expansive run never
cleared its own bar at all: mission 1's froze the better of its two candidate
baselines as the target ("Freezing the EA's 0.0659 as the bar would be a
strawman") and never reached it, and mission 2's missed its bar by 0.003 and
built thirteen frozen benchmarks instead.

## What I wrote down, three times

**24 June: replicated.** The slide hedges in its subtitle: "Replication-strength
claim needs same-template replicates, but n=1 per cell on two missions is more
than n=1 on one." A write-up from the same day reads the split as structural;
neither has been rewritten since.

**15 July: no fingerprint but the words.** Three weeks later I audited nine runs
adversarially, seven reviewers each handed one claim and told to break it. That
audit put a retraction banner on the 24 June write-up: the split there is
confounded with the two runs picking different mission targets, and across all
nine runs "the philosophy was paint, not structure". It singles out **mission 2
as the cleanest comparison in the set**, both runs single-domain, equal at 40
iterations and held to the same one-lever discipline, and finds near-identical
work: "When the philosophy had a fair fight, it left no fingerprint but the
words." The one gap it reports runs backwards, the cautious run editing its own
values file once and the expansive one never touching it.

**24 July: both of you over-claimed.** Nine days later a separate
re-verification stapled a correction to both documents. On the 24 June write-up
it confirms the headline numbers verbatim against the run's own report, restates
that the values-as-architecture reading is confounded with target choice, and
ends "Correctly kept archived." On the audit it confirms the verifiable core,
the tag, benchmark and iteration counts and the debunking of an invented
boldness score, then says of the audit's own headline: "over-generalized; do not
rely on it."

The most recent document says both earlier readings over-claimed and does not
say which is closer to right. The audit's other evidence for that backwards gap
was that the cautious run "wrote 4 formal proposals to change its rulebook",
which the correction reclassifies as proposals about the immutable constitution
file, routed to a human rather than applied, and so evidence the floor held.

## What actually survives

{% include figure.html
   src="/img/blog/2026-07-02-same-two-agents/what-replicated.webp"
   alt="Five small bar charts with four rows each, mission 1 and mission 2 by
        cautious and expansive: cleared its own bar, frozen benchmarks, hoisted
        modules, TASKS_DONE lines, and loose Python files at the workspace
        root. Only the first two point the same way on both missions."
   caption="Those first two panels are the whole surviving claim. Anything
            needing the commit history, including the byte-identical grader
            check, is a run-time observation I cannot repeat."
%}

Two things came out the same way on both missions: which run cleared its own
bar, and the expansive run leaving more frozen benchmarks behind, 10 against 1
on mission 1 and 13 against 6 on mission 2. Neither expansive run lowered the
bar it missed, the failure the frozen-grader machinery exists to catch.

Three did not, cautious first. Hoisted shared modules were 1 against 1 on
mission 1 and 0 against 2 on mission 2. Loose scripts at the workspace root were
0 against 39 on mission 1, the biggest measured difference in the experiment,
and 0 against 0 on mission 2, because three hours before mission 2 started I
committed a runner change restoring a workspace-layout sweep at the review
checkpoint, precisely because of that 39. The gap I would most like to call
character is one I closed myself between the missions.

The third is a number I got wrong. I reported log length on mission 2 as 1,487
lines against 3,055, which is not like for like: the mission-2 cautious run is
the only one that archived old entries, moving its first fifteen iterations into
`TASKS_DONE_archive/`, another 994 lines. Counted properly it is 2,481 against
3,055. My own deck names that archive in the same bullet as the 1,487; I quoted
the number without the caveat next to it. On mission 1 the logs are 869 and 852,
a tie.

## What I cannot settle

**The confound is the whole problem.** The two agents inside a mission never
worked on the same problem: each picked its own target and wrote its own bar, so
"cleared the bar" compares two different tests sat by two different students,
and part of what I am calling character is the choice of target itself.

It eats into the benchmark count too: the audit reads a run's extra benchmark
directories as harder rungs of the problem it happened to pick rather than a
wider reach, which is close to saying the count belongs to the target and not to
the values. I do not think that fully explains 10 against 1 and 13 against 6,
but I cannot show it does not.

Nor can I rescue the audit's verdict wholesale. It is right that mission 2 is
the cleanest pair and the residue thin. But one of its two data points there was
reclassified nine days later, its own claim table grades that claim **PARTIAL**
at medium confidence, the weakest grade of anything it kept, and its headline is
flagged as over-generalised. The document that disagrees with my replication is
not in good enough shape to replace it. My filing is a verdict too: both of
these documents sit in an archive folder, and on the day the corrections landed
I promoted the sixty-iteration study out of it.

So: one run per cell, two missions, a target-choice confound, and three rounds
of my own writing that do not agree. The most recent verifies numbers rather
than adjudicating readings; it neither restores the replication nor endorses the
audit. What would settle it is more than one run per cell, iterations and
configuration held equal, and a fixed starting target so that target choice
cannot masquerade as character. I have not run that. When I ran a properly
powered version of a related question, the effect I liked went away, and on a
third task, taking my own tally apart pair by pair left no reliable direction at
all. Neither of those is this experiment; I have not settled this one.

## Where my records disagree

"Completed" is doing more work than it should here, as it was in my write-up of
the earlier pair, which reported "60 of 60 completed" when it meant the highest
iteration reached. No iteration in these four was killed by its own time cap,
but only mission 2's expansive run went start to finish in one session with a
clean exit on all 40 iterations: both mission-1 runs were resumed repeatedly
through API outages, and mission 2's cautious run lost iterations 25 and 26 to
overload errors and never retried them, which I have not found recorded before
now and which my deck contradicts by saying both mission-2 runs completed 40 of
40.

The deck disagrees with the record in three places: mission 1 commit counts of
85 and 88 against the write-up's 88 and 88, neither checkable now the per-run
git directories are gone; a copy-pasted benchmark description on one mission-2
slide; and 92.2%, the held-out figure, given on another slide as the scored
number, which is really 93.5% of the same ceiling. None of that moves the shape,
and I would rather say it than have someone else find it.
