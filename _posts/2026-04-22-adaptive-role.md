---
layout: post
title: >-
  Caesar adapts its research role, usually around a similar template
published: false
date: 2026-04-22
description: >-
  Topic-specific research prompts often keep the same explorer persona;
  whether adaptation improves answers remains untested.
image: >-
  /img/blog/2026-04-22-adaptive-role/three-roles.webp
tags: [caesar, agents, prompting]
---

[Caesar](https://jasonzliang.github.io/caesar-agent/) [adapts its system prompt
before web exploration](https://arxiv.org/html/2604.20855v3#S2.SS2). Given a starting query and the first search results, a
language model writes a specialized research role that guides subsequent
reading and navigation.

The mechanism is enabled in the shipped presets, but its effect on answer
quality has not been measured in a controlled comparison. The available logs
show topic-specific missions built around a surprisingly consistent vocabulary:
**51 of 57 role openings use some form of Cartographer**.

## How the role is generated

Caesar begins with a [71-word default role](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/caesar_agent.py#L101-L110) describing an explorer seeking novel
patterns and connections. For a query-started run, it first expands the query,
executes searches and merges the results into a local HTML page. The default
expansion requests five additional queries; the [`nano` preset](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/config/config_preset/nano.yaml#L14-L31) requests nine.
That generated search-results page supplies the initial evidence for adaptation.
A URL-started run instead uses the supplied page.

The [adaptation instruction](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/caesar_agent.py#L217-L280) asks the model to preserve the existing exploration
philosophy, set a goal based on the starting query and focus on promising areas
revealed by the page. It requests a creative, original role description of
roughly [350 words by default](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/caesar_config.py#L83-L96), or [400 in creative benchmark configurations](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/config/config_creative/constrained_creativity.yaml#L31-L34),
starting with the literal prefix `Your role:`. The resulting text becomes the
system prompt for the rest of the run.

{% include figure.html
   src="/img/blog/2026-04-22-adaptive-role/three-roles.webp"
   alt="Three queries paired with generated research roles: a new emotion with
        Speculative Affective Cartographer, calculus applied to cooking with
        a structural translator, and a business idea with Blue-Ocean
        Cartographer of Hidden Frictions."
   caption="Three roles from a five-run batch launched within eight seconds
            using the same checkout and model. Excerpts come from console logs;
            ellipses mark omitted text."
%}

[Several guards keep the default role when adaptation fails](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/caesar_agent.py#L227-L280). Missing page text
skips the step; an empty reply or one shorter than 50 characters is rejected;
exceptions also retain the default. A resumed run [restores its saved role from
the checkpoint](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/checkpoint.py#L142-L146) rather than generating another.

The [library default](https://github.com/jasonzliang/caesar-agent/blob/67fd931d491d39ec92f40ef27f91feb00b2173bc/caesar/caesar_config.py#L146-L153) disables adaptation; the supplied command-line and web
presets enable it for new exploration runs. Optional hand-written philosophical
personas are a separate feature.

## What changes across topics

The inspected sample contains 57 run logs across seven distinct starting
queries, excluding separately named `exp_*` experiments. In 51 roles, the
opening paragraph contains *Cartographer*; in 42, it contains *explorer*; in 53,
it contains at least one of those terms. The topic-specific modifiers vary
more than the basic persona: examples include Speculative Affective, Culinary
Calculus, White-Space Venture and Counterfactual Sensory.

The role counts and search-hit example use unpublished run logs;
[illustrated excerpts](https://github.com/jasonzliang/jasonzliang.github.io/blob/0a7b590e1e708c903dbf69ffc0a18d7c6b969a49/img/blog/2026-04-22-adaptive-role/make_figs.py#L67-L84) are available in the plotting code.

The adaptation instruction gives the model the current role as a basis; the
default explorer persona already points toward a mapping metaphor. The logs
demonstrate prompt adaptation, but provide limited evidence of broad variation
in the generated research strategy.

In one inspected query-started run, the first page contained 180 search hits
across nine queries, each with a title, URL and snippet. These search results
provide vocabulary, candidate sources and initial directions. They do not
provide a full reading of the field or a tested assessment of which direction
will prove useful.

## A plausible mechanism without a measured benefit

A topic-specific role could make relevant distinctions explicit in the context
used for later decisions. For example, it might emphasize evidence standards,
useful analogies or constraints suggested by the initial search. This is a form
of automated [prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering):
the system turns retrieved context into instructions that persist through the
run.

Whether that persistence improves the final answer remains open. There is no
[ablation study](https://en.wikipedia.org/wiki/Ablation_study) comparing matched
runs with adaptation enabled and disabled while holding other settings fixed.

The [hub-versus-leaf comparison](/blog/hub-vs-leaf/) measures another aspect of
Caesar's notes. It also lacks the same-page context ablation needed to isolate
its proposed mechanism. Its results cannot substitute for a test of role
adaptation.

A matched evaluation would measure answer quality, navigation and cost,
including a fixed-role baseline.
