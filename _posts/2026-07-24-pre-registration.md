---
layout: post
title: "I froze my analysis, and it said I was underpowered"
date: 2026-07-24
description: >-
  Medicine and psychology freeze their analysis before seeing the data. Almost
  nobody does this in AI. Here is what it looks like when the experimental unit
  is an agent run.
image: /img/blog/2026-07-24-pre-registration/verdict-gate.webp
tags: [methodology, self-improving-agents, evaluation]
---

Before I re-scored a single run of my last experiment, I wrote down which one
number I was going to read, how it would be computed, and what I was not allowed
to conclude from it. Then I committed that document to git, and the analysis
choices in it never changed.

The experiment was four agent runs improving an online bin-packing heuristic, a
program that drops arriving items into bins one at a time with no lookahead. One
run got a control values document and one got a [Nietzsche-derived
one](/blog/nietzsche/), at each of two versions of those documents. The runs
themselves were already finished and frozen. What was still ahead of me was
scoring their programs on a held-out benchmark I had just rebuilt, and that
scoring step is what the document locked down.

This is pre-registration. Clinical trials have done it for decades. Psychology
took it up after its replication crisis. In machine learning it barely exists
outside the occasional workshop, and I think that is a mistake we are going to
keep paying for.

## The failure it prevents

The failure has a name: HARKing, Hypothesizing After the Results are Known.

It does not require dishonesty. Here is the version that gets everybody. You run
an experiment with a primary metric. The primary metric comes out flat. But
while looking at the results you notice a secondary measurement that separates
the conditions cleanly, and it has a plausible story. So you write that up.

Nothing in that sequence feels like cheating. Each step is a reasonable response
to what you are looking at. But if you had twelve measurements available and
picked the one that separated, you have not run one experiment, you have run
twelve and reported the winner, without the multiple-comparison correction that
would require. Both pre-registrations below apply one, Holm's, to their
secondary measurements as a family.

The document I froze blocks the specific version of this I was most at risk of.
It fixes the comparison as two-sided, predicting no direction at all, and says
why: I had already seen the runs' scores on the set the agent optimizes against,
and a pilot on the offline version of the same task had put the two conditions
in the opposite order from those scores. Predicting a direction then would have
been choosing my hypothesis to fit data I had already peeked at.

I had already seen enough of the data to have a hunch. Writing down that I was
not allowed to use it is the whole point.

## What has to be in it

Three documents, and the split between them is the honest part of this story.

The one I froze is `PREREGISTRATION.md`, committed seven minutes before the
commit that re-scored the runs. It is deliberately modest: it calls itself a
"descriptive case study" and sets **no accept/reject threshold at all**, because
at one run per condition there was nothing a threshold could legitimately
decide. The machinery for actually *testing* a hypothesis lives in
`PREREGISTRATION_POWERED.md`, written the next day for a powered follow-up, and
that one is still marked draft. The verdict gate in the next section is in
neither: it comes from a third document, a standing analysis playbook that says
how any two runs in this project get compared.

Between them the two pre-registrations pin down five things. I have marked which
one each comes from, because three of the five are not in the frozen document,
and a post that let you assume otherwise would be doing the thing this post is
against.

**The primary endpoint** (frozen and draft). Exactly one number: how the evolved
program packs items whose sizes are drawn uniformly, when every item it trained
on came from a Weibull distribution. That is the distribution shift. The metric
is the mean excess over a lower bound on the optimal number of bins, and lower
is better.

**The unit of analysis** (frozen and draft). This one is specific to agent
research, and where I expect most people to get it wrong. My experimental unit
is **the run**, not the instance the run's program is scored on. The primary
held-out set is 50 packing instances, and a run that packs all 50 is one data
point, not 50, because the 50 are not independent: they were all packed by the
same evolved program from the same trajectory. Counting instances instead of
runs would have multiplied my sample size by fifty and made almost anything look
significant.

**The test** (draft only). A permutation test: take the runs' scores, throw away
which condition each came from, and re-deal the labels. Every way of splitting
the runs into two groups of equal size gives you one difference the experiment
could have produced by luck alone. The p-value is the fraction of those re-dealt
differences at least as large as the real one. This is nice: the re-dealt
distribution *is* your pipeline's noise floor, measured rather than assumed.

My implementation does not sample those re-deals, it enumerates them, which at
five runs per condition is 252 and not the ten thousand shuffles you usually
see; only above ten runs per condition does it fall back to a fixed-seed sample
of 200,000. Enumerating makes one limit visible that sampling hides. At three
runs per condition there are only 20 possible splits, so the smallest two-sided
p the design can produce is 0.1. A pilot that size cannot reach p below 0.05 no
matter what the data say.

**The smallest effect worth caring about** (draft only). Mine is one percentage
point of that excess metric, fixed in advance, revisable only before the pilot
and never after seeing the data. Without this you can declare any statistically
significant difference meaningful, however tiny.

**The decision rule** (draft only). The null hypothesis is that the values
document makes no difference at all. Reject it only if the permutation p is
below 0.05 **and** the difference exceeds that one-point threshold. Otherwise
report a null, with the minimum detectable effect stated alongside it: the
smallest difference this many runs could have caught. Set that against the
smallest effect worth caring about above, and if the first number is bigger than
the second, the experiment could never have answered the question. The frozen
document deliberately has no such rule.

## The verdict gate

The part I would most recommend stealing is in that third document. The
playbook's rule forces every result into one of four boxes, with no exits:

- **Inconclusive by saturation**: every condition is pinned at a ceiling or a
  floor, so nothing could have been detected.
- **Underpowered**: you cannot bound the effect at all.
- **Effect**: the difference has to survive being reported as an interval rather
  than a point, and it has to exceed the run-to-run noise.
- **Null**: allowed only if the conditions had room to move *and* you state the
  noise band.

{% include figure.html
   src="/img/blog/2026-07-24-pre-registration/verdict-gate.webp"
   alt="A flowchart. Could this benchmark have shown a difference at all? No:
        inconclusive by saturation. Can you bound the effect at this number of
        runs? No: underpowered. Does the difference clear the measured noise
        floor? Yes: Effect. No: Null."
   caption="Writing the gate down before scoring is what stops the last
            question from being the only one you ask."
%}

The saturation box is the one that earns its keep, and the figure asks it first.
If every condition scores 0.99 on a benchmark whose maximum is 1.0, you have not
found that your intervention does nothing. You have found that your benchmark
cannot see. Those are completely different conclusions and they get reported
identically all the time.

The rule that goes with it, in the playbook's own words: say "no detectable
difference at this N," never "values don't affect performance." Those sentences
describe different worlds.

## Underpowered

Applying that gate, the honest verdict on the experiment was **underpowered**.
One run per condition cannot separate a real effect from run-to-run variation,
so nothing causal could be claimed, and the frozen document said so in advance
rather than letting me discover a reason afterwards.

That is an unsatisfying outcome for four agent runs and about twenty hours of
agent time, spent in one overnight batch. It is also correct, and I know it is
correct rather than merely suspecting it, which is the entire return on writing
the document.

The follow-up is specified in that second document, honest about its own status
in a way worth preserving: it is headed "Draft for review," it says confirmatory
work "must not begin until this doc is frozen," and it declines to assert a
sample size, on the grounds that picking a number before the pilot would be
unprincipled. It is a plan for a power analysis, not a power analysis.

And when I later ran a powered version of the same question on a different task,
it reversed a headline I had believed, which is the best argument I have for
putting the machinery in place beforehand.

## Why this is not bureaucracy

The objection I expect is that AI moves too fast for this, and pre-registration
is ceremony imported from slower fields.

I would put it the other way around. The faster your iteration loop, the more
analyses you run, and the more chances you have to find a pattern that is not
there. A field that ships experiments weekly and never freezes an analysis is
not moving faster than medicine. It is accumulating unmeasured false-positive
rate at unprecedented speed.

The frozen document is 56 lines of markdown. Five later commits touched it, all
of them path updates or terminology sweeps, and not one changed an analysis
choice. You can check that from the git history rather than from my say-so,
which is the only thing that makes a freeze worth anything. The barrier here is
not cost.
