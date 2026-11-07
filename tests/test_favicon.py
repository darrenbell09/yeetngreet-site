"""Favicon assets and homepage head links meet Google Search crawlability conventions."""

from __future__ import annotations

import pathlib
import re
import struct
import unittest
from html.parser import HTMLParser


ROOT = pathlib.Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
ROBOTS = (ROOT / "robots.txt").read_text(encoding="utf-8")
CACHE_BUST = "20261107a"

# Marketing + redirect/go shells that must advertise the same root icons.
HEAD_PAGES = (
    "index.html",
    "product.html",
    "pricing.html",
    "privacy.html",
    "terms.html",
    "refunds.html",
    "404.html",
    "go/founding/index.html",
    "go/waitlist/index.html",
    "overrides/main.html",
    "docs/index.html",
)


def png_dimensions(path: pathlib.Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path.name}: not a PNG signature")
    length = struct.unpack_from(">I", data, 8)[0]
    chunk = data[12:16]
    if chunk != b"IHDR" or length < 8:
        raise AssertionError(f"{path.name}: missing IHDR")
    width, height = struct.unpack_from(">II", data, 16)
    return width, height


def ico_dimensions(path: pathlib.Path) -> list[tuple[int, int]]:
    data = path.read_bytes()
    reserved, image_type, count = struct.unpack_from("<HHH", data, 0)
    if reserved != 0 or image_type != 1 or count < 1:
        raise AssertionError(f"{path.name}: invalid ICO header")
    sizes: list[tuple[int, int]] = []
    for i in range(count):
        offset = 6 + i * 16
        width_b, height_b = struct.unpack_from("<BB", data, offset)
        sizes.append((width_b or 256, height_b or 256))
    return sizes


class _IconLinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.icons: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "link":
            return
        data = {k: (v or "") for k, v in attrs}
        rel = data.get("rel", "").lower()
        if rel in {"icon", "shortcut icon", "apple-touch-icon", "apple-touch-icon-precomposed"}:
            self.icons.append(data)


def collect_icons(html: str) -> list[dict[str, str]]:
    parser = _IconLinkCollector()
    parser.feed(html)
    return parser.icons


class FaviconTests(unittest.TestCase):
    def test_png_assets_are_square_and_sized(self) -> None:
        w32, h32 = png_dimensions(ROOT / "favicon-32.png")
        self.assertEqual((w32, h32), (32, 32))

        w96, h96 = png_dimensions(ROOT / "favicon-96.png")
        self.assertEqual((w96, h96), (96, 96))
        # Google recommends larger than 48x48 for Search surfaces.
        self.assertGreater(w96, 48)

        w_ati, h_ati = png_dimensions(ROOT / "apple-touch-icon.png")
        self.assertEqual(w_ati, h_ati)
        self.assertGreaterEqual(w_ati, 96)

        # MkDocs theme favicon copy should also be the 96px brand mark.
        for rel in (
            "docsrc/assets/images/favicon.png",
            "docs/assets/images/favicon.png",
        ):
            w, h = png_dimensions(ROOT / rel)
            self.assertEqual((w, h), (96, 96), rel)

    def test_ico_fallback_includes_usable_sizes(self) -> None:
        sizes = ico_dimensions(ROOT / "favicon.ico")
        self.assertIn((16, 16), sizes)
        self.assertIn((32, 32), sizes)
        self.assertIn((48, 48), sizes)
        self.assertTrue(all(w == h for w, h in sizes))

    def test_homepage_head_references_crawlable_icons(self) -> None:
        icons = collect_icons(INDEX)
        hrefs = [i.get("href", "") for i in icons]
        self.assertTrue(
            any(h.startswith("/favicon.ico?") and CACHE_BUST in h for h in hrefs),
            hrefs,
        )
        self.assertTrue(
            any(
                h.startswith("/favicon-96.png?")
                and CACHE_BUST in h
                and i.get("type") == "image/png"
                and i.get("sizes") == "96x96"
                for i, h in zip(icons, hrefs)
            ),
            icons,
        )
        self.assertTrue(
            any(h.startswith("/favicon-32.png?") and CACHE_BUST in h for h in hrefs),
            hrefs,
        )
        self.assertTrue(
            any(
                i.get("rel") == "apple-touch-icon"
                and i.get("href", "").startswith("/apple-touch-icon.png?")
                for i in icons
            ),
            icons,
        )
        # Absolute root paths so crawlers resolve icons from any page URL.
        for href in hrefs:
            self.assertTrue(href.startswith("/"), href)
            self.assertFalse(href.startswith("//"), href)

    def test_marketing_and_docs_shells_share_icon_links(self) -> None:
        required = (
            f'/favicon.ico?v={CACHE_BUST}',
            f'/favicon-96.png?v={CACHE_BUST}',
            f'/favicon-32.png?v={CACHE_BUST}',
            f'/apple-touch-icon.png?v={CACHE_BUST}',
        )
        for rel in HEAD_PAGES:
            html = (ROOT / rel).read_text(encoding="utf-8")
            for needle in required:
                self.assertIn(needle, html, rel)

    def test_robots_allows_homepage_and_icons(self) -> None:
        # Googlebot must crawl the homepage; Googlebot-Image must crawl favicon URLs.
        self.assertIn("User-agent: *", ROBOTS)
        self.assertIn("Allow: /", ROBOTS)
        self.assertNotRegex(ROBOTS, r"(?i)disallow:\s*/favicon")
        self.assertNotRegex(ROBOTS, r"(?i)disallow:\s*/$")
        self.assertNotRegex(ROBOTS, r"(?i)disallow:\s*/\*")

    def test_icon_files_exist_at_stable_root_paths(self) -> None:
        for name in (
            "favicon.ico",
            "favicon-96.png",
            "favicon-32.png",
            "apple-touch-icon.png",
        ):
            path = ROOT / name
            self.assertTrue(path.is_file(), name)
            self.assertGreater(path.stat().st_size, 64, name)


if __name__ == "__main__":
    unittest.main()
