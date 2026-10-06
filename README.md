# YeetnGreet site

Marketing pages for [yeetngreet.app](https://yeetngreet.app/) plus customer **MkDocs Material** docs at [yeetngreet.app/docs/](https://yeetngreet.app/docs/).

## Layout

| Path | Role |
| --- | --- |
| `index.html`, `privacy.html`, `styles.css`, `CNAME` | Marketing (keep intact) |
| `docs.html` | Redirect → `/docs/` |
| `docsrc/` | MkDocs **source** (Markdown — edit here) |
| `docs/` | **Built** HTML published by GitHub Pages at `/docs/` |
| `mkdocs.yml`, `requirements.txt` | Docs config (`docs_dir: docsrc`) |
| `.github/workflows/pages.yml` | Rebuilds `docs/` on changes to `docsrc/` |

GitHub Pages is configured as **legacy**: branch `main`, folder `/` (root). That keeps the marketing homepage at `/` and serves the built site from the `docs/` directory at `/docs/`.

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

Public Windows downloads are not linked from this site yet. Founding beta interest is collected on the [homepage founding form](https://yeetngreet.app/#founding) ($349/yr · 10 slots · 5 tenants).
