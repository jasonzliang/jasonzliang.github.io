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
work on: it explores the web on its own and writes long-form answers. This is
one of a series of posts about how it works.*

A finished research report is a wall of text. The obvious fix is to have an
image model draw something, and the obvious way to do that is to hand it the
report's title and hope.

That produces generic stock-art. The model has no idea what the report is
actually about, so it renders the most average possible interpretation of the
words.

Caesar already has something better available, and it is sitting unused: **the
pages it cited.** It just cited twenty sources. Those sources have pictures in
them. Whatever the report is about, somebody has already illustrated it,
probably badly, probably not in the style you want, but *accurately*.

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
`pixel` or a dozen more like them, duplicate image URLs are collapsed, and 343
is what came out the far side of that, not what went in. Nothing is filtered on
image size, so plenty of junk survives: navigation graphics the token list does
not happen to name, author photographs, decorative headers.

Scoring all 343 with a vision model is the obvious next move and the pipeline
refuses to do it. Scoring is capped at 60 candidates, so **60 of the 343 ever
get looked at** and 283 are never seen at all. Each of the 60 is scored 0 to 10
for how useful it would be as a visual reference for the report's opening.
Anything under 4.0 is dropped, what survives is ranked, and the top four are
kept, with a per-domain limit of two so one image-heavy source cannot supply the
whole set.

Which 60 is the part that has changed since. In this run there was no ranking at
all: the cap just took 60 of the 343 and scored those. The pipeline now ranks
all 343 first with a cheap text-only heuristic over alt text and URL keywords,
takes the top 50, and adds 10 sampled at random from the tail.

The random 10 matter more than they look. Without them a ranked pool can only
ever surface images whose alt text or URL already sounds relevant, which is a
good way to never discover the well-chosen photograph somebody forgot to label.
Both of the Wikimedia references below arrived with alt text of exactly nothing.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/funnel.webp"
   alt="A grid of 343 small squares, one per scraped image. Most are pale grey;
        56 scattered mid-grey ones were scored by the vision model, and four
        blue ones in the bottom row were kept."
   caption="One square per candidate image. Both of the small numbers are
            configured caps rather than natural stopping points: 60 is the
            scoring budget and four is the reference budget. The number nobody
            chose is 343."
%}

The four here scored **8.0, 8.0, 8.0 and 7.0**. Two are Wikimedia Commons files
embedded in the Wikipedia article the report cited, and neither carried any alt
text at all. The other two come from a blog post on the site of a company that
sells video intercoms, and those do carry alt text: *"biomimetic architecture
example trees"* and *"skyline of city using biomimetic architecture"*.

Then a vision model writes a dense description of each survivor, and a language
model turns the report plus those four descriptions into an image prompt. The
opening of the prompt it wrote:

> Low-angle upward view inside a biology-logic-driven sculptural building: pale
> wood branching ribs and faceted canopy panels form a clear load path, with
> circular skylights and recessed round fixtures punctuating the ceiling.

## The result

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/generated.webp"
   alt="An upward view inside a pale wood structure with branching tree-like
        ribs and circular skylights, with lattice towers covered in greenery
        visible beyond, and an inset technical diagram labelling maintenance
        service pods."
   caption="Generated for a report on biomimetic architecture, drawn from four
            images the agent scraped from its own cited sources."
%}

The lattice towers in the background are not an accident. One of the four
references was a photograph of exactly that, tree-like metal lattice towers
wrapped in greenery, and the glass towers with vertical planting on the right
are the fourth reference, which was a city skyline.

The inset technical panel with callout labels is the better example. Nobody
specified an inset, or callouts, or labels. What the prompt-writing step was
told about the references was one line: "Anchors visual style, palette,
composition, and lighting in the reference captions when available". The second
reference was a *labelled* photograph of deep-sea sponges, and the vision model
described it this way: "Red arrows and small white marks are overlaid on the
image, giving it an annotated, documentary look." The prompt-writing step did
what it was told, read that description as style, and asked for a "documentary"
inset. A stylistic quirk of one source photograph propagated into the finished
illustration.

Where the descriptions go, the errors go too. The first reference is a
photograph looking up inside the Sagrada Família, whose branching columns are
stone. The vision model called them "pale wood", the prompt asked for "pale wood
branching ribs", and the finished picture is unmistakably made of wood.

You can take the prompt apart and put every clause back to the reference it came
from, then match the clauses to the picture by eye.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/provenance.webp"
   alt="The generated image with four coloured boxes drawn on it, numbered one
        to four, under the heading 'Where each region came from, matched by
        eye'. Each is listed against a reference image and its relevance score:
        branching wood ribs from a photo of Sagrada Familia arches, the
        annotated pod inset from a labelled photograph of a Venus flower basket
        sponge, the lattice towers and the green-clad high-rises from two
        photographs on a commercial site."
   caption="The boxes are mine, drawn by hand. The run records four captions
            and the prompt written from them, not regions of the output, so the
            last step of this match is my eye. The inset that reads as a
            stylistic flourish is the second reference showing through: a
            labelled photograph of deep-sea sponges, arrows and all."
%}

That is the thing worth noticing. The illustration is specific to *these*
sources rather than to the topic in the abstract. A different run, citing
different pages, gets a different picture.

So I pointed the same post-processor at four earlier reports on unrelated
questions, changing nothing between them. Those four ran on a later build of the
generator than the picture above, so they are comparable with each other rather
than with it.

{% include figure.html
   src="/img/blog/2026-05-20-image-generation/gallery.webp"
   alt="Four generated images in a grid. A recipe calculus question produced a
        black-and-white lithographed recipe card with a no-arbitrage loop
        diagram. An echolocation question produced a museum alcove of textured
        tiles. A business-idea question produced a photorealistic image of a
        cashbox and receipt in a bamboo-walled clinic. A creativity-scoring
        question produced a clean whitepaper equation figure."
   caption="Four reports, one generator, unchanged between them. No human
            picked these four registers, but 'nobody chose' would be too
            strong: the prompt-writing model picks the idiom from a menu the
            template hands it, and the fourth was routed into diagram mode by a
            regex over the report text, which forces the flat whitepaper look."
%}

No human chooses the visual register report by report. A prompt-writing model
does, from a menu of twelve the template supplies (etching, lithograph,
blueprint, cyanotype, specimen plate and seven more), under instructions to
match the idiom to the subject's native register and to borrow palette and
materials from the reference captions when those are vivid. That is how one
question ends up as a lithographed recipe card and another as something that
reads like a press photograph.

The fourth is the useful one. On the creativity-scoring question the agent
scraped **171** images and the best of them scored 4.0, well under the 7.0 gate,
so no reference pixels were sent and the picture was drawn from the text alone.
That is the threshold in the next section doing its job: no references is a
better outcome than one mediocre one. It is weaker evidence than it looks,
though, because that report would have gone text-only regardless. The regex
classifier had already routed it into diagram mode, which drops reference images
by design.

## Two settings that carry the real lessons

Most of this pipeline is plumbing. Two configuration values are not, and both
were set by discovering something.

**The scoring model has to be a strong one.** The comment in the config is
blunt:

> gpt-4o collapses scores to the rubric's middle (no spread) so the rerank
> signal dies — keep at gpt-5.4.

A weaker vision model does not score badly. It scores *uniformly*. Asked to rate
sixty images from 0 to 10, it puts almost everything near the middle, and once
every candidate has roughly the same score the ranking carries no information at
all. The pipeline runs, produces output, and the selection stage is silently
doing nothing.

This is the same failure that shows up everywhere in evaluation work: a
measurement that cannot discriminate is worse than no measurement, because it
looks like it is working. I have run into it with [saturated
benchmarks](/blog/circle-packing/), where every method reaches the same ceiling
and the benchmark stops being able to rank anything. Here it was a vision model
refusing to use the ends of its own scale.

**Weak references are worse than none.** The scraped images can be passed to the
image model directly, as visual references. That only happens if the *best* one
scores at least 7.0. Below that, the config notes, "mid-quality refs bias the
model more than they help": a roughly-relevant photo drags the output toward
itself without contributing anything true. A second, lower threshold, this one a
constant in the code rather than a config knob, drops any individual reference
scoring under 4.0, which is where the logos and interface chrome go.

So the design is: use the references when the best of them is good, and drop
them completely when it is not. Not softly, either. Below 7.0 the survivors are
not even described in words; the captioning pass never runs and the prompt is
written from the report alone. The run above cleared the gate comfortably, its
best reference scoring 8.0.

## Why I like this pattern

The general shape is: **an agent that has already done work should mine that
work before reaching for something new.**

Caesar visited those pages, parsed them, and cited them. The images were already
in the HTML it downloaded. Using them costs one more pass over data it had, and
it turns a generic illustration into a specific one grounded in the same sources
the text is grounded in.

I suspect there are several more of these lying around any agent that keeps
state. The exploration graph was another one, [months of snapshots nobody had
plotted](/blog/graph-growth/). The pattern is the same: the interesting material
was already on disk, generated as a side effect of doing something else.
