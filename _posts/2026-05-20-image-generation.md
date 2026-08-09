---
layout: post
title: "An agent illustrates its report from the pages it cited"
date: 2026-05-20
description: >-
  Caesar finishes a research report, goes back to the pages it cited, scrapes
  343 images, keeps four, and draws its own illustration from what it saw.
image: >-
  /img/blog/2026-05-20-image-generation/generated.webp
tags: [caesar, agents, multimodal]
---

*[Caesar](https://jasonzliang.github.io/caesar-agent/) is a research agent I
work on: it explores the web and writes long-form answers.*

A finished research report is a wall of text. The obvious fix, an image model
drawing something from the report's title, produces generic stock-art: the model
has no idea what the report is about, so it renders the most average
interpretation of the words.

Caesar already has something better sitting unused: **the pages it cited.** It
just cited twenty sources, and those have pictures. Whatever the report is
about, somebody has already illustrated it, probably badly, but *accurately*.

So the pipeline goes back and looks.

## The funnel

For one run, on a question about biomimetic architecture:

| Stage | Count |
|---|---|
| Cited pages revisited | 20 |
| Candidates left after the scrape filters | **343** |
| Scored by the vision model (the cap is 60) | **60** |
| Kept as references (the cap is four) | **4** |

Every image on every cited page gets pulled. A boilerplate filter throws out any
URL with a path segment that is exactly `logo`, `icon`, `favicon`, `avatar`,
`pixel` or a dozen more, duplicates collapse, and 343 is what came out the far
side, not what went in. Nothing is filtered on size, so plenty of junk survives:
navigation graphics the token list does not name, author photographs, decorative
headers.

Scoring all 343 with a vision model is the obvious next move and the pipeline
refuses. Scoring is capped at 60 candidates, so **only 60 of the 343 ever get
looked at** and 283 are never seen. Each is scored 0 to 10 as a visual reference
for the report's opening; anything under 4.0 is dropped, the survivors ranked,
the top four kept, with a per-domain limit of two so no image-heavy source
supplies the whole set.

Which 60 is the part that has changed since. In this run there was no ranking:
the cap just took 60 of the 343. The pipeline now ranks all 343 with a cheap
text-only heuristic over alt text and URL keywords, takes the top 50, and adds
10 at random from the tail, because a purely ranked pool only surfaces images
whose alt text or URL already sounds relevant. Both Wikimedia references below
arrived with alt text of exactly nothing.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/funnel.webp"
   alt="A grid of 343 small squares, one per scraped image. Most are pale grey;
        56 mid-grey ones were scored but not kept, scattered at random because
        the run does not record which, and four blue ones in the bottom row
        were kept."
   caption="The number nobody chose is 343: 60 and four are configured caps,
            the scoring and reference budgets."
%}

The four here scored **8.0, 8.0, 8.0 and 7.0**. Two are Wikimedia Commons files
embedded in the Wikipedia article the report cited, neither with alt text. The
other two, from a blog post on the site of a company that sells video intercoms,
have it: *"biomimetic architecture example trees"* and *"skyline of city using
biomimetic architecture"*.

Then a vision model writes a dense description of each survivor, and a language
model turns the report plus those descriptions into an image prompt, which
opens:

> Low-angle upward view inside a biology-logic-driven sculptural building: pale
> wood branching ribs and faceted canopy panels form a clear load path, with
> circular skylights and recessed round fixtures punctuating the ceiling.

## The result

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/generated.webp"
   alt="An upward view inside a pale wood structure with branching tree-like
        ribs and circular skylights, lattice towers covered in greenery beyond,
        and an inset technical diagram labelling maintenance service pods."
   caption="Drawn from four images scraped from the report's own cited sources."
%}

The lattice towers behind the structure are one reference showing through, and
the glass towers with vertical planting on the right another, a city skyline.
The inset technical panel with callout labels is the better example: nobody
specified an inset, or callouts, or labels. All the prompt-writing step was told
about the references was one line: "Anchors visual style, palette, composition,
and lighting in the reference captions when available". The second reference was
a *labelled* photograph of deep-sea sponges, which the vision model described
as: "Red arrows and small white marks are overlaid on the image, giving it an
annotated, documentary look." The step read that as style and asked for a
"documentary" inset: a quirk of one source photograph propagating into the
finished illustration.

Where the descriptions go, the errors go too. The first reference is a
photograph looking up inside the Sagrada Família, whose branching columns are
stone. The vision model called them "pale wood", the prompt asked for "pale wood
branching ribs", and the finished picture is unmistakably wood.

Every clause of the prompt goes back to a reference, and from there to the
picture by eye.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/provenance.webp"
   alt="The generated image with four numbered boxes on it, headed 'Where each
        region came from, matched by eye', each listed against a reference and
        its score: branching wood ribs from a photo of Sagrada Familia arches,
        the annotated pod inset from a labelled photograph of a Venus flower
        basket sponge, the lattice towers and green-clad high-rises from two
        photographs on a commercial site."
   caption="The boxes are mine, drawn by hand. The run records four captions
            and the prompt written from them, not regions of the output, so the
            last step of this match is my eye."
%}

The illustration is specific to *these* sources, not the topic in the abstract:
a different run, citing different pages, gets a different picture.

So I pointed the same post-processor at four earlier reports on unrelated
questions, changing nothing. They ran on a later build than the picture above,
so they are comparable with each other rather than with it.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/gallery.webp"
   alt="Four generated images: a recipe calculus question gave a
        black-and-white lithographed recipe card with a no-arbitrage loop
        diagram, echolocation a museum alcove of textured tiles, a business
        idea a photorealistic cashbox and receipt in a bamboo-walled clinic,
        and creativity scoring a clean whitepaper equation figure."
   caption="Four reports, one unchanged generator, four visual registers."
%}

No human chooses the visual register report by report, but "nobody chose" would
be too strong. A prompt-writing model does, from a menu of twelve the template
supplies (etching, lithograph, blueprint, cyanotype, specimen plate and seven
more), told to match the idiom to the subject's native register and borrow
palette and materials from vivid reference captions.

The fourth is the useful one. On the creativity-scoring question the agent
scraped **171** images and the best scored 4.0, well under the 7.0 gate, so no
reference pixels were sent and the picture came from the text alone: the
threshold in the next section doing its job, no references beating one mediocre
one. It is weaker evidence than it looks, though: that report would have gone
text-only regardless, because a regex over the report text had already routed it
into diagram mode, which overrides that menu, drops reference images by design
and forces the flat whitepaper look.

## Two settings that carry the real lessons

Most of this pipeline is plumbing. Two configuration values are not.

**The scoring model has to be a strong one.** The config comment is blunt:

> gpt-4o collapses scores to the rubric's middle (no spread) so the rerank
> signal dies — keep at gpt-5.4.

A weaker vision model does not score badly, it scores *uniformly*: asked to rate
sixty images from 0 to 10, it puts almost everything near the middle, and once
every candidate scores about the same the ranking carries no information. The
pipeline runs, produces output, and the selection stage silently does nothing.

This failure shows up everywhere in evaluation work: a measurement that cannot
discriminate is worse than none, because it looks like it is working. I have run
into it with [saturated benchmarks](/blog/circle-packing/), where every method
reaches the same ceiling; here, a vision model refusing to use the ends of its
own scale.

**Weak references are worse than none.** The scraped images go to the image
model directly as visual references only if the *best* one scores at least 7.0.
Below that, the config notes, "mid-quality refs bias the model more than they
help": a roughly-relevant photo drags the output toward itself without
contributing anything true. A lower threshold, a constant in the code rather
than a config knob, drops any individual reference under 4.0, where the logos
and interface chrome go.

Below 7.0 the survivors are not even described in words: the captioning pass
never runs and the prompt is written from the report alone. The run above
cleared the gate, its best reference scoring 8.0.

## Why I like this pattern

The general shape is: **an agent that has already done work should mine that
work before reaching for something new.** The images were already in the HTML
Caesar downloaded when it cited those pages; using them costs one more pass over
data it had and turns a generic illustration into a specific one grounded in the
same sources as the text. I suspect there are several more lying around any
agent that keeps state: the exploration graph was another, [months of snapshots
nobody had plotted](/blog/graph-growth/), material already on disk, generated as
a side effect of doing something else.