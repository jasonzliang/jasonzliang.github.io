#!/usr/bin/env python3
"""Reflow Markdown prose to an 80-column width without changing what renders.

Left alone, because rewrapping them would change the output or break parsing:
  - YAML front matter
  - fenced code blocks
  - table rows and any line beginning with `|`
  - headings, horizontal rules, and link-reference definitions
  - any single word longer than the column budget (long URLs)

Reflowed, each with the right hanging indent:
  - paragraphs
  - blockquotes (one `> ` level)
  - list items, ordered and unordered
  - `{% include %}` tags, split one parameter per line

Usage:  python3 _scripts/reflow.py _posts/*.md
        python3 _scripts/reflow.py --check _posts/*.md
"""

import re
import sys
import textwrap

WIDTH = 80

FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
HR = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
TABLE = re.compile(r"^\s*\|")
LINKDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s")
QUOTE = re.compile(r"^(\s{0,3}>\s?)(.*)$")
BULLET = re.compile(r"^(\s*)([-*+]|\d+[.)])(\s+)(.*)$")
INDENTED_CODE = re.compile(r"^(\s{4,})\S")
LIQUID_OPEN = re.compile(r"^\s*\{%")
INCLUDE_PARAM = re.compile(r'([\w-]+)\s*=\s*("(?:[^"\\]|\\.)*"|\S+)')


def wrap(text, width, initial="", subsequent=""):
    """Wrap, but never split a word: an over-long URL keeps its own line."""
    return textwrap.wrap(
        text, width=width, initial_indent=initial,
        subsequent_indent=subsequent, break_long_words=False,
        break_on_hyphens=False) or [initial.rstrip()]


def wrap_include(line):
    """`{% include a.html x="1" y="2" %}` -> one parameter per line.

    Long values wrap inside their quotes. The newline and indent become
    ordinary whitespace in the attribute, which HTML collapses, so what
    renders is unchanged.
    """
    m = re.match(r"^(\s*)\{%-?\s*(\w+)\s+(\S+)\s*(.*?)\s*-?%\}\s*$", line)
    if not m:
        return [line]
    indent, tag, target, rest = m.groups()
    params = INCLUDE_PARAM.findall(rest)
    if not params or len(line) <= WIDTH:
        return [line]

    out = ["%s{%% %s %s" % (indent, tag, target)]
    for key, raw in params:
        head = "%s   %s=" % (indent, key)
        if not raw.startswith('"') or len(head) + len(raw) <= WIDTH:
            out.append(head + raw)
            continue
        pad = " " * (len(head) + 1)
        # one column held back for the closing quote
        pieces = wrap(raw[1:-1], WIDTH - len(pad) - 1)
        out.append(head + '"' + pieces[0])
        out.extend(pad + p for p in pieces[1:-1])
        out.append(pad + pieces[-1] + '"' if len(pieces) > 1 else out.pop() + '"')
    out.append("%s%%}" % indent)
    return out


def reflow(text):
    lines = text.split("\n")
    out = []
    i = 0

    # Front matter. Long single-line scalars become YAML folded blocks, which
    # parse to exactly the same string; everything else is left alone.
    if lines and lines[0].strip() == "---":
        out.append(lines[0])
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            fm = re.match(r'^(\w+):\s+"?(.*?)"?\s*$', lines[i])
            if len(lines[i]) > WIDTH and fm and "[" not in fm.group(2):
                key, value = fm.groups()
                out.append("%s: >-" % key)
                out.extend(wrap(value, WIDTH, "  ", "  "))
            else:
                out.append(lines[i])
            i += 1
        if i < len(lines):
            out.append(lines[i])
            i += 1

    in_fence = False
    para = []
    para_kind = None  # (kind, initial_indent, subsequent_indent)

    def flush():
        nonlocal para_kind
        if not para:
            para_kind = None
            return
        kind, initial, subsequent = para_kind
        body = " ".join(s.strip() for s in para).strip()
        if kind == "quote":
            budget = WIDTH - len(initial)
            for j, w in enumerate(wrap(body, budget)):
                out.append((initial if j == 0 else subsequent) + w)
        else:
            out.extend(wrap(body, WIDTH, initial, subsequent))
        del para[:]
        para_kind = None

    while i < len(lines):
        line = lines[i]

        if FENCE.match(line):
            flush()
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue

        if not line.strip():
            flush()
            out.append("")
            i += 1
            continue

        if (HEADING.match(line) or HR.match(line) or TABLE.match(line)
                or LINKDEF.match(line) or INDENTED_CODE.match(line)):
            flush()
            out.append(line)
            i += 1
            continue

        if LIQUID_OPEN.match(line):
            flush()
            # A tag already split across lines is joined back up first, so
            # running this script twice is the same as running it once.
            j = i
            while j < len(lines) and "%}" not in lines[j]:
                j += 1
            joined = " ".join(l.strip() for l in lines[i:j + 1])
            out.extend(wrap_include(re.match(r"^(\s*)", line).group(1) + joined))
            i = j + 1
            continue

        if QUOTE.match(line):
            flush()
            # Take the whole quote block at once. Rewrapping is only safe when
            # it is plain prose: a quote containing its own list or code would
            # be flattened, so those pass through verbatim.
            j = i
            chunk = []
            while j < len(lines) and QUOTE.match(lines[j]):
                chunk.append(lines[j])
                j += 1
            bodies = [QUOTE.match(c).group(2) for c in chunk]
            reflowable = not any(BULLET.match(b) or b.startswith("    ")
                                 or FENCE.match(b) or TABLE.match(b)
                                 for b in bodies)
            if not reflowable:
                out.extend(chunk)
            else:
                # split into paragraphs on the blank `>` lines
                group = []
                for b in bodies + [""]:
                    if b.strip():
                        group.append(b.strip())
                        continue
                    if group:
                        for w in wrap(" ".join(group), WIDTH - 2):
                            out.append("> " + w)
                        group = []
                        out.append(">")
                if out and out[-1] == ">":
                    out.pop()
            i = j
            continue

        mb = BULLET.match(line)
        if mb:
            flush()
            indent, bullet, gap, rest = mb.groups()
            initial = indent + bullet + gap
            para_kind = ("list", initial, " " * len(initial))
            para.append(rest)
            i += 1
            continue

        if para_kind and para_kind[0] in ("list", "quote"):
            para.append(line)                 # continuation of the same item
            i += 1
            continue

        if not para:
            para_kind = ("para", "", "")
        para.append(line)
        i += 1

    flush()
    return "\n".join(out)


def split_front_matter(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return "", text
    for n in range(1, len(lines)):
        if lines[n].strip() == "---":
            return "\n".join(lines[1:n]), "\n".join(lines[n + 1:])
    return "", text


def front_matter_pairs(block):
    """key -> value, resolving YAML folded (`>-`) scalars back to one string."""
    pairs, key, buf = {}, None, []
    for line in block.split("\n"):
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m and not line.startswith(" "):
            if key:
                pairs[key] = " ".join(buf).strip()
            key, first = m.group(1), m.group(2).strip()
            buf = [] if first in (">-", ">", "|", "|-") else [first]
        elif key:
            buf.append(line.strip())
    if key:
        pairs[key] = " ".join(buf).strip()
    return {k: v.strip('"').strip("'") for k, v in pairs.items()}


def words(text):
    """Everything that affects rendering, with line breaks normalised away.

    Leading blockquote markers go too: rewrapping a quote moves them to
    different lines without changing a word of what is quoted.
    """
    text = re.sub(r"(?m)^\s{0,3}>\s?", "", text)
    return re.sub(r"[ \t\n]+", " ", text).strip()


def equivalent(before, after):
    fb, bb = split_front_matter(before)
    fa, ba = split_front_matter(after)
    return (words(bb) == words(ba)
            and front_matter_pairs(fb) == front_matter_pairs(fa))


def main(argv):
    check = "--check" in argv
    paths = [a for a in argv if not a.startswith("--")]
    bad = 0
    for path in paths:
        with open(path) as fh:
            before = fh.read()
        after = reflow(before)
        if not equivalent(before, after):
            print("REFUSED (content would change): %s" % path)
            bad += 1
            continue
        over = [n for n, l in enumerate(after.split("\n"), 1) if len(l) > WIDTH]
        if check:
            print("%s  %s  long lines: %s"
                  % ("OK " if before == after else "WOULD REWRAP", path,
                     over or "none"))
            continue
        if before != after:
            with open(path, "w") as fh:
                fh.write(after)
        print("%s  long lines remaining: %s" % (path, over or "none"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
