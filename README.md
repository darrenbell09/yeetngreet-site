# YeetnGreet site

Marketing pages for [yeetngreet.app](https://yeetngreet.app/) plus customer **MkDocs Material** docs at [yeetngreet.app/docs/](https://yeetngreet.app/docs/).

YeetnGreet is proprietary software.

## Layout

| Path | Role |
| --- | --- |
| `index.html`, `product.html`, `pricing.html`, `privacy.html`, `styles.css`, `CNAME` | Marketing (keep intact) |
| `robots.txt`, `sitemap.xml`, `sitemap-pages.xml` | Crawl hints (`sitemap.xml` indexes marketing + `/docs/sitemap.xml`) |
| `docsrc/` | MkDocs **source** (Markdown — edit here) |
| `docs/` | **Built** HTML published by GitHub Pages at `/docs/` |
| `mkdocs.yml`, `requirements.txt` | Docs config (`docs_dir: docsrc`) |
| `.github/workflows/pages.yml` | Rebuilds `docs/` on changes to `docsrc/` |

GitHub Pages is configured as **legacy**: branch `main`, folder `/` (root). That keeps the marketing homepage at `/` and serves the built site from the `docs/` directory at `/docs/`.

Do **not** add a root `docs.html`: on GitHub Pages, `/docs` would serve that file instead of redirecting into the `docs/` folder. Prefer links to `/docs/`.

## Favicons (Google Search)

Root icons are published with the marketing site:

| Path | Role |
| --- | --- |
| `favicon-96.png` | Square PNG ≥96px for Search / modern browsers (`rel=icon`) |
| `favicon-32.png` | Small PNG fallback |
| `favicon.ico` | Multi-size ICO fallback (16 / 32 / 48) |
| `apple-touch-icon.png` | 256px touch icon (also a valid Google `rel` value) |

Homepage `<head>` links use stable root-absolute URLs. `robots.txt` allows `/` so Googlebot / Googlebot-Image can crawl the page and icon files. Eligibility does not guarantee Search will show the icon; after merge, request homepage indexing in Search Console when ready.

## Local docs preview

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

Open the URL MkDocs prints (usually `http://127.0.0.1:8000/`).

```bash
mkdocs build --strict -d docs   # refresh published HTML locally
touch docs/.nojekyll
```

## Screenshots

`docsrc/assets/images/*.png` are **placeholders**. Replace with real captures from a technician PC (app UI / `%LOCALAPPDATA%\YeetnGreet`), then rebuild.

## Get early access

Public Windows downloads are not linked from this site yet. Join the [waitlist on the pricing page](https://yeetngreet.app/pricing.html). Plans are licensed-user bands from Free (1–25) through Enterprise (701+).
