"""Marketing opt-in checkbox on waitlist/founding handoff pages."""

from __future__ import annotations

import pathlib
import unittest
from html.parser import HTMLParser


ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKETING = (ROOT / "marketing.js").read_text(encoding="utf-8")
PRIVACY = (ROOT / "privacy.html").read_text(encoding="utf-8")
WAITLIST = (ROOT / "go" / "waitlist" / "index.html").read_text(encoding="utf-8")
FOUNDING = (ROOT / "go" / "founding" / "index.html").read_text(encoding="utf-8")
DESIGN = (ROOT / "tools" / "marketing-subscribe.md").read_text(encoding="utf-8")
WORKER = (ROOT / "worker" / "marketing" / "src" / "index.js").read_text(encoding="utf-8")
WORKER_CFG = (ROOT / "worker" / "marketing" / "wrangler.jsonc").read_text(encoding="utf-8")
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")

WORKER_URL = "https://yeetngreet-marketing.darren-c9b.workers.dev"


class _FormInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.checkbox: dict[str, str] | None = None
        self.checkbox_checked = False
        self.email_hidden = False
        self.has_meta_refresh = False
        self.honeypot: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: (v or "") for k, v in attrs}
        if tag == "meta" and data.get("http-equiv", "").lower() == "refresh":
            self.has_meta_refresh = True
        if tag == "input" and data.get("id") == "yg-marketing-optin":
            self.checkbox = data
            self.checkbox_checked = "checked" in data
        if tag == "div" and data.get("id") == "yg-marketing-email-wrap" and "hidden" in data:
            self.email_hidden = True
        if tag == "input" and data.get("id") == "yg-marketing-email-wrap" and "hidden" in data:
            self.email_hidden = True
        if tag == "input" and data.get("id") == "yg-marketing-website":
            self.honeypot = data


class MarketingOptInTests(unittest.TestCase):
    def test_go_pages_have_unticked_marketing_checkbox(self) -> None:
        for name, html in (("waitlist", WAITLIST), ("founding", FOUNDING)):
            parser = _FormInspector()
            parser.feed(html)
            self.assertIsNotNone(parser.checkbox, name)
            self.assertFalse(parser.checkbox_checked, name)
            self.assertEqual(parser.checkbox.get("type"), "checkbox")
            self.assertIn("Email me YeetnGreet news and updates", html)
            self.assertTrue(parser.email_hidden, name)
            self.assertFalse(parser.has_meta_refresh, name)
            self.assertNotIn("location.replace", html)
            self.assertNotIn("http-equiv", html.lower())
            self.assertIn("marketing.js", html)
            self.assertIn('id="yg-signup-form"', html)

    def test_go_pages_include_hidden_honeypot(self) -> None:
        for name, html in (("waitlist", WAITLIST), ("founding", FOUNDING)):
            parser = _FormInspector()
            parser.feed(html)
            self.assertIsNotNone(parser.honeypot, name)
            self.assertEqual(parser.honeypot.get("type"), "text")
            self.assertEqual(parser.honeypot.get("name"), "website")
            self.assertIn('tabindex="-1"', html)
            self.assertIn('class="yg-hp"', html)

    def test_sources_and_endpoint_are_explicit(self) -> None:
        self.assertIn('data-yg-source="waitlist"', WAITLIST)
        self.assertIn('data-yg-source="founding"', FOUNDING)
        self.assertIn(f'YG_MARKETING_SUBSCRIBE_URL =\n  "{WORKER_URL}"', MARKETING)
        self.assertIn("consent: true", MARKETING)
        self.assertIn("consented_at", MARKETING)
        self.assertIn("source_path", MARKETING)
        self.assertIn("consent_text", MARKETING)
        self.assertIn("website:", MARKETING)
        self.assertIn("Email me YeetnGreet news and updates", MARKETING)
        self.assertIn("worker/marketing", MARKETING)

    def test_marketing_script_never_sends_email_to_ga(self) -> None:
        self.assertIn('ygTrack("generate_lead"', MARKETING)
        self.assertNotRegex(MARKETING, r"ygTrack\([^)]*email")
        self.assertNotRegex(MARKETING, r"gtag\([^)]*email")
        self.assertIn("Must never be passed to gtag", MARKETING)

    def test_design_doc_describes_deployed_worker(self) -> None:
        self.assertIn("yeetngreet-marketing", DESIGN)
        self.assertIn(WORKER_URL, DESIGN)
        self.assertIn("D1", DESIGN)
        self.assertIn("marketing_subscribers", DESIGN)
        self.assertIn("unsubscribed_at", DESIGN)
        self.assertIn("workers.dev", DESIGN)
        self.assertIn("wrangler d1 execute yeetngreet-marketing", DESIGN)
        self.assertNotIn("Do not deploy this Worker", DESIGN)
        self.assertIn("Google Form", DESIGN)

    def test_worker_is_post_only_with_restricted_cors(self) -> None:
        self.assertIn('name": "yeetngreet-marketing"', WORKER_CFG)
        self.assertIn("c9bdb7514d2ffc3a0845df5bce71ab12", WORKER_CFG)
        self.assertIn("1799af3b-2a74-47c1-aeac-352bd1d04524", WORKER_CFG)
        self.assertIn('"workers_dev": true', WORKER_CFG)
        self.assertNotIn("routes", WORKER_CFG)
        self.assertIn("https://yeetngreet.app", WORKER)
        self.assertIn("method_not_allowed", WORKER)
        self.assertIn("consent_required", WORKER)
        self.assertIn("ON CONFLICT(email) DO UPDATE SET", WORKER)
        self.assertIn("unsubscribed_at = NULL", WORKER)
        self.assertIn("rate_limited", WORKER)
        self.assertIn("payload_too_large", WORKER)
        self.assertIn("honeypotFilled", WORKER)
        self.assertIn("Never log email", WORKER)
        self.assertNotIn("console.log", WORKER)

    def test_pricing_keeps_waitlist_ctas(self) -> None:
        self.assertIn("Join the waitlist", PRICING)
        self.assertIn('href="/go/waitlist/"', PRICING)
        self.assertNotIn("Buy monthly", PRICING)
        self.assertNotIn("Buy annual", PRICING)
        self.assertNotIn("data-paddle-plan", PRICING)
        self.assertIn("licensed users", PRICING)

    def test_privacy_covers_marketing_and_unsubscribe(self) -> None:
        self.assertIn('id="marketing-emails"', PRIVACY)
        self.assertIn("support@yeetngreet.app", PRIVACY)
        self.assertIn("unsubscribe", PRIVACY.lower())
        self.assertIn("We do not send your email address to Google Analytics", PRIVACY)
        self.assertIn("only when that box is ticked", PRIVACY)

    def test_copy_rules(self) -> None:
        for name, text in (
            ("marketing.js", MARKETING),
            ("go/waitlist", WAITLIST),
            ("go/founding", FOUNDING),
            ("privacy", PRIVACY),
            ("pricing", PRICING),
        ):
            lower = text.lower()
            self.assertNotRegex(lower, r"\bseats?\b", name)
            self.assertNotRegex(lower, r"\bmsp\b", name)
            if name != "privacy":
                self.assertNotIn("open source", lower, name)


if __name__ == "__main__":
    unittest.main()
