#!/usr/bin/env python3
"""Align post filenames and figure directories with post titles.

A post's filename drives its URL (`permalink: /blog/:title/`), so when a title
changes the slug should follow. This renames:

    _posts/<date>-<old-slug>.md   ->  _posts/<date>-<new-slug>.md
    img/blog/<whatever>/          ->  img/blog/<date>-<new-slug>/

and rewrites every reference: `/blog/<old-slug>/` links between posts, and
`/img/blog/<old-dir>/` paths in post front matter, figure includes, and the
`make_figs.py` scripts.

SLUGS below is hand-written rather than derived from the title, because
auto-slugging a sentence-length title produces something unreadable. Keys are
the current filename stem; a value of None means "leave the slug alone, only
date-prefix its figure directory".

Re-runnable: entries whose source no longer exists are skipped, so it is safe
to run again after a new post lands.

    python3 _scripts/rename_slugs.py --check    # show the plan, change nothing
    python3 _scripts/rename_slugs.py            # apply
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Second pass: the slug is now set equal to the figure directory's slug, so a
# post and its figures share one name. Long title-derived slugs made the
# `src="/img/blog/<date>-<slug>/<file>.webp"` lines unwrappable at 80 columns,
# and a path cannot be broken across lines. Short slug, long title.
SLUGS = {
    "2026-02-10-we-asked-three-ais-to-grade-seven-ais": "judge-bias",
    "2026-03-30-ai-judges-landslide-humans-56-percent": "human-vs-machine",
    "2026-04-14-notes-from-hub-pages-scored-higher": "hub-vs-leaf",
    "2026-04-22-the-agent-rewrites-its-own-job-description": "adaptive-role",
    "2026-05-12-an-agents-map-stays-a-tree-for-400-steps": "graph-growth",
    "2026-05-20-an-agent-illustrates-its-report-from-its-sources":
        "image-generation",
    "2026-06-18-the-agent-that-audited-its-own-resume": "resume-audit",
    "2026-06-25-why-i-gave-an-ai-agent-nietzsche": "nietzsche",
    "2026-07-08-starting-values-are-an-axiom-not-a-fence": "self-overcoming",
    "2026-07-24-i-froze-my-analysis-before-scoring": "pre-registration",
    "2026-07-26-i-took-my-own-result-apart": "bin-packing-values",
    "2026-08-02-an-agent-wrote-itself-a-rule-against-lying":
        "values-rewriting",
    "2026-08-04-an-agent-tied-a-famous-benchmark-on-its-first-try":
        "circle-packing",
    "2026-08-05-i-told-an-agent-to-overfit-on-purpose": "overfit",
    "2026-08-06-agent-values-from-the-literature": "literature-values",
    "2026-08-07-i-ran-it-once-and-got-a-headline": "powered-replication",
    "2026-08-08-rewriting-values-helped-the-timid": "ale-bench",
}

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")


def move(src, dst):
    """git mv when the path is tracked, plain rename otherwise."""
    tracked = subprocess.run(["git", "ls-files", "--error-unmatch", src],
                             cwd=ROOT, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL).returncode == 0
    if tracked:
        subprocess.run(["git", "mv", src, dst], cwd=ROOT, check=True)
    else:
        os.rename(os.path.join(ROOT, src), os.path.join(ROOT, dst))


def figure_dirs(post_path):
    """Every img/blog/<dir> the post references."""
    s = open(post_path).read()
    return sorted({m.group(1) for m in
                   re.finditer(r"/img/blog/([^/\"]+)/", s)})


def main(check):
    posts_dir = os.path.join(ROOT, "_posts")
    post_renames, dir_renames = {}, {}

    for stem, new_slug in SLUGS.items():
        src = os.path.join(posts_dir, stem + ".md")
        if not os.path.exists(src):
            continue
        date, old_slug = DATE_RE.match(stem).groups()
        slug = new_slug or old_slug
        new_stem = "%s-%s" % (date, slug)
        if new_stem != stem:
            post_renames[stem] = new_stem
        for d in figure_dirs(src):
            if d != new_stem:
                dir_renames[d] = new_stem

    print("post renames: %d" % len(post_renames))
    for a, b in sorted(post_renames.items()):
        print("   %s\n-> %s" % (a, b))
    print("\nfigure dir renames: %d" % len(dir_renames))
    for a, b in sorted(dir_renames.items()):
        print("   img/blog/%-52s -> img/blog/%s" % (a, b))
    if check:
        return 0

    # 1. move the figure directories
    for old, new in dir_renames.items():
        move("img/blog/" + old, "img/blog/" + new)

    # 2. rewrite every reference, in posts and in the figure scripts
    targets = [os.path.join("_posts", f) for f in os.listdir(posts_dir)
               if f.endswith(".md")]
    for d in os.listdir(os.path.join(ROOT, "img", "blog")):
        p = os.path.join("img", "blog", d, "make_figs.py")
        if os.path.exists(os.path.join(ROOT, p)):
            targets.append(p)

    edits = 0
    for rel in targets:
        p = os.path.join(ROOT, rel)
        s = before = open(p).read()
        for old, new in dir_renames.items():
            s = s.replace("/img/blog/%s/" % old, "/img/blog/%s/" % new)
        for old, new in post_renames.items():
            s = s.replace("/blog/%s/" % DATE_RE.match(old).group(2),
                          "/blog/%s/" % DATE_RE.match(new).group(2))
        if s != before:
            open(p, "w").write(s)
            edits += 1

    # 3. move the posts last, so the rewrite above saw stable paths
    for old, new in post_renames.items():
        move("_posts/%s.md" % old, "_posts/%s.md" % new)

    print("\nrewrote references in %d files" % edits)
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
