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
