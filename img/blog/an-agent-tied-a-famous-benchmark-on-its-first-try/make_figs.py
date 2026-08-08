"""Figure for "An agent tied a famous benchmark on its first try".

This one is not generated here. It is the writeup figure from the
circle-packing repo, fetched and re-encoded as WebP.

    gh api repos/jasonzliang/circle-packing-sota/contents/writeup/fig4_prev_vs_new.png \
        --jq .content | base64 -d > /tmp/f4.png

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks imports).
"""

import os
import subprocess

from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = "/tmp/f4.png"
REPO = "jasonzliang/circle-packing-sota"
PATH = "writeup/fig4_prev_vs_new.png"
MAX_W = 1600

if not os.path.exists(SRC):
    blob = subprocess.check_output(
        ["gh", "api", "repos/%s/contents/%s" % (REPO, PATH), "--jq", ".content"])
    import base64
    with open(SRC, "wb") as fh:
        fh.write(base64.b64decode(blob))

im = Image.open(SRC)
# flatten the alpha channel onto white rather than letting convert() blacken it
if im.mode in ("RGBA", "LA", "P"):
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    im = Image.alpha_composite(bg, im)
im = im.convert("RGB")

if im.width > MAX_W:
    im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)

out = os.path.join(OUT, "packing-old-vs-new.webp")
im.save(out, "WEBP", quality=88, method=6)
print("%s  %dx%d  (%.0f KB)" % (out, im.width, im.height,
                                os.path.getsize(out) / 1024.0))
