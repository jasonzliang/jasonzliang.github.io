---
layout: post
title: "Notes from hub pages scored higher, and why I doubt it"
date: 2026-04-14
description: >-
  Notes the agent took at well-connected pages scored higher than notes it took
  at dead ends. A real result, and a narrower one than it first looked.
image: /img/blog/2026-04-14-hub-vs-leaf/hub-vs-leaf.webp
tags: [agents, knowledge-graphs, caesar]
---

Most retrieval systems treat the web as a bag. You issue a query, you get back a
list of documents, you feed the good ones to a model. The structure connecting
those documents, which page links to which, what sits next to what, is thrown
away before the writing starts.

[Caesar](https://jasonzliang.github.io/caesar-agent/), the research agent I work
on, does something different. As it explores, it builds a graph: pages are
nodes, and the links it chose to follow are edges. It then generates its notes
*conditioned on that local structure*, what a page says, read against what its
neighbours say.

That much is not an interpretation, it is code. The note-taking prompt carries a
block headed `RELATED INSIGHTS OF NEIGHBORING PAGES`, and every entry in it is
stamped with its hop distance from the page being read. "Neighbouring" is
generous: the block reaches three hops out and holds up to 24 entries, and it
sits beside a second block of up to eight pages from the traversal history that
every page gets regardless of where in the graph it sits. So a well-connected
page tends to fill the block and a dead end tends not to. But a dead end is not
writing blind. The link that led there is already in the graph before the notes
are written, so a leaf inherits whatever its one neighbour could see.

The obvious question is whether that does any work, or whether the graph is
decoration on top of ordinary retrieval.

## What was actually measured

Here is the procedure, stated plainly, because the details turn out to matter
more than the headline does.

Take five finished explorations, one for each of the five research challenges we
evaluate on. In each exploration's final graph, rank the pages by how many
neighbours they have, and pull two groups out of the ranking:

- **Hubs**: the ten most-connected pages the agent visited more than once.
  Across these five graphs they have between 5 and 36 neighbours, and were
  visited between 3 and 45 times.
- **Leaves**: the ten least-connected pages the agent visited exactly once.
  Every one of them has a single neighbour: reached, read, never returned to.

Concatenate the notes from each group into one file. That gives two files per
challenge, ten sets of notes apiece, each between about 5,000 and 5,800 words,
and the leaf file is the longer one on three of the five challenges, so neither
side wins by being longer. Then put both files in front of a panel of three LLM
judges, five trials each, scored on the rubric we use everywhere else: how new,
how useful, how surprising, one to ten on each, thirty in total.

One thing I need to be exact about, because it is not what the first version of
this post said. There is no second writing step. Nobody handed these notes to a
writer and asked for a finished answer. The artifact that gets scored is the raw
pile of notes, concatenated, and it opens with the literal string `Insights:`.
What was compared is two piles of notes, not two written answers. That is a
narrower thing to have measured, and the rest of the post is about how much of
the claim survives it.

## The result

| | Hub notes | Leaf notes |
|---|---|---|
| New | 8.35 | 7.32 |
| Useful | 7.80 | 7.21 |
| Surprising | 8.28 | 7.35 |
| **Total** | **24.43** | **21.88** |

Hub notes lead on all three dimensions in the pooled average, and they lead on
total score in all five challenges. That is the finding. Two of the fifteen
per-challenge dimensions fail to follow it: on the open-ended challenge leaf
notes lead on Useful, 7.87 to 7.67, and on cross-domain synthesis the two tie
there at 7.67.

{% include figure.html
   src="/img/blog/2026-04-14-hub-vs-leaf/hub-vs-leaf.webp"
   alt="Paired bars comparing notes harvested at hub pages against notes
        harvested at leaf pages. Hub notes score higher on New (8.35 vs 7.32),
        Useful (7.80 vs 7.21) and Surprising (8.28 vs 7.35), which sums to
        24.43 against 21.88 out of 30. Whiskers spanning the 10th to 90th
        percentile of the individual scorings overlap on all three dimensions."
   caption="The hub lead runs from 0.59 to 1.03 points per dimension on a
            one-to-ten scale, which is why the bars sit as close together as
            they do, and the whiskers are how far the individual scorings
            overlap. The panel doing the scoring could see which pile was
            which."
%}

## Which unit the effect size is measured at

The effect size we report is [Cliff's delta](/blog/human-vs-machine/), which
asks how often a draw from one group lands above a draw from the other, and this
is where I went wrong the first time, so it is worth slowing down.

The paper's unit is the challenge, five of them. Averaged within a challenge,
hub notes scored 25.07, 23.93, 25.07, 24.40 and 23.67. Leaf notes scored 20.87,
21.33, 22.27, 21.47 and 23.47. The lowest hub mean sits above the highest leaf
mean, which is exactly the condition the paper's Table 1 caption calls strict
dominance, and it is what makes **delta = 1.00**. It is a statement about five
numbers against five numbers.

Drop to the level of individual scorings, 75 a side, and the picture is much
coarser. Pick one hub scoring and one leaf scoring at random: the hub one is
higher 73% of the time, lower 19%, and tied the remaining 8%. Cliff's delta over
those pairings is **0.54**. Hub scores run from 18 to 29 out of 30, leaf scores
from 15 to 28. The two distributions overlap heavily.

Both numbers are true, at their own units. What the first version of this post
did was quote the 1.00 and then gloss it as if it were the second: pick any
hub-sourced item and any leaf-sourced item and the hub one wins, every time.
That is false. Close to one pairing in five goes the other way.

The margin is not uniform either. On four of the five challenges hub notes lead
by between 2.6 and 4.2 points. On the fifth, the open-ended one, the gap is
23.67 against 23.47, which is nothing. Strict dominance at n = 5 holds, and it
holds by two tenths of a point.

The analysis script also reports a Mann-Whitney U test on the 150 rows, p =
8.3e-09. I would not lean on it. It treats 75 scorings a side as 75 independent
samples, and they are not: they are three judges scoring five texts, five times
each.

The same comparison was also run over a second set of explorations, and this is
the part I should have led with, because it is the only replication I have.
Those explorations used the older note-taking prompt: one hop of neighbours, no
traversal history. Several other config knobs differ too, so it is not a clean
ablation, but that is the difference the run was set up to isolate. It was
judged twice. The first pass, three judges by three trials, gave 23.29 against
21.76 over 45 scorings a side. The second, run minutes before the main one on
the identical three-by-five design, gave 23.49 against 22.17 over 75.

Both point the same way. Both point less emphatically. And in both of them one
of the five challenges reverses, counterfactual reasoning, where the leaf pile
wins. So the strict dominance that produces delta = 1.00 does not replicate: the
challenge-level delta is 0.92 on the first pass and 0.52 on the second, against
1.00 here, and the scoring-level delta is 0.33 and 0.30 against 0.54. The
consistency across all five challenges is the whole basis for the 1.00, and it
is the part that fails to hold up when I run it again.

## Four reasons to discount this

**The scoring was not blind.** This is the one that bothers me. The judging
harness assembles its prompt by pasting each answer under a header that contains
the filename, the two files are called `answer_cat_hubs.txt` and
`answer_cat_leaves.txt`, and both go into the same prompt. So the judges saw the
two piles side by side and were told by name which was which. "Hubs" and
"leaves" are not neutral words, and a judge that has any prior about graph
structure has been handed the answer. I cannot rule out that the labels account
for the entire gap, and I have not re-run the panel with the files renamed.
Everywhere this post says hub notes scored higher, read it as scored higher
under a panel that could see the condition labels.

**A third of the leaf notes are about pages the agent never got to read.** I
eventually went and read the two piles instead of the score tables. Sixteen of
the fifty leaf entries are the model writing about a bot check: a Cloudflare
interstitial, a redirect, an access gate. One calls the page "a barricade, not
information." Another observes that "the artifact here is *absence*." One of the
fifty hub entries is like this. They are not spread evenly, either. On the
constrained challenge nine of ten leaf notes are about pages that would not
load, and that is the challenge with the largest gap, 4.20 points. On
counterfactual reasoning it is six of ten. On the other three challenges it is
none, and across those three the gap is 1.98 points rather than 2.55. Worse, the
selection rule causes this: a page that answers with a bot check offers no links
worth following and no reason to come back, so it settles in the graph with one
neighbour and one visit, which is exactly the definition of a leaf here. Some
unknown share of this result is readable pages beating unreadable ones.

**Hubs were revisited and leaves were not.** The selection rule asks for a visit
count above one on the hub side and exactly one on the leaf side. Caesar
rewrites a page's notes every time it returns, with the previous notes in
context, so the hub pile has been through more passes of revision, in one case
45 of them. Graph position and amount of processing are confounded by
construction. Some of what I want to attribute to position is probably just
rework.

**Hubs may simply be better pages.** The deflationary reading is that
well-connected pages tend to be surveys, overviews and canonical references, and
of course notes from a good survey beat notes from a dead end. If that is the
whole story the finding reduces to "read better sources," which nobody needs a
graph to discover. Separating "hubs are better pages" from "hubs are better
vantage points" needs a design this study does not have: the same page, read
once with neighbour context and once without. I have not run it.

## What is left

Stated at the width the evidence supports: notes harvested at well-connected
pages scored higher than notes harvested at dead ends, 24.43 against 21.88 on a
30-point rubric, on all three dimensions pooled and on total score in all five
challenges, under a non-blind LLM panel, on a leaf sample where a third of the
notes were taken on pages that would not load, and with the five-for-five part
failing to reproduce on the one other set of explorations I tried it on.

That is a smaller claim than the one I started with, and it is still worth
having. The agent gathers far more material than fits into a synthesis prompt,
so something has to choose what goes in. The default is recency or retrieval
score. This says graph position is a usable selection signal, and a cheap one,
because you already have the graph. That much survives the confounds, since even
on the most deflationary reading, where connectivity is mostly a proxy for the
page having loaded and been worth returning to, it is still a proxy you get for
nothing.

The mechanism I would like to be true, that a hub is a better *vantage point*
rather than a better *page*, remains a hypothesis. The prompt-level machinery
for it is real and you can read it in the source. Whether it is what produced
these numbers, this experiment cannot say, and neither can I until someone runs
the ablation: the same page read once with neighbour context and once without,
everything else held fixed.

The generalizable part is smaller than I wanted it to be, and I think it still
holds. If you are building anything that crawls and then writes, you are almost
certainly discarding the structure of the crawl, and that structure is free,
already sitting in your logs. On this task it carried enough signal to be worth
selecting on. Whether it carries more than "surveys are good pages," or more
than "that one came back a 403," is an open question, and I would rather leave
it open than close it with the experiment I have.
