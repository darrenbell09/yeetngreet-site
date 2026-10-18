"""Render og/og-image.html to a 1200x630 PNG for link previews.

Run by .github/workflows/pages.yml after `mkdocs build`, so the PNG is
generated in CI instead of being committed by hand:

    python tools/render_og.py docs/assets/social/yeetngreet-og.png
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "og" / "og-image.html"


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/assets/social/yeetngreet-og.png")
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        page.goto(SRC.as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_function("Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)")
        page.screenshot(path=str(out), clip={"x": 0, "y": 0, "width": 1200, "height": 630})
        browser.close()
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
