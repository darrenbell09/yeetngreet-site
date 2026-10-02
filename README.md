# YeetnGreet site

Marketing pages for [yeetngreet.app](https://yeetngreet.app/) plus the customer **MkDocs Material** documentation published at [yeetngreet.app/docs/](https://yeetngreet.app/docs/).

## Layout

| Path | Role |
| --- | --- |
| `index.html`, `privacy.html`, `styles.css`, `CNAME` | Marketing homepage (keep intact) |
| `docs.html` | Short redirect → `/docs/` |
| `docs/` | MkDocs **source** (Markdown) |
| `mkdocs.yml`, `requirements.txt` | Docs site config |
| `.github/workflows/pages.yml` | Build marketing + docs → GitHub Pages |

## Local docs preview

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

Open the URL MkDocs prints (usually `http://127.0.0.1:8000/`). That preview is the docs site only; marketing HTML is separate static files at the repo root.

```bash
mkdocs build --site-dir site   # optional local build check
```

## GitHub Pages

Workflow **Deploy site and docs** assembles:

- Root: marketing files + `docs.html` redirect
- `/docs/`: MkDocs `site/` output

**One-time:** Repo **Settings → Pages → Source: GitHub Actions** (so the workflow can publish). Custom domain `yeetngreet.app` stays via `CNAME`.

Download the Windows app from [Releases](https://github.com/darrenbell09/yeetngreet-site/releases/latest).

## Screenshots

`docs/assets/images/*.png` are **placeholders**. Replace with real captures from a technician PC (app UI / `%LOCALAPPDATA%\YeetnGreet`) before calling the docs “final.”
