#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# new-post.sh — scaffold a new blog post + its image folder.
# Usage:  ./new-post.sh "My Post Title"
# Creates: _posts/YYYY-MM-DD-my-post-title.md  and  img/blog/my-post-title/
# ---------------------------------------------------------------------------
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: ./new-post.sh \"My Post Title\""
  exit 1
fi

TITLE="$*"
DATE="$(date +%F)"

# Slugify: lowercase, spaces -> hyphens, strip non-alphanumeric/hyphen, squeeze hyphens
SLUG="$(printf '%s' "$TITLE" \
  | tr '[:upper:]' '[:lower:]' \
  | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//')"

POST="_posts/${DATE}-${SLUG}.md"
IMGDIR="img/blog/${SLUG}"

if [ -e "$POST" ]; then
  echo "Refusing to overwrite existing post: $POST"
  exit 1
fi

mkdir -p "$(dirname "$POST")" "$IMGDIR"
cat > "$POST" <<EOF
---
layout: post
title: "${TITLE}"
date: ${DATE}
description: "One-sentence summary shown on the blog index and in search/social previews."
tags: [tag1, tag2]
# image: /img/blog/${SLUG}/cover.png   # optional social/preview image
---

Write your post here in Markdown.

## A section

Add a captioned image (put files in \`${IMGDIR}/\`):

{% raw %}{% include figure.html src="/img/blog/${SLUG}/example.png" alt="..." caption="..." %}{% endraw %}

Embed a video:

{% raw %}{% include video.html id="YOUTUBE_ID" title="..." %}{% endraw %}
EOF

echo "Created $POST"
echo "Created $IMGDIR/"
echo
echo "Next:"
echo "  1. Edit $POST and add images to $IMGDIR/"
echo "  2. git add -A && git commit -m \"post: ${TITLE}\" && git push"
echo "  3. Live at https://jasonzliang.github.io/blog/${SLUG}/ in ~1 min"
