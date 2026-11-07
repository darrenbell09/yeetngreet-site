"""Technical SEO crawlability and metadata conventions for the marketing site."""

from __future__ import annotations

import json
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class _HeadCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.canonical = ""
        self.description = ""
        self.robots = ""
        self.jsonld: list[str] = []
        self._in_ld = False
        self._ld_buf: list[str] = []
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        if tag == "link" and data.get("rel") == "canonical":
            self.canonical = data.get("href", "")
        if tag == "meta" and data.get("name") == "description":
            self.description = data.get("content", "")
        if tag == "meta" and data.get("name") == "robots":
            self.robots = data.get("content", "")
        if tag == "script" and data.get("type") == "application/ld+json":
            self._in_ld = True
            self._ld_buf = []
        if tag == "a" and data.get("href"):
            self.hrefs.append(data["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_ld:
            self.jsonld.append("".join(self._ld_buf))
            self._in_ld = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._in_ld:
            self._ld_buf.append(data)


def parse_head(html: str) -> _HeadCollector:
    parser = _HeadCollector()
    parser.feed(html)
    return parser


class TechnicalSeoTests(unittest.TestCase):
    def test_docs_html_stub_removed_to_avoid_pages_collision(self) -> None:
        # GitHub Pages serves docs.html at /docs, shadowing the docs/ directory redirect.
        self.assertFalse((ROOT / "docs.html").exists())
        self.assertTrue((ROOT / "docs" / "index.html").is_file())

    def test_robots_allows_crawl_and_points_at_sitemap_index(self) -> None:
        robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("User-agent: *", robots)
        self.assertIn("Allow: /", robots)
        self.assertIn("Sitemap: https://yeetngreet.app/sitemap.xml", robots)
        self.assertNotRegex(robots, r"(?i)disallow:\s*/docs")

    def test_sitemap_index_and_marketing_urls(self) -> None:
        index = ET.parse(ROOT / "sitemap.xml").getroot()
        locs = [el.text for el in index.findall("sm:sitemap/sm:loc", NS)]
        self.assertEqual(
            locs,
            [
                "https://yeetngreet.app/sitemap-pages.xml",
                "https://yeetngreet.app/docs/sitemap.xml",
            ],
        )
        pages = ET.parse(ROOT / "sitemap-pages.xml").getroot()
        page_locs = [el.text for el in pages.findall("sm:url/sm:loc", NS)]
        self.assertEqual(
            page_locs,
            [
                "https://yeetngreet.app/",
                "https://yeetngreet.app/product.html",
                "https://yeetngreet.app/pricing.html",
                "https://yeetngreet.app/privacy.html",
                "https://yeetngreet.app/terms.html",
                "https://yeetngreet.app/refunds.html",
            ],
        )
        # Thin redirect shells and utility pages stay out of the marketing sitemap.
        joined = "\n".join(page_locs)
        self.assertNotIn("docs.html", joined)
        self.assertNotIn("/go/", joined)
        self.assertNotIn("404.html", joined)
        self.assertNotIn("index.html", joined)

        docs = ET.parse(ROOT / "docs" / "sitemap.xml").getroot()
        docs_locs = [el.text for el in docs.findall("sm:url/sm:loc", NS)]
        self.assertIn("https://yeetngreet.app/docs/", docs_locs)
        self.assertTrue(any(loc and loc.startswith("https://yeetngreet.app/docs/") for loc in docs_locs))

    def test_marketing_pages_have_absolute_canonical_and_description(self) -> None:
        expected = {
            "index.html": "https://yeetngreet.app/",
            "product.html": "https://yeetngreet.app/product.html",
            "pricing.html": "https://yeetngreet.app/pricing.html",
            "privacy.html": "https://yeetngreet.app/privacy.html",
            "terms.html": "https://yeetngreet.app/terms.html",
            "refunds.html": "https://yeetngreet.app/refunds.html",
        }
        for rel, canonical in expected.items():
            head = parse_head((ROOT / rel).read_text(encoding="utf-8"))
            self.assertEqual(head.canonical, canonical, rel)
            self.assertTrue(head.title.strip(), rel)
            self.assertGreaterEqual(len(head.description.strip()), 40, rel)
            self.assertNotIn("noindex", head.robots.lower())

    def test_internal_brand_links_prefer_canonical_home(self) -> None:
        for rel in (
            "index.html",
            "product.html",
            "pricing.html",
            "privacy.html",
            "terms.html",
            "refunds.html",
        ):
            html = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn('href="index.html"', html, rel)
            self.assertIn('href="/"', html, rel)

    def test_homepage_organization_jsonld_uses_verified_facts_only(self) -> None:
        head = parse_head((ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(len(head.jsonld), 1)
        data = json.loads(head.jsonld[0])
        graph = {node["@type"]: node for node in data["@graph"]}
        org = graph["Organization"]
        site = graph["WebSite"]
        self.assertEqual(org["name"], "YeetnGreet")
        self.assertEqual(org["legalName"], "YeetnGreet LLC")
        self.assertEqual(org["url"], "https://yeetngreet.app/")
        self.assertEqual(org["email"], "support@yeetngreet.app")
        self.assertEqual(org["logo"], "https://yeetngreet.app/favicon-96.png")
        self.assertEqual(org["contactPoint"]["email"], "support@yeetngreet.app")
        self.assertEqual(site["url"], "https://yeetngreet.app/")
        # Do not invent ratings, reviews, offers, or unsupported product claims.
        blob = json.dumps(data)
        for banned in (
            "aggregateRating",
            "review",
            "offers",
            "SoftwareApplication",
            "MSP",
            "open source",
            "sameAs",
        ):
            self.assertNotIn(banned, blob)

    def test_utility_shells_stay_noindex(self) -> None:
        for rel in ("404.html", "go/waitlist/index.html", "go/founding/index.html"):
            head = parse_head((ROOT / rel).read_text(encoding="utf-8"))
            self.assertIn("noindex", head.robots.lower(), rel)

    def test_key_docs_have_page_specific_descriptions(self) -> None:
        samples = {
            "docsrc/support.md": "support@yeetngreet.app",
            "docsrc/getting-started/install.md": "YeetnGreet-Setup.exe",
            "docsrc/jobs/offboard.md": "Offboard",
            "docsrc/pricing-and-licensing.md": "licensed users",
            "docs/support/index.html": "support@yeetngreet.app",
            "docs/getting-started/install/index.html": "YeetnGreet-Setup.exe",
        }
        for rel, needle in samples.items():
            text = (ROOT / rel).read_text(encoding="utf-8")
            if rel.endswith(".md"):
                self.assertRegex(text, rf"description:.*{re.escape(needle)}")
            else:
                head = parse_head(text)
                self.assertIn(needle, head.description, rel)
                # Must not still be the generic site_description only.
                self.assertNotEqual(
                    head.description,
                    "Onboard and offboard Microsoft 365 for IT admins — from your technicians' PCs.",
                    rel,
                )

    def test_product_and_pricing_titles_include_brand_and_topic(self) -> None:
        product = parse_head((ROOT / "product.html").read_text(encoding="utf-8"))
        pricing = parse_head((ROOT / "pricing.html").read_text(encoding="utf-8"))
        self.assertIn("YeetnGreet", product.title)
        self.assertIn("onboarding", product.title.lower())
        self.assertIn("YeetnGreet", pricing.title)
        self.assertIn("licensed users", pricing.title.lower())

    def test_customer_terminology_guardrails_on_structured_surfaces(self) -> None:
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        product = (ROOT / "product.html").read_text(encoding="utf-8")
        pricing = (ROOT / "pricing.html").read_text(encoding="utf-8")
        for html in (home, product, pricing):
            lower = html.lower()
            self.assertNotRegex(lower, r"\bmsp\b")
            self.assertNotIn("open source", lower)
        self.assertIn("admin", home.lower())
        self.assertIn("admin", product.lower())
        self.assertIn("licensed users", home.lower())
        self.assertIn("licensed users", pricing.lower())
        self.assertIn("14-day trial", home)
        self.assertIn("Free", pricing)


if __name__ == "__main__":
    unittest.main()
