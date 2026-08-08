"""Figure for "Why I gave an AI agent Nietzsche".

Not generated here: this is the abelian-sandpile identity the agent itself
produced during a self-improvement run. Copied and re-encoded as WebP.

The source is 256x256 flat-colour pixel art, so it is upscaled with
nearest-neighbour (keeping every cell crisp rather than smearing the fractal)
and saved losslessly, which is both sharper and smaller than lossy WebP for
an image with four colours.

Run from any directory EXCEPT /tmp (a stray /tmp/six.py shadows the real
`six` package and breaks imports).
"""

import os

from PIL import Image

OUT = os.path.dirname(os.path.abspath(__file__))
SRC = ("/Users/jason/Desktop/science_moonshot/self_improvement_v1/result/"
       "20260616-2346_original_30i_30m/artifacts/"
       "iter44-2026-06-17-abelian-sandpile/identity.png")
SCALE = 3

im = Image.open(SRC).convert("RGB")
im = im.resize((im.width * SCALE, im.height * SCALE), Image.NEAREST)

out = os.path.join(OUT, "sandpile.webp")
im.save(out, "WEBP", lossless=True, quality=100, method=6)
print("%s  %dx%d  (%.0f KB)" % (out, im.width, im.height,
                                os.path.getsize(out) / 1024.0))
