---
layout: post
title: >-
  Notes from well-connected pages scored higher in a Caesar comparison
date: 2026-04-14
description: >-
  Notes from well-connected pages received higher ratings, without showing
  that context from nearby pages caused the advantage.
image: /img/blog/2026-04-14-hub-vs-leaf/hub-vs-leaf.webp
tags: [agents, knowledge-graphs, caesar]
---

[Caesar](https://jasonzliang.github.io/caesar-agent/) keeps a graph of its web
exploration: pages are nodes and followed links become edges. Its note-taking
prompt includes insights from nearby pages, allowing each source to be read in
the context of earlier material.

An exploratory comparison found that notes from well-connected pages scored
[**24.43 out of 30**, compared with **21.88**](https://arxiv.org/html/2604.20855v3#A7.SS2.p5) for notes from pages with one
neighbour. The comparison suggests graph position may help select useful
material, but it does not isolate a benefit from the graph context itself.

## Selecting hub and leaf notes

The [tested prompt](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/caesar_agent.py#L371-L444) draws on pages up to three hops away, with at most 24
neighbour entries. A separate traversal-history block supplies up to eight
previous pages regardless of graph position. Even a leaf can inherit context
through the page that led to it: that edge exists before its notes are written.

Five completed explorations, one per research challenge, supplied two groups
apiece. Hubs were the ten most-connected pages visited more than once. They had
5 to 36 neighbours and 3 to 45 visits. Leaves were the ten least-connected
pages visited exactly once; each had one neighbour.

Each group's ten notes were [concatenated into a file](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/analysis/transfer_configs.py#L267-L320), producing five hub files
and five leaf files. These contained roughly 5,000–5,800 words each; the leaf
file was longer in three challenges. **The evaluated artifacts were raw notes,
not research answers generated from those notes.** There was no further writing
step.

Three [LLM judges](/blog/judge-bias/) scored every file five times on New,
Useful and Surprising, each from 1 to 10. That yields 75 scorings per group,
but only five distinct files per group.

| Dimension | Hub notes | Leaf notes |
|---|---:|---:|
| New | 8.35 | 7.32 |
| Useful | 7.80 | 7.21 |
| Surprising | 8.28 | 7.35 |
| **Total** | **24.43** | **21.88** |

Hub notes led on pooled scores for all three dimensions and on total scores in
all five challenges. Usefulness had two exceptions: leaves led 7.87 to 7.67 on
open-ended synthesis and tied hubs at 7.67 on cross-domain synthesis.

{% include figure.html
   src="/img/blog/2026-04-14-hub-vs-leaf/hub-vs-leaf.webp"
   alt="Hub and leaf note scores on New, Useful and Surprising. Hub means are
        higher on all three dimensions; 10th-to-90th-percentile ranges overlap
        throughout. Totals are 24.43 and 21.88 out of 30."
   caption="Means over 75 scorings per group: three judges, five trials and
            five files. The judges could see the hub and leaf condition labels."
%}

## Effect sizes depend on the unit

At the challenge level, hub means were 25.07, 23.93, 25.07, 24.40 and 23.67;
leaf means were 20.87, 21.33, 22.27, 21.47 and 23.47. The lowest hub mean exceeds
the highest leaf mean, yielding **Cliff's delta = 1.00** under the
[paper's](https://arxiv.org/html/2604.20855v3#A2.SS5) challenge-mean convention.

At the individual-scoring level, the distributions overlap substantially. Of
all hub–leaf score pairings, about 73% favour hubs, 19% favour leaves and 8%
tie, yielding **delta = 0.54**
([reported values and plotting code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-04-14-hub-vs-leaf/make_figs.py#L13-L51)). Hub totals range from 18 to 29; leaf totals from
15 to 28. As in the [human-evaluation discussion](/blog/human-vs-machine/), a
delta computed over means does not describe every individual score.

The margin also varies by task. Four challenges show leads of 2.6–4.2 points;
open-ended synthesis differs by only **0.20 points**. The analysis script's
[Mann–Whitney U test](https://en.wikipedia.org/wiki/Mann-Whitney_U_test) reports
p = 8.3 × 10⁻⁹ over individual scorings, but repeated judgments of the same
texts do not provide 150 independent text samples.

A second set of explorations used the older one-hop prompt without traversal
history and differed in other configuration settings. Two judging passes gave
23.29 versus 21.76, then 23.49 versus 22.17, using 45 and 75 scorings per group,
respectively. Both favoured hubs overall, but leaves won counterfactual reasoning.
Challenge-level deltas were 0.92 and 0.52; individual-scoring deltas were 0.33
and 0.30. The direction recurred, while the five-for-five result did not.
Configuration differences prevent treating this as a controlled prompt ablation.
The additional replication results use unpublished run records.

## Four unresolved confounders

**Visible labels.** Both files [appeared in the same prompt](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/analysis/llm_as_judge.py#L138-L145) under names including
`answer_cat_hubs.txt` and `answer_cat_leaves.txt`. Judges could infer the
condition and bring expectations about connectivity to the comparison. No
blinded rerun is available; label effects cannot be ruled out as an explanation
for the full gap.

**Unreadable sources.** Sixteen of the 50 leaf entries concern bot checks,
redirects or access gates, compared with one of the 50 hub entries. Nine occur
on constrained synthesis, the challenge with the largest gap, and six on
counterfactual reasoning. Across the other three challenges, which contain only
one such leaf entry, the mean gap is 1.98 rather than 2.55 points. The selection
rule encourages this imbalance: blocked pages offer few links and little reason
to return.

**Unequal revision.** Hubs were revisited; leaves were not. Caesar rewrites
notes on a return visit with previous notes in context. Additional processing,
in one case across 45 visits, is inseparable from position in this design.

**Different source quality.** Surveys and canonical references may attract more
connections and contain better material. The comparison cannot distinguish a
useful location in the graph from a useful source.

Connectivity remains a potentially inexpensive selection signal when an agent
has more notes than a synthesis prompt can hold. Testing whether it adds value
requires a controlled comparison of the same pages with and without neighbour
context, matched access and revision opportunities, and blinded scoring. The
current result is an association between the selected note groups under the
reported judging conditions.

Source: [Caesar paper, revised version](https://arxiv.org/abs/2604.20855v3).
