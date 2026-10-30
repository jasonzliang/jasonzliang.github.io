---
layout: post
title: >-
  An AI agent audited its own logbook: two of eight links were confirmed
published: false
date: 2026-06-18
description: >-
  An agent's self-audit exposed how a logbook can overstate code reuse, and
  why unverified claims are different from false ones.
image: >-
  /img/blog/2026-06-18-resume-audit/claimed-vs-verified.webp
tags: [self-improving-agents, evaluation, ai-honesty]
---

A coding agent's logbook can overstate how much new work builds on earlier work.
In one exploratory run, an agent built a graph of its earlier work, then built
a checker that challenged the graph. At iteration
6, only two of eight claimed links were confirmed against git history.

The audit exposed a parser error. Some claims conflicted with the record;
others exceeded what the checker could establish.

## A graph built from prose

The harness restarted the coding agent in a fresh session every iteration.
Continuity came from files and git history; uncommitted work was discarded.
Each logbook entry included `builds-on`, naming earlier iterations, and
`code-reuse`, naming earlier code. At iteration 3, the agent wrote a tool to
turn those fields into a lineage graph, described as a
[directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph).

The run eventually reached the configured ceiling of iteration 60, leaving
55 artifact directories. The ceiling is distinct from the number of iterations
that produced artifacts. A later correction note reported 56, which matches the
recorded commit count rather than the artifact count.

The graph parser treated filename and task-ID mentions as dependency claims.
This treated a mention of a file as evidence that the agent had used it.
At iteration 6, the agent added a verifier that looked for
imports, file modifications and temporal consistency in the corresponding commits.
Its saved report was:

```text
ADVERSARIAL DAG — 8 claimed edge(s) checked against git:
  2 ok · 3 unsupported · 3 PHANTOM · 0 unverifiable
```

The [plotting data and code](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-06-18-resume-audit/make_figs.py#L44-L54)
record these reported counts.

{% include figure.html
   src="/img/blog/2026-06-18-resume-audit/claimed-vs-verified.webp"
   alt="Eight claimed lineage links at iteration 6: two confirmed against git,
        three unsupported and three contradicted."
   caption="The saved iteration-6 audit. Phantom means the claim conflicts with
            the record, including files created in the same commit that
            supposedly reused them. These counts do not summarize the full run."
%}

Two phantom links credited reuse of files first created in that same commit.
The third linked iteration 2 to iteration 4. The earlier entry had actually
said there was no reuse, then mentioned a task queued for later. The parser
converted that future task reference into a dependency.

Another entry said there was no reuse because `dynamics.py` was too specific to
its original problem. The filename still became an arrow. The error lay in
turning an unqualified text match into a factual claim.

## Unsupported claims need a separate category

The three unsupported links did not all have the same status. Two represented
one real derivation: iteration 4 copied and adapted the kernel from iteration
2, rather than importing its module. The verifier's import-and-modification
checks could not establish that relationship. The third was the spurious
`dynamics.py` link. Since the module already existed, the checker could neither
confirm the claimed reuse nor reject it on temporal grounds.

Calling all six unconfirmed links false would therefore misstate the finding.
The checker detected code dependencies, not every form of intellectual
influence. Its middle category preserved that limit.

The logbook later summarized this snapshot as roughly fourfold inflation: eight
claimed edges divided by two confirmed edges. That ratio describes the parser's
output relative to this check at iteration 6. It does not estimate how much the
agent exaggerated across the whole run.

## The sibling run used a different counting rule

A second run used the same harness and task with a standard values file; the
auditor came from the run with Nietzsche-inspired values. This was one run per
condition, an exploratory comparison [described separately](/blog/nietzsche/).
The sibling reached iteration 60 and left 57 artifact directories.

Its final graph reported 56 build-on edges. Its parser searched only for
`iterNN` references in the `builds-on` field, avoiding the filename-scraping
errors above. All 56 point to earlier iterations, and none comes from a field
saying there was no reuse.

The sibling's README called the count a lower bound because unnamed reuse
would be missed. That is a coverage caveat, not proof that all 56 named links
are valid. The run built a schema checker and tool self-tests, but no checker
that compared those lineage claims with code history. Its true amount of reuse
could be higher or lower than the reported graph suggests.

## A useful check that was not preserved

The first run left the lineage audit outside its required workflow. A standing
lesson told later iterations to run it, but no later entry records
doing so. A task to connect it to the renderer remained unfinished, and the
harness did not require it before committing.

A later audit reported 133 final claims: 31 phantom, 37 unsupported and 65
unflagged. These are saved historical results. The archived workspaces lost
their per-run `.git` directories, so the verdicts cannot now be reproduced.
Running the checker against the archive still extracts 133 claims, but returns
132 as unverifiable; the remaining temporal contradiction can be checked
without git.

Self-reported lineage, code dependencies and conceptual influence require
different checks. A credible reuse metric needs a defined counting rule, a check against evidence
outside the logbook, routine execution and preservation of the underlying
record. These runs supplied parts of that process, leaving the total amount of
compounding unresolved.
