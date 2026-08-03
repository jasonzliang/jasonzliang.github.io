# Blog — how it works & how to post

The blog lives at **`/blog/`** and is powered by **Jekyll**, which GitHub Pages
builds automatically on every push. Your hand-built pages (`index.html`,
`publications.html`, `experience.html`, `projects.html`) are **not touched** by
Jekyll — they have no front matter, so they're copied through verbatim.

## Publish a post in 3 steps

```bash
# 1. Scaffold a new post + its image folder
./new-post.sh "My Post Title"
#    → _posts/2026-07-28-my-post-title.md  and  img/blog/my-post-title/

# 2. Edit the Markdown, drop images into the image folder

# 3. Commit & push — GitHub Pages rebuilds automatically
git add -A && git commit -m "post: my post title" && git push
```

The post goes live at `https://jasonzliang.github.io/blog/my-post-title/`
within ~1 minute. It also appears automatically on the `/blog/` index and in
the RSS feed at `/blog/feed.xml`.

## Post front matter

```yaml
---
layout: post
title: "My Post Title"
date: 2026-07-28
description: "One-sentence summary (shown on the index + in Google/social previews)."
tags: [agentic-ai, neuroevolution]
# image: /img/blog/my-post-title/cover.png   # optional preview image
---
```

`description` and `image` feed `jekyll-seo-tag`, which auto-generates the
per-post `<title>`, canonical URL, Open Graph, and Twitter card tags — so every
post is SEO-clean with zero manual meta.

## Content building blocks

**Captioned image** (files go in `img/blog/<slug>/`):

```liquid
{% include figure.html src="/img/blog/my-post/diagram.png" alt="..." caption="..." %}
```

**Video** (YouTube or self-hosted):

```liquid
{% include video.html id="YOUTUBE_ID" title="..." %}
{% include video.html src="/img/blog/my-post/clip.mp4" poster="/img/blog/my-post/poster.jpg" %}
```

**Code** — fenced blocks get syntax highlighting automatically. Standard
Markdown covers headings, **bold**/*italic*, lists, > blockquotes, tables, and
links.

A worked example of all of the above lived in `_posts/2026-07-28-welcome.md`,
removed once the blog went live. To get the template back:

```bash
git show 7572284:_posts/2026-07-28-welcome.md > _posts/$(date +%F)-draft.md
```

## Preview locally (optional)

Not required — you can just push and let GitHub build. To preview locally you
need **Ruby ≥ 3.1** (the system Ruby 2.6 on this Mac is too old):

```bash
bundle install
bundle exec jekyll serve      # http://localhost:4000/blog/
```

Or, if you have Docker:

```bash
docker run --rm -v "$PWD:/srv/jekyll" -p 4000:4000 jekyll/jekyll:latest \
  jekyll serve --host 0.0.0.0
```

## Files this adds

| Path | Purpose |
|------|---------|
| `_config.yml` | Jekyll config (URLs, plugins, SEO inputs) |
| `_layouts/default.html` | Shared shell — replicates the site header/footer/fonts |
| `_layouts/post.html` | Single-post article layout |
| `blog/index.html` | The blog listing page |
| `_includes/figure.html`, `video.html` | Reusable image/video snippets |
| `css/blog.css` | Blog + post styling (reuses your `style.css` tokens) |
| `_posts/` | Your posts (Markdown) |
| `img/blog/` | Per-post images/media |
| `new-post.sh` | Scaffolds a new post |
| `Gemfile` | Local-dev only (GitHub Pages ignores it) |

Nothing else on the site changed except a **"Blog" link added to the nav** on
the four existing pages and a `/blog/` entry added to `sitemap.xml`.
