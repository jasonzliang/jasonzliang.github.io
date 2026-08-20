"""Regenerate favicon.ico from favicon.svg.

The site ships two icons and no more:

  favicon.svg  the real one. Scales to any size, ~600 bytes. Linked from every
               <head>. The monogram is pinned to ~78% of the box with
               textLength, so which fallback font renders it cannot change the
               layout -- a naturally-set "JL" is narrower and turns to mush at
               16px, the size a browser tab actually uses.
  favicon.ico  fallback only. Browsers request /favicon.ico whether or not it
               is linked, so omitting it means a 404 on every visit. Contains
               16/32/48, which is why no separate PNGs are needed.

Dropped deliberately: favicon-16x16.png and favicon-32x32.png (both duplicated
sizes already inside the .ico) and apple-touch-icon.png (iOS home-screen
bookmarks only).

    python3 _scripts/make_favicon.py     # rewrites favicon.ico from the SVG

Needs rsvg-convert (brew install librsvg). Edit favicon.svg by hand; this
script only rasterises it.
"""
import io
import subprocess
import sys

from PIL import Image

SVG = "favicon.svg"
ICO = "favicon.ico"
SIZES = [16, 32, 48]


def render(px):
    out = subprocess.run(
        ["rsvg-convert", "-w", str(px), "-h", str(px), SVG],
        capture_output=True, check=True,
    )
    return Image.open(io.BytesIO(out.stdout)).convert("RGBA")


def main():
    try:
        frames = [render(px) for px in SIZES]
    except FileNotFoundError:
        sys.exit("rsvg-convert not found: brew install librsvg")
    # Pillow builds the other sizes off the first image, so hand it the
    # largest and let sizes= carry the rest.
    frames[-1].save(ICO, sizes=[(px, px) for px in SIZES])
    print("wrote %s from %s at %s" % (ICO, SVG, SIZES))


if __name__ == "__main__":
    main()
