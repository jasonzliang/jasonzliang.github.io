---
layout: post
title: >-
  Caesar adapts its research role, usually around a similar template
published: false
date: 2026-04-22
description: >-
  Caesar rewrites its research prompt from the starting page. In 51 of 57
  logged adaptations, the resulting role used the word Cartographer.
image: >-
  /img/blog/2026-04-22-adaptive-role/three-roles.webp
tags: [caesar, agents, prompting]
---

[Caesar](https://jasonzliang.github.io/caesar-agent/) adapts its system prompt
before web exploration. Given a starting query and the first search results, a
language model writes a specialized research role that guides subsequent
reading and navigation.

The mechanism is enabled in the shipped presets, but its effect on answer
quality has not been measured in a controlled comparison. The available logs
show topic-specific missions built around a surprisingly consistent vocabulary:
**51 of 57 role openings use some form of Cartographer**.

## How the role is generated

Caesar begins with a 71-word default role describing an explorer seeking novel
patterns and connections. For a query-started run, it first expands the query,
executes searches and merges the results into a local HTML page. The default
expansion requests five additional queries; the `nano` preset requests nine.
That generated search-results page supplies the initial evidence for adaptation.
A URL-started run instead uses the supplied page.

The adaptation instruction asks the model to preserve the existing exploration
philosophy, set a goal based on the starting query and focus on promising areas
revealed by the page. It requests a creative, original role description of
roughly 350 words by default, or 400 in creative benchmark configurations,
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

Several guards keep the default role when adaptation fails. Missing page text
skips the step; an empty reply or one shorter than 50 characters is rejected;
exceptions also retain the default. A resumed run restores its saved role from
the checkpoint rather than generating another.

The library default disables adaptation; the supplied command-line and web
presets enable it for new exploration runs. Optional hand-written philosophical
personas are a separate feature.

## What changes across topics

The inspected sample contains 57 run logs across seven distinct starting
queries, excluding separately named `exp_*` experiments. In 51 roles, the
opening paragraph contains *Cartographer*; in 42, it contains *explorer*; in 53,
it contains at least one of those terms. The topic-specific modifiers vary
more than the basic persona: examples include Speculative Affective, Culinary
Calculus, White-Space Venture and Counterfactual Sensory.

This consistency is compatible with the instruction itself. The model receives
the current role and is told to use it as a basis; the default explorer persona
already points toward a mapping metaphor. The logs therefore demonstrate prompt
adaptation, but provide limited evidence of broad variation in the generated
research strategy.

The first page also deserves a precise description. In one inspected
query-started run, it contained 180 search hits across nine queries, each with a
title, URL and snippet. Such a page provides vocabulary, candidate sources and
initial directions. It does not provide a full reading of the field or a tested
assessment of which direction will prove useful.

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
The presence of a specialized role in the logs is evidence that the feature
executes, not that it helps.

The [hub-versus-leaf comparison](/blog/hub-vs-leaf/) measures another aspect of
Caesar's notes. It also lacks the same-page context ablation needed to isolate
its proposed mechanism. Its results cannot substitute for a test of role
adaptation.

A useful next evaluation would measure answer quality, navigation and cost
across matched runs, including a fixed-role baseline. Until that comparison
exists, the supported conclusion concerns observed prompt variation, not
improved research performance.
