---
layout: post
title: >-
  The agent rewrites its own job description. I cannot tell you if it helps.
date: 2026-04-22
description: >-
  Before exploring anything, Caesar reads one page and rewrites the system
  prompt that defines what kind of researcher it is. This is on by default, and
  I cannot tell you whether it helps.
image: >-
  /img/blog/2026-04-22-adaptive-role/three-roles.webp
tags: [caesar, agents, prompting]
---

*[Caesar](https://jasonzliang.github.io/caesar-agent/) is a research agent I
work on: it explores the web on its own and writes long-form answers. This is
one of a series of posts about how it works.*

Most agent systems have a system prompt that says what the agent is. "You are an
expert research assistant." It is written once, by a human, and it is the same
for every task the system ever runs.

Caesar ships with one of those too, all 71 words of it, opening "You are an
explorer seeking novel patterns and connections in information." Before it
explores anything, it replaces that with one it writes itself.

## How it works

The order matters, so here it is. Given a starting query rather than a starting
URL, Caesar's first act is not the rewrite: it asks the model for a handful of
extra search queries (five by default, nine in the `nano` preset), runs them all
through a search API, and saves the merged hits to a local HTML file. *That*
file is the "starting page." Only then does it fetch the page back and ask for a
replacement role description. The instruction it receives:

> Using your current role as basis, analyze the page content to create a
> specialized role that:
>  - Improves upon core exploration philosophy
>  - Creates an overall goal for the agent to strive for based on the starting
>    query
>  - Focuses exploration toward most promising areas revealed by the page
>    content
>
> Provide an adapted role description (~350 words) that is creative, innovative,
> and original!
>
> IMPORATNT: Your response must start with "Your role:" followed by the adapted
> role description.

That is the rendered prompt, not the template, and three things about the
difference are worth stating. The `~350` is a config value called
`role_max_length`; 350 is its default and what all three presets get, but the
benchmark configs raise it to 400, and until a change last December the same
line asked for a number of tokens rather than words. The clause "based on the
starting query" is conditional and appears only when the run starts from a
query. And if an insights file is configured, two further clauses appear asking
the new role to build on it; no shipped preset configures one, so they are
absent above. The misspelling in the last line is in the source, and it is why
every adapted role in the logs opens with "Your role:".

{% include figure.html
   src="/img/blog/2026-04-22-adaptive-role/three-roles.webp"
   alt="Three cards under the heading 'One batch, one instruction. Three
        queries, three self-written roles.' Each card gives the query the run
        started from and the role the agent then wrote for itself. Asked to
        invent a new emotion humans do not experience, it called itself a
        Speculative Affective Cartographer. Asked to apply the structure of
        calculus to cooking, a structural translator of recipes into
        calculus-like transformations. Asked to invent a completely original
        business idea, a Blue-Ocean Cartographer of Hidden Frictions."
   caption="Three of the five runs in one batch, launched within eight seconds
            of each other from the same checkout with the same model, so the
            only thing that differs is the query. Queries and role text are
            verbatim from the runs' console logs, with ellipses marking cuts.
            Two of the three called themselves Cartographers, which is the
            subject of the next section."
%}

What comes back becomes the agent's system prompt for the rest of the run,
subject to three guards worth naming: if the page yields no text nothing is
adapted, if the reply is empty or under fifty characters the default role is
kept, and any exception leaves the default in place. A run resumed from a
checkpoint skips the step and reloads the role it already had. A question about
protein folding produces a different researcher than a question about municipal
transit policy: not different *instructions*, a different self-description,
written by the agent from one page of evidence about where its search landed.

This is not an experimental flag. The library default in `caesar_config.py` is
`adapt_role: False`, but every preset that ships flips it on: `adapt_role: True`
in all three command-line presets (`nano`, `mini`, `regular`) and in all four
the web app ships. So every default run of Caesar does this. The one exception I
can find is the web app's synthesis-only follow-up path, which turns the flag
back off along with the entire exploration loop, so there is nothing to adapt to
anyway.

## What the roles actually look like

Before making the case for this, here is the thing that argues hardest against
it, which I found while checking the figure.

The run directory in my repo holds 57 runs with a role adaptation in the log,
covering seven distinct starting queries. In **51 of the 57** the agent named
itself some kind of *Cartographer*. In 42 the opening line contains the word
*explorer*; 53 contain one or the other.

That is not a coincidence, and it is not the model being unimaginative in a
vacuum. The prompt hands the model its current role and tells it to use that "as
basis," and the current role, on a fresh run, is the default one that opens "You
are an explorer seeking novel patterns and connections in information." So what
actually varies across topics is the modifier and the mission statement.
Speculative Affective, Culinary Calculus, White-Space Venture, Counterfactual
Sensory. The noun and the sentence shape barely move.

Whether a topic-specific modifier bolted to a near-fixed template is worth
anything is exactly the question the rest of this post says I cannot answer. I
mention it here so that nobody reads the figure as more variety than it is.

## Why it might work

The argument is about specificity. A generic research persona has to be generic
enough to cover every possible topic, which means it cannot contain anything
useful about *this* topic. It cannot tell the agent which distinctions matter
here, what counts as a promising thread, or what a good answer in this field
looks like.

The starting page carries some of that, implicitly. It is worth being clear
about what that page is: on a query-started run it is not an article the agent
stumbled onto, it is the merged search-results file Caesar just generated, which
in one run I opened held 180 results across nine queries, each one a title, a
URL and a snippet. That is still a dense sample of the field's vocabulary and
its landmark sources, and if you hand the agent a starting URL instead, it is
whatever real page you handed it. Asking the model to turn that into a
specialist's self-description is a cheap way to move it into the context that
governs every subsequent decision.

There is also a less flattering reading, which is that this is prompt
engineering that the system does to itself so that a human does not have to. I
think that reading is basically correct and not actually a criticism.

## What I cannot tell you

Whether it helps.

There is no ablation. An ablation is the plainest comparison there is: run the
system with the feature, run it again with the feature taken out, change nothing
else, and see what the difference was. I have not done that. So I cannot tell
you it improves answer quality, and I am not going to imply it while avoiding
the claim.

That is an uncomfortable thing to admit about a feature that is on by default in
every preset, and it is worth being precise about why it happened. Features like
this get added because they are cheap and the reasoning is appealing, they
visibly do something in the logs, and nothing ever forces the comparison.
Meanwhile the things that *do* get examined are the ones carrying a claim
somebody can check.

I have measured [where in the exploration graph an insight comes
from](/blog/hub-vs-leaf/). That did not happen because graph position matters
more than the role does. It happened because there was a claim about graph
position in public with a number in it, and a number in public is a thing that
can be shown wrong: that post has since been corrected twice, once about what
was actually being scored and once about which unit the effect size was measured
at. I should be careful about how much credit it earns even so. It was a
measurement, not an ablation, and that post closes by saying the ablation it
actually needs, the same page read once with neighbour context and once without,
has not been run either. But it did at least get looked at. The adaptive role
has never carried a claim of that kind, so nothing has ever pulled it into the
open, and it sits in the default configuration, unmeasured, doing something.

## The self-transcendence files, which are not switched on

There is a related thing in the repository I want to describe accurately,
because it would be easy to overstate.

Alongside the adaptive role, there are hand-written persona files with names
like `self_transcend_role_v1`. They are a deliberate mashup of Nietzsche and
Buddhism, naming Überwindung and Dukkha outright, with sections titled
"Impermanent Identity," "Creative Dissatisfaction," "Willful Becoming," "Chaotic
Leaps" and "The Pathless Path," written to give the agent a disposition toward
restlessness rather than closure.

They are **commented out in all three shipped presets.** They exist, they were
tuned as recently as April, and the default configuration does not load them.
The commented-out lines in the presets point into `config/role/`, a directory
that does not exist; the files actually live in `config/custom_role/`, so
uncommenting those particular lines would not even load them.

To be exact rather than tidy: five other config files, none of them among the
three presets, do still name one of these files without commenting it out. Four
of the five point into that same dead `config/role/` directory and would fail to
load anything. The fifth, `config/config_test/single_agent_test.yaml`, points at
the real path, and its `overwrite_role_file` line is applied *before* the
`adapt_role` check, so that config genuinely does seed the agent with
`self_transcend_role_v1` before anything else happens. It is a test config, not
a preset. On a default run the agent writes its own role from the page; it is
not seeded with that persona first.

I mention them because the idea connects to a related question I take up on a
different system, a loop that runs a coding agent rather than Caesar: [what an
agent writes when it can rewrite its own values](/blog/values-rewriting/).
Across 41 runs there, every agent permitted to edit its values did so, and a
guardrail on their length held every time. That study is explicit that it cannot
say whether the resulting agents were any better or any worse, and it is a
different system besides, so it is not an ablation of `adapt_role` and does not
stand in for one. Nothing here has been ablated, and this feature is still
unmeasured.

## The honest summary

Caesar rewrites its own job description from the first page it reads, on every
run, by default. You can watch it happen in the logs, and what you will mostly
see there is the word *Cartographer*. Whether it improves a single answer is
unmeasured, and I would treat any intuition about that, including mine, as
unsupported until someone runs the comparison.
