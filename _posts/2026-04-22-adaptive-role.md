---
layout: post
title: >-
  The agent rewrites its own job description. I cannot tell you if it helps.
date: 2026-04-22
description: >-
  Before exploring, Caesar reads one page and rewrites the prompt defining what
  researcher it is. On by default, 51 of 57 runs produced nearly the same role,
  and I cannot tell you whether it helps.
image: >-
  /img/blog/2026-04-22-adaptive-role/three-roles.webp
tags: [caesar, agents, prompting]
---

*[Caesar](https://jasonzliang.github.io/caesar-agent/) is a research agent I
work on: it explores the web and writes long-form answers.*

Most agent systems have a system prompt saying what the agent is. "You are an
expert research assistant." Written once, by a human, and the same for every
task the system ever runs.

Caesar ships with one of those too, all 71 words of it, opening "You are an
explorer seeking novel patterns and connections in information." Before it
explores anything, it replaces that with one it writes itself.

## How it works

The order matters. Given a starting query rather than a URL, Caesar's first act
is not the rewrite: it asks the model for extra search queries (five by default,
nine in the `nano` preset), runs them through a search API, and saves the merged
hits to a local HTML file. *That* is the "starting page." Only then does it
fetch the page back and ask for a replacement role. The instruction:

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

That is the rendered prompt, not the template, and three differences matter. The
`~350` is a config value called `role_max_length`; 350 is its default and what
all three command-line presets get, but benchmark configs raise it to 400, and
until a change last December the line asked for tokens, not words. The clause
"based on the starting query" appears only when the run starts from a query. If
an insights file is configured, two further clauses appear asking the new role
to build on it; no shipped preset configures one, so they are absent above. The
misspelling in the last line is in the source, and that line is why every
adapted role in the logs opens with "Your role:".

{% include figure.html
   src="/img/blog/2026-04-22-adaptive-role/three-roles.webp"
   alt="Three cards headed 'One batch, one instruction. Three queries, three
        self-written roles.' Each pairs a run's query with the role the agent
        wrote for itself, then quotes its opening line. Invent a new emotion
        humans do not experience: Speculative Affective Cartographer. Apply the
        structure of calculus to cooking: structural translator of recipes into
        calculus-like transformations. Invent a completely original business
        idea: Blue-Ocean Cartographer of Hidden Frictions."
   caption="Three of the five runs in one batch, launched within eight seconds
            of each other from the same code checkout with the same model, so
            only the query differs. Queries and roles are verbatim from the
            console logs, ellipses marking cuts."
%}

What comes back becomes the agent's system prompt for the rest of the run,
subject to three guards: if the page has no text, nothing is adapted; if the
reply is empty or under fifty characters, the default role is kept; on any
exception, the default stays. A run resumed from a checkpoint skips the step and
reloads the role it had. A question about protein folding produces a different
researcher than one about municipal transit policy: not different *instructions*
but a different self-description, written from one page of evidence about where
the search landed.

This is not an experimental flag. The library default in `caesar_config.py` is
`adapt_role: False`, but every shipped preset flips it on: `adapt_role: True` in
all three command-line presets (`nano`, `mini`, `regular`) and in all four web
app presets. The one exception I can find is the web app's synthesis-only
follow-up path, which turns the flag off along with the whole exploration loop,
so there is nothing to adapt to.

## The roles are nearly all the same

Here is what argues hardest against the feature, found while checking the
figure.

My run directory holds 57 runs with a role adaptation logged, across seven
distinct starting queries. In **51 of the 57** the agent named itself some kind
of *Cartographer*. In 42 the opening line contains the word *explorer*; 53
contain one or the other.

That is not the model being unimaginative in a vacuum. The prompt hands it its
current role and tells it to use that "as basis," and on a fresh run that role
is the default one opening "You are an explorer seeking novel patterns...", a
short step from *Cartographer*. So what varies across topics is the modifier and
the mission statement. Speculative Affective, Culinary Calculus, White-Space
Venture, Counterfactual Sensory. The noun and the sentence shape barely move.

Whether a topic-specific modifier on a near-fixed template is worth anything is
exactly what this post cannot answer. I mention it so nobody reads the figure as
more variety than it is.

## Why it might work

The argument is about specificity. A generic research persona has to cover every
possible topic, so it cannot contain anything useful about *this* one: which
distinctions matter here, what counts as a promising thread, what a good answer
in this field looks like.

The starting page carries some of that implicitly, and it is worth saying what
that page is: on a query-started run it is not an article the agent stumbled
onto but the merged search-results file Caesar just generated; one I opened held
180 results across nine queries, each a title, a URL and a snippet. Still a
dense sample of the field's vocabulary and landmark sources. With a starting URL
instead, it is whatever real page you handed it. Turning that into a
specialist's self-description is a cheap way to move it into the context that
governs every later decision.

There is also a less flattering reading: this is [prompt
engineering](https://en.wikipedia.org/wiki/Prompt_engineering) the system does
to itself so a human does not have to. I think that is basically correct, and
not a criticism.

## What I cannot tell you

Whether it helps.

There is no [ablation](https://en.wikipedia.org/wiki/Ablation_study). An
ablation is the plainest comparison: run the system with the feature, run it
again without, change nothing else, and see the difference. I have not done
that. So I cannot tell you it improves answer quality, and I am not going to
imply it while avoiding the claim.

That is uncomfortable to admit about a feature on by default in every preset,
and worth being precise about why. Features like this get added because they are
cheap, the reasoning is appealing, they visibly do something in the logs, and
nothing forces the comparison. The things that *do* get examined are the ones
carrying a claim somebody can check.

I have measured [where in the exploration graph an insight comes
from](/blog/hub-vs-leaf/), not because graph position matters more than the
role, but because there was a public claim about it with a number in it, and a
number in public can be shown wrong: that post has since been corrected twice,
once about what was being scored and once about which unit the effect size was
measured at. Even so, it was a measurement, not an ablation. That post closes by
saying the ablation it needs, the same page read once with neighbour context and
once without, has not been run either. The adaptive role has never carried a
claim of that kind, so nothing has ever pulled it into the open, and it sits in
the default configuration, unmeasured, doing something.

## The self-transcendence files, off by default

Alongside the adaptive role are hand-written persona files with names like
`self_transcend_role_v1`: a deliberate mashup of Nietzsche and Buddhism, naming
Überwindung and Dukkha outright, with sections titled "Impermanent Identity,"
"Creative Dissatisfaction," "Willful Becoming," "Chaotic Leaps" and "The
Pathless Path," written to give the agent a disposition toward restlessness
rather than closure.

They are **commented out in all three command-line presets.** They were tuned as
recently as April. The commented-out lines point into `config/role/`, a
directory that does not exist; the files live in `config/custom_role/`, so
uncommenting them would load nothing.

To be exact rather than tidy: five other config files, none among the three
presets, still name one of these files uncommented. Four point into that same
dead `config/role/` directory. The fifth,
`config/config_test/single_agent_test.yaml`, points at the real path, and its
`overwrite_role_file` line is applied *before* the `adapt_role` check, so it
does seed the agent with `self_transcend_role_v1`. It is a test config, not a
preset. On a default run the agent writes its own role from the page.

The idea connects to a question I take up on a different system, a loop running
a coding agent rather than Caesar: what an agent writes when it can rewrite its
own values. Across 41 runs there, every agent permitted to edit its values did
so, and a guardrail on the values' length held every time. That study cannot say
whether the resulting agents were better or worse, and it is a different system,
so it is not an ablation of `adapt_role` and does not stand in for one. Nothing
here has been ablated, and this feature is still unmeasured.

## The honest summary

Caesar rewrites its own job description from the first page it reads, on every
run, by default. What you will mostly see in the logs is the word
*Cartographer*. Whether it improves a single answer is unmeasured, and I would
treat any intuition about that, mine included, as unsupported until someone runs
the comparison.
