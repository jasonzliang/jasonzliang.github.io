"""Figures for the 2026-08-10 packing-records post.

sweep.webp is not generated here. It is Figure 1 of

  <research-repo>/self_improvement_v2/reports/circle-packing/
      2026-08-10_circle-packing_sota-comparison_report.pdf

extracted from the PDF rather than replotted, because the per-N sweep data
behind it (92 sizes) lives in the companion repo's comparison.md and not in
this repository. The 21 win values in the post come from that report's
Table 1.

  pdftoppm -r 400 -png -f 3 -l 3 <report>.pdf p3
  # crop to the axes plus the plot title, excluding the LaTeX caption below
  from PIL import Image
  im = Image.open("p3-3.png").crop((250, 380, 3250, 1590))
  im = im.resize((1600, round(1600 * im.height / im.width)), Image.LANCZOS)
  im.convert("RGB").save("sweep.webp", "WEBP", quality=88, method=6)
"""


# The extracted report uses a first-person subscript on its vertical axis.
# Apply these label-only corrections after extracting sweep.webp. Both boxes
# lie outside the plot and its tick labels; other pixels are preserved.
AXIS_LABEL_BOX = (160, 205, 197, 401)
REFERENCE_TITLE_BOX = (300, 30, 1390, 71)


def correct_sweep_labels(image_path):
    import io

    from matplotlib.font_manager import FontProperties, findfont
    from matplotlib.mathtext import math_to_image
    from PIL import Image, ImageDraw, ImageFont

    image = Image.open(image_path).convert("RGB")
    if image.size != (1600, 645):
        raise ValueError("Expected the documented 1600 x 645 sweep crop")
    buffer = io.BytesIO()
    math_to_image(
        r"$\Sigma r_{\mathrm{solver}} - \Sigma r_{\mathrm{record}}$",
        buffer, prop=FontProperties(size=10), dpi=144, format="png",
        color="#202020",
    )
    label = Image.open(buffer).convert("RGBA").rotate(90, expand=True)
    image.paste("white", AXIS_LABEL_BOX)
    image.paste(label, (165, 303 - label.height // 2), label)
    image.paste("white", REFERENCE_TITLE_BOX)
    title = "Updated solver vs 10 Aug 2026 Packomania csqv records (N=2..93)"
    font = ImageFont.truetype(findfont(FontProperties(family="DejaVu Sans")), 30)
    draw = ImageDraw.Draw(image)
    width = draw.textlength(title, font=font)
    draw.text((841 - width / 2, 33), title, font=font, fill="#000000")
    # Lossless encoding keeps the decoded plot pixels unchanged.
    image.save(image_path, "WEBP", lossless=True, method=6)


if __name__ == "__main__":
    from pathlib import Path

    correct_sweep_labels(Path(__file__).with_name("sweep.webp"))
