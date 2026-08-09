---
layout: post
title: "The agent that audited its own résumé"
date: 2026-06-18
description: >-
  An AI agent kept a log of which earlier work it had built on. Then it checked
  those claims against git. Of the first eight, two held up, three were refuted,
  and three the check could not settle.
image: >-
  /img/blog/2026-06-18-resume-audit/claimed-vs-verified.webp
tags: [self-improving-agents, evaluation, ai-honesty]
---

Here is a setup that turns out to be unusually revealing.

I built a loop that runs an AI coding agent over and over. Each iteration is a
completely fresh session, no memory of any previous one. Everything the agent
knows about its own past has to come off the disk: the files it wrote, and the
git history. Anything it does not commit before the iteration ends is destroyed.

Because there is no memory, the agent keeps a logbook. Every iteration it writes
down what it did, plus two fields: `builds-on`, which earlier iterations this
one stood on top of, and `code-reuse`, which earlier files it reused. The run
reached iteration 60, but 60 was the configured ceiling rather than a count of
finished work: 55 of those iterations left an artifact behind. (My own write-up
of the run carries a correction note saying 56. That is its commit count, which
is a different thing; the workspace has 55 artifact directories.) Across those,
the two fields become a graph of the run's own intellectual history: this idea
led to that tool, which enabled this result. The agent's own tooling calls it a
DAG, a directed acyclic graph, meaning the arrows all run one way, from earlier
work to later, and no chain of them ever loops back to where it started.

At iteration 3, the agent wrote a program to draw that graph.

At iteration 6, it wrote a different program to check whether the graph was
true.

## Two out of eight

The checker compared each claimed "I built on X" link against git: the one
record the logbook cannot edit. The result, from the agent's own report:

```
ADVERSARIAL DAG — 8 claimed edge(s) checked against git:
  2 ok · 3 unsupported · 3 PHANTOM · 0 unverifiable
```

Of eight claims about its own history, two held up.

{% include figure.html
   src="/img/blog/2026-06-18-resume-audit/claimed-vs-verified.webp"
   alt="A bar of eight claimed influences above a stacked bar splitting the
        same eight by what git said at iteration 6: 2 verified, meaning git
        confirms it, 3 unsupported, meaning git cannot confirm it, and 3
        phantom, meaning git contradicts it."
   caption="The audit's three verdicts, at iteration 6 of a 60-iteration run.
            Phantom does not mean the work never happened: it means git
            contradicts the claim, as when the agent credited a file it had
            created in the very commit it said it was reusing from."
%}

The three phantoms are the good part. Two were cases where the agent claimed to
have *reused* a file that it had in fact *created* in that same commit, taking
credit for standing on a shoulder that was its own. The third is stranger:
iteration 2 claimed to have reused iteration 4. An edge pointing backwards in
time.

The cause was mundane and, I suspect, extremely common, and it was not confined
to the phantoms. The graph was built by scraping both fields for anything shaped
like a filename or a task ID and turning every mention into an arrow. Iteration
2's `code-reuse` field said `none` and then mentioned a task it had *queued for
later*, which is where the backwards arrow came from. Iteration 5's field read
*"none — reimplemented because the dynamics.py kernel is 1-D-map-specific"* and
produced a confident arrow to `dynamics.py`. The regex saw a mention and
recorded a fact.

The agent's own summary, promoted into the standing lessons at the top of its
logbook, was that the graph "inflates ~4×." That figure is this snapshot: eight
claims, two confirmed.

## The category it refused to collapse

The result I find most interesting is not the phantoms. It is the three
"unsupported" links, and the agent's insistence on keeping them separate.

Two of the three were real intellectual descent. Iteration 4, for instance,
genuinely built on iteration 2, by copying and adapting its kernel rather than
importing it, and git cannot see that. It is not a false claim; it is a true
claim that this particular instrument cannot confirm. The third was the
`dynamics.py` arrow above, invented by the regex out of a field that said
`none`, and git could not refute that one either, because `dynamics.py` really
did already exist. So the middle bucket is holding two unlike things: a real
lineage the instrument cannot see, and a fabricated one it cannot rule out.
"Unsupported" is the right verdict for both, which is the point. It is the
bucket for claims the evidence does not reach.

From the agent's write-up: **"'Unsupported' is not 'false.'"** And: "The single
bucket 'an edge' hid three different things."

It would have been easy, and it would have made a cleaner headline, to report "6
of 8 claims failed." The agent declined to do that. Given a binary verdict space
it did not fit into, it added a third category rather than round to the answer
that made its finding look bigger.

The lesson it wrote in its own log is better than my summary:

> a claim can never count as its own evidence (a `dynamics.py` in a docstring is
> not an `import dynamics`).

## Neither number is a measurement

I ran a second agent through the identical harness at the same time, same rules,
same task, same everything, differing only in a short values document. That run
built an integrity checker of its own at iteration 3, but it only lints the
logbook's schema and runs the tool self-tests. Nothing in it ever put a lineage
claim in front of git.

These are the same two June runs I write about from the other side in why I gave
an AI agent Nietzsche. The one that built the auditor is the Nietzschean agent;
the sibling here is the standard-values one. That post is about what the two
values files say and how differently the agents behaved because of them. This
one is about what happened when one of the two checked its own record.

That second run reached iteration 60 too, left artifacts in 57 of its
iterations, and closed by reporting **56** build-on edges, presented as the
picture of how much its work compounded. (That 56 is a coincidence; the 56
earlier in this post is the other run's commit count.)

The tempting move is to say those 56 are inflated the same way. They are not.
That run's parser matched `iterNN` tokens in the `builds-on` field only, rather
than scraping filenames and task IDs out of two fields, and its own README
already called 56 a lower bound, since an iteration that reused an earlier one
without naming it contributes no edge. I re-ran that parse against the archived
log: all 56 edges run from an earlier iteration to a later one, and none of them
come from a field that says `none`. The specific failure modes that produced the
phantoms are absent here.

What is absent is the other half. Nothing ever asked whether an iteration that
named a parent actually used the parent's code, and nothing can now: the
archived workspaces were stripped of their `.git` directories, so the record the
audit depends on is gone.

I want to be clear that this is my error, not the agent's. Back on the first
run, the audit tool existed. That agent even promoted an instruction to run it
into the standing lessons at the top of its own logbook, where every fresh
iteration would read it before starting. No later entry records running it, the
follow-up task to wire it into the graph renderer was still sitting unchecked in
the to-do list when the run ended, and the checks an iteration had to pass
before committing never included it.

The one time the tool was pointed at the finished log, by my own audit pass
rather than by the run, it counted **133** claimed edges, almost all of them
claims to have reused a particular file rather than to have built on a
particular iteration, and flagged 31 as phantom and 37 as unsupported. That
leaves 65 it did not flag. So 2 of 8 is a snapshot of iteration 6 and not a
verdict on the run: by the end, roughly half the claims were standing. Those
verdicts are the thing I can no longer reproduce. Rerun the checker on the
archived workspace today and it still finds the same 133 claims, but returns 132
of them unverifiable, because the git it needs is gone.

So I do not know how much either run compounded. One number is a self-report
with a known parse rule and a stated lower-bound caveat. The other is an audited
number I can no longer re-derive. Neither is a measurement.

## An error of unknown sign

The generalization I would have reached for is that a system's self-computed
metrics flatter it. That is not what these two runs show. One over-counted its
lineage by turning mentions into facts. The other under-counted it, by its own
admission, because an iteration that reuses earlier work without naming it
leaves nothing for the parser to find. The uncomfortable version is milder and
worse: **a number a system computes from its own description of itself has an
error of unknown sign**, not through anything as deliberate as lying, but
because the measurement and the thing measured share an author.

The fix is not more careful prose. It is to adjudicate claims against a record
the system cannot rewrite, to do it *every time* rather than once, and to keep
that record afterwards. I had the first part right and the other two wrong.
