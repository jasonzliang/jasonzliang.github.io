# Jason Zhi Liang — Personal Website

Static personal/academic website inspired by the Hugo Blox Builder layout used at [vsonicv.github.io](https://vsonicv.github.io). Hand-written HTML/CSS — no build step required.

## Local preview

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

## Deploy (GitHub Pages)

This repo is configured to publish from the `main` branch root. After pushing, enable Pages in the repo's **Settings → Pages** (or via `gh`):

```bash
gh api -X POST "repos/$OWNER/$REPO/pages" -f source.branch=main -f source.path=/
```

## Structure

- `index.html` — landing page with hero, about, interests, education, featured publications
- `publications.html` — full publications and patents list
- `experience.html` — professional experience timeline
- `projects.html` — research projects and technical skills
- `css/style.css` — site-wide styling
