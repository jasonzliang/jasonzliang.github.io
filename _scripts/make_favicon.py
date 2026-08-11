"""Generate the site favicon set.

A "JL" monogram, white on the site accent blue (--color-accent, #1d4ed8),
on a rounded square. Rendered at 512px and downsampled so the glyph edges
stay clean at 16px, where a favicon actually lives -- the monogram is set
wide (80% of the box) because a tighter 'JL' turns to mush at that size.

    python3 _scripts/make_favicon.py

Writes favicon.ico (16/32/48), favicon-16x16.png, favicon-32x32.png and
apple-touch-icon.png (180, squared off -- iOS applies its own mask).
"""
from PIL import Image, ImageDraw, ImageFont

ACCENT = (29, 78, 216)          # #1d4ed8, matches --color-accent in css/style.css
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
S = 512                          # master size; everything downsamples from here


def master(radius_frac=0.18, pad_frac=0.0):
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = int(S * pad_frac)
    d.rounded_rectangle([pad, pad, S - 1 - pad, S - 1 - pad],
                        radius=int(S * radius_frac), fill=ACCENT + (255,))
    # size the monogram to the box rather than trusting a point size
    for pt in range(int(S * 0.95), 10, -4):
        f = ImageFont.truetype(FONT, pt)
        l, t, r, b = d.textbbox((0, 0), "JL", font=f)
        if (r - l) <= S * 0.80 and (b - t) <= S * 0.62:
            break
    l, t, r, b = d.textbbox((0, 0), "JL", font=f)
    d.text(((S - (r - l)) / 2 - l, (S - (b - t)) / 2 - t), "JL",
           font=f, fill=(255, 255, 255, 255))
    return img


def main():
    m = master()
    for px in (16, 32):
        m.resize((px, px), Image.LANCZOS).save("favicon-%dx%d.png" % (px, px))
    m.save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    # iOS masks the corners itself, so ship a full-bleed square
    master(radius_frac=0.0).resize((180, 180), Image.LANCZOS)\
        .convert("RGB").save("apple-touch-icon.png")


if __name__ == "__main__":
    main()
