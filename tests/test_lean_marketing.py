"""Lean home + product marketing pages keep live chrome and approved copy."""

from __future__ import annotations

import pathlib
import re
import unittest
from html.parser import HTMLParser


ROOT = pathlib.Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
PRODUCT = (ROOT / "product.html").read_text(encoding="utf-8")
STYLES = (ROOT / "styles.css").read_text(encoding="utf-8")


class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.h1s: list[str] = []
        self.h2s: list[str] = []
        self._heading: list[str] | None = None
        self.nav_hrefs: list[str] = []
        self.footer_hrefs: list[str] = []
        self._in_nav = False
        self._in_footer = False
        self.scripts: list[str] = []
        self.stylesheets: list[str] = []
        self.has_nav_toggle = False
        self.nav_toggle_attrs: dict[str, str] = {}
        self.has_theme_toggle = False
        self.has_site_nav = False
        self.text_chunks: list[str] = []
        self.cta_labels: list[str] = []
        self._in_cta = False
        self._cta_buf: list[str] = []
        self.ids: set[str] = set()
        self.shot_srcs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: (v or "") for k, v in attrs}
        if tag == "title":
            self._in_title = True
        if tag in {"h1", "h2"}:
            self._heading = []
        if tag == "nav" and data.get("id") == "site-nav":
            self._in_nav = True
            self.has_site_nav = True
        if tag == "footer":
            self._in_footer = True
        if tag == "a" and "href" in data:
            href = data["href"]
            if self._in_nav:
                self.nav_hrefs.append(href)
            if self._in_footer:
                self.footer_hrefs.append(href)
            if "btn" in data.get("class", ""):
                self._in_cta = True
                self._cta_buf = []
        if tag == "button" and "nav-toggle" in data.get("class", ""):
            self.has_nav_toggle = True
            self.nav_toggle_attrs = data
        if tag == "button" and "theme-toggle" in data.get("class", ""):
            self.has_theme_toggle = True
        if tag == "script" and data.get("src"):
            self.scripts.append(data["src"])
        if tag == "link" and data.get("rel") == "stylesheet" and data.get("href"):
            self.stylesheets.append(data["href"])
        if data.get("id"):
            self.ids.add(data["id"])
        if tag == "img" and data.get("src"):
            self.shot_srcs.append(data["src"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag in {"h1", "h2"} and self._heading is not None:
            text = _norm("".join(self._heading))
            if tag == "h1":
                self.h1s.append(text)
            else:
                self.h2s.append(text)
            self._heading = None
        if tag == "nav":
            self._in_nav = False
        if tag == "footer":
            self._in_footer = False
        if tag == "a" and self._in_cta:
            self.cta_labels.append(_norm("".join(self._cta_buf)))
            self._in_cta = False
            self._cta_buf = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._heading is not None:
            self._heading.append(data)
        if self._in_cta:
            self._cta_buf.append(data)
        stripped = data.strip()
        if stripped:
            self.text_chunks.append(stripped)

    def visible_text(self) -> str:
        return " ".join(self.text_chunks)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse(html: str) -> _Collector:
    parser = _Collector()
    parser.feed(html)
    return parser


def live_plan_prices() -> list[str]:
    return re.findall(r"\$(?:0|19|49|99|149|249)", PRICING)


class LeanMarketingTests(unittest.TestCase):
    def test_home_hero_copy_is_exact(self) -> None:
        home = parse(INDEX)
        self.assertEqual(home.h1s, ["Onboard. Offboard. Stop wasting licenses."])
        text = home.visible_text()
        self.assertIn("Now in prerelease · 14-day trial on paid plans", text)
        self.assertIn(
            "YeetnGreet runs joiners and leavers from Admin templates.",
            text,
        )
        self.assertIn("Request founding beta", home.cta_labels)
        self.assertIn("See pricing", home.cta_labels)

    def test_home_has_lean_sections_only(self) -> None:
        home = parse(INDEX)
        self.assertIn("Where Microsoft 365 lifecycle breaks", home.h2s)
        self.assertIn("Admins set the policy. Technicians run it.", home.h2s)
        self.assertIn("Reclaim license spend", home.h2s)
        self.assertIn("IT teams running cloud Microsoft 365 / Entra.", home.h2s)
        self.assertIn("Plans by licensed users pooled across your account.", home.h2s)
        self.assertIn("why", home.ids)
        text = home.visible_text()
        self.assertIn("Offboarding skips policy", text)
        self.assertIn("Admin builds the template", text)
        self.assertIn("Northshore Logistics", text)
        self.assertIn("See the workflows", text)
        self.assertNotIn("Where user lifecycle goes wrong", text)
        self.assertNotIn("Price a plan before you buy.", text)
        self.assertNotIn("Users needing attention", text)
        self.assertNotIn("Est. spend", text)
        self.assertNotIn("Join the pre-release waitlist", text)

    def test_product_page_has_workflow_sections(self) -> None:
        product = parse(PRODUCT)
        self.assertEqual(product.h1s, ["How YeetnGreet runs the job"])
        self.assertIn("Same onboarding, every time.", product.h2s)
        self.assertIn("Technicians can’t change the steps.", product.h2s)
        self.assertIn("Offboard with a checklist.", product.h2s)
        self.assertIn("Price a plan before you buy.", product.h2s)
        self.assertIn("docs/assets/images/onboard-create-user.png", product.shot_srcs)
        self.assertIn("docs/assets/images/rbac-tech-templates.png", product.shot_srcs)
        self.assertIn("docs/assets/images/offboard-select-users.png", product.shot_srcs)
        self.assertIn("assets/app/hero-whatif.png", product.shot_srcs)
        for path in product.shot_srcs:
            self.assertTrue((ROOT / path).is_file(), f"missing shot {path}")

    def test_live_chrome_stays_on_home_and_product(self) -> None:
        for name, html in (("index", INDEX), ("product", PRODUCT)):
            page = parse(html)
            self.assertTrue(page.has_nav_toggle, name)
            self.assertEqual(page.nav_toggle_attrs.get("aria-controls"), "site-nav")
            self.assertEqual(page.nav_toggle_attrs.get("aria-expanded"), "false")
            self.assertEqual(page.nav_toggle_attrs.get("aria-label"), "Open menu")
            self.assertTrue(page.has_site_nav, name)
            self.assertTrue(page.has_theme_toggle, name)
            self.assertTrue(any("theme.js" in src for src in page.scripts), name)
            self.assertTrue(any("analytics.js" in src for src in page.scripts), name)
            self.assertTrue(any("styles.css" in href for href in page.stylesheets), name)
            self.assertIn("#why" if name == "index" else "index.html#why", page.nav_hrefs)
            self.assertIn("product.html", page.nav_hrefs)
            self.assertIn("/docs/", page.nav_hrefs)
            self.assertIn("pricing.html", page.nav_hrefs)
            self.assertIn("/docs/support/", page.nav_hrefs)
            self.assertIn("privacy.html", page.nav_hrefs)
            self.assertTrue(
                any(href.endswith("#founding") for href in page.nav_hrefs),
                name,
            )
            self.assertIn("product.html", page.footer_hrefs)
            self.assertIn("terms.html", page.footer_hrefs)
            self.assertIn("refunds.html", page.footer_hrefs)
            self.assertIn("privacy.html", page.footer_hrefs)
            self.assertIn("mailto:support@yeetngreet.app", page.footer_hrefs)

    def test_shared_marketing_nav_includes_product(self) -> None:
        for filename in (
            "pricing.html",
            "privacy.html",
            "terms.html",
            "refunds.html",
            "404.html",
        ):
            html = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn("product.html", html, filename)
            self.assertIn('class="nav-toggle"', html) if filename != "404.html" else None
            self.assertIn("theme.js", html)

    def test_copy_rules(self) -> None:
        for name, html in (("index", INDEX), ("product", PRODUCT)):
            page = parse(html)
            text = page.visible_text().lower()
            self.assertNotRegex(text, r"\bseats?\b", name)
            self.assertNotRegex(text, r"\bmsp\b", name)
            self.assertNotIn("open source", text, name)
            self.assertIn("admin", text, name)
        home = parse(INDEX).visible_text()
        self.assertIn("licensed users", home)
        self.assertIn("Free: 1–25 licensed users", home)
        self.assertIn("Paid from $19/mo", home)

    def test_home_pricing_teaser_matches_live_bands(self) -> None:
        self.assertIn("1–25 licensed users", PRICING)
        self.assertIn("$19", PRICING)
        self.assertEqual(live_plan_prices(), ["$0", "$19", "$49", "$99", "$149", "$249"])
        home = parse(INDEX).visible_text()
        self.assertIn("1–25", home)
        self.assertIn("$19/mo", home)
        self.assertNotIn("$29", home)
        self.assertNotIn("1–10", home)

    def test_palette_tokens_stay_live(self) -> None:
        self.assertIn("--bg: #f3f4f7;", STYLES)
        self.assertIn("--cta: #1a1d27;", STYLES)
        self.assertIn("--link: #2b57c9;", STYLES)
        self.assertIn("--danger: #c2410c;", STYLES)
        dark = STYLES.split(':root[data-theme="dark"]', 1)[1]
        self.assertIn("--bg: #12141a;", dark)
        self.assertIn("--cta: #7aa2f7;", dark)
        self.assertIn("--cta-ink: #0b1020;", dark)
        self.assertNotIn("#2563eb", STYLES)
        self.assertNotIn("#4f46e5", STYLES)

    def test_theme_js_keeps_nav_accessibility(self) -> None:
        theme = (ROOT / "theme.js").read_text(encoding="utf-8")
        self.assertIn('querySelector(".nav-toggle")', theme)
        self.assertIn('getElementById("site-nav")', theme)
        self.assertIn('aria-expanded', theme)
        self.assertIn("Escape", theme)
        self.assertIn("yeetngreet-site-theme", theme)

    def test_lean_sections_are_visible_without_observer(self) -> None:
        """Below-the-fold copy must not start at opacity 0 waiting on scroll IO."""
        self.assertNotIn("IntersectionObserver", INDEX)
        self.assertNotIn("IntersectionObserver", PRODUCT)
        self.assertNotRegex(INDEX, r'\bclass="[^"]*\breveal\b')
        self.assertNotRegex(PRODUCT, r'\bclass="[^"]*\breveal\b')
        hide_rule = re.search(
            r"@media\s*\(prefers-reduced-motion:\s*no-preference\)\s*\{[^}]*\.reveal\s*\{[^}]*opacity:\s*0",
            STYLES,
            re.DOTALL,
        )
        self.assertIsNone(hide_rule)
        self.assertIn(".reveal,\n.reveal.is-visible {\n  opacity: 1;\n}", STYLES)
        self.assertIn("theme.js", INDEX)
        self.assertIn("theme.js", PRODUCT)
        self.assertIn('class="nav-toggle"', INDEX)
        self.assertIn('class="nav-toggle"', PRODUCT)

    def test_cname_and_docs_product_link(self) -> None:
        self.assertEqual((ROOT / "CNAME").read_text(encoding="utf-8").strip(), "yeetngreet.app")
        mkdocs = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        self.assertIn("product: https://yeetngreet.app/product.html", mkdocs)
        header = (ROOT / "overrides/partials/header.html").read_text(encoding="utf-8")
        self.assertIn("product.html", header)
        sitemap = (ROOT / "sitemap-pages.xml").read_text(encoding="utf-8")
        self.assertIn("https://yeetngreet.app/product.html", sitemap)


if __name__ == "__main__":
    unittest.main()
