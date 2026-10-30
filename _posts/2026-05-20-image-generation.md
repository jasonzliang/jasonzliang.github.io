---
layout: post
title: >-
  Caesar illustrates reports using images from cited sources
date: 2026-05-20
description: >-
  One report yielded 343 candidate images from 20 cited pages. A vision
  model scored 60 and retained four, whose details shaped the illustration.
image: >-
  /img/blog/2026-05-20-image-generation/generated.webp
tags: [caesar, agents, multimodal]
---

[Caesar](https://jasonzliang.github.io/caesar-agent/) can illustrate a finished
report using images found on its cited pages. The pipeline revisits those
sources, filters and scores candidate images, then uses selected references to
help write a generation prompt.

A run about [biomimetic architecture](https://en.wikipedia.org/wiki/Biomimetic_architecture)
shows both the specificity this adds and the errors it can carry forward. Four
references contributed recognizable visual details. One incorrect description
of stone columns as wood also reached the final image. Source-derived imagery
therefore provides context, not a guarantee of factual accuracy.

## From cited pages to four references

| Stage | Count |
|---|---:|
| Cited pages revisited | 20 |
| Candidates after scraping filters | 343 |
| Candidates scored by the vision model | 60 |
| References retained | 4 |

The scraper collects image candidates from cited pages, removes duplicate URLs
and filters known boilerplate path segments such as `logo`, `icon`, `favicon`,
`avatar` and `pixel`. The **343** candidates are what remain after filtering.
There is no size filter, so decorative headers, author photographs and other
irrelevant material can survive.

The vision-scoring budget is capped at 60. In this run, the cap selected 60
without relevance ranking; **283 candidates were never visually assessed**.
Each selected candidate received a score from 0 to 10 for suitability as a
reference for the report's opening. Candidates below 4.0 were discarded; the
rest were ranked, with at most four retained and at most two from one domain.

A later implementation first ranks candidates using text from alt attributes
and URL keywords, selects the top 50, and samples 10 from the remaining pool.
The random component allows images with poor metadata to enter consideration.
Both Wikimedia references retained in the earlier run had empty alt text.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/funnel.webp"
   alt="A schematic grid representing 343 candidate images: 283 unscored,
        56 scored but not retained, and four retained. The positions do not
        identify the actual candidate ordering."
   caption="Candidate counts from one run. Sixty scored images and four
            references are configured caps; square positions are illustrative."
%}

The retained references scored **8.0, 8.0, 8.0 and 7.0**. Two were
[Wikimedia Commons](https://commons.wikimedia.org/) files embedded in a cited
Wikipedia article. Two came from a video-intercom company's blog, with alt text
describing tree-inspired architecture and a biomimetic city skyline.

A vision model described each reference. A language model then combined those
descriptions with the report to write an image prompt, specifying an upward
interior view, branching pale-wood ribs, faceted canopy panels and circular
skylights.

## Tracing visible details

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/generated.webp"
   alt="Generated architectural illustration with pale wooden branching ribs,
        circular skylights, lattice towers, planted high-rises and an inset
        diagram labeling maintenance service pods."
   caption="A generated illustration informed by four source images. It is a
            conceptual rendering, not evidence of a built structure."
%}

The image contains lattice towers and planted high-rises resembling details in
the selected references. An annotated deep-sea sponge photograph offers a more
specific trace. Its caption described red arrows and white markings as giving
the image a documentary appearance; the prompt requested a documentary inset,
and the output contains a labeled technical panel.

This is an interpretation of the recorded descriptions, prompt and visible
output. The pipeline does not log which reference controls each output region.
The numbered provenance overlay below was matched by eye.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/provenance.webp"
   alt="Four manually matched regions in the generated image: branching ribs
        associated with Sagrada Família, an annotated inset associated with a
        sponge photograph, and towers associated with two architecture images."
   caption="Manual visual matches to the four references. The run records
            descriptions and the generation prompt, not region-level attribution."
%}

The Sagrada Família reference exposes a factual failure. Its branching columns
are stone, but the vision description called them pale wood. That material
entered the prompt and appears in the output. Reusing sources can transmit
misreadings along with useful details; visual resemblance alone cannot validate
the result.

## Other reports and fallback behaviour

The same pipeline processed four earlier reports on a later build. Their
outputs vary substantially in style, but the examples do not measure image
quality or isolate the contribution of references.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/gallery.webp"
   alt="Four generated images: a lithographed recipe-calculus card, a textured
        echolocation museum alcove, a cashbox and receipt in a clinic, and a
        white-background creativity-scoring equation diagram."
   caption="Four reports processed by the same later generator configuration.
            These examples use a different build from the architecture run."
%}

The prompt-writing model normally chooses among twelve visual idioms supplied
by the template, including etching, lithograph, blueprint, cyanotype and
specimen plate. It matches an idiom to the subject and borrows palette or
materials from reference descriptions. A separate diagram mode, triggered by
patterns in the report text, forces a flat technical presentation and excludes
reference images.

The creativity-scoring report produced 171 candidates, with a best score of
4.0. That falls below the **7.0 best-reference gate** required to use images.
The image was generated from text alone. Diagram mode had already disabled
references, so the score gate did not determine that choice. This example
cannot establish that the gate improved the result.

## Selection settings and their limits

The 4.0 individual-candidate cutoff and 7.0 best-reference gate have different
roles. Below the latter, the captioning pass is skipped and the prompt is
written from the report alone. Above it, selected references can supply both
visual input and descriptions.

The 7.0 gate is intended to avoid distracting references, but the examples do
not establish that this threshold is optimal.

A configuration comment reports another selection failure: one vision scorer
clustered scores near the rubric's middle, leaving little signal for reranking.
This is an implementation observation, not a controlled model comparison.

The pipeline reuses material gathered during research, much as saved
[exploration snapshots](/blog/graph-growth/) enable later analysis. Its examples
show source-specific visual details and identifiable error propagation. A
matched comparison with text-only generation would be needed to establish
whether the additional scraping, scoring and captioning improve illustrations
overall.
