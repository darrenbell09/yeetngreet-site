"""Marketing opt-in checkbox on waitlist/founding handoff pages."""

from __future__ import annotations

import pathlib
import re
import unittest
from html.parser import HTMLParser


ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKETING = (ROOT / "marketing.js").read_text(encoding="utf-8")
PRIVACY = (ROOT / "privacy.html").read_text(encoding="utf-8")
WAITLIST = (ROOT / "go" / "waitlist" / "index.html").read_text(encoding="utf-8")
FOUNDING = (ROOT / "go" / "founding" / "index.html").read_text(encoding="utf-8")
ANALYTICS = (ROOT / "analytics.js").read_text(encoding="utf-8")
DESIGN = (ROOT / "tools" / "marketing-subscribe.md").read_text(encoding="utf-8")


class _FormInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.checkbox: dict[str, str] | None = None
        self.checkbox_checked = False
        self.email_hidden = False
        self.has_meta_refresh = False
        self.auto_redirect = False

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

    def test_sources_and_endpoint_are_explicit(self) -> None:
        self.assertIn('data-yg-source="waitlist"', WAITLIST)
        self.assertIn('data-yg-source="founding"', FOUNDING)
        self.assertRegex(MARKETING, r'YG_MARKETING_SUBSCRIBE_URL\s*=\s*""')
        self.assertIn("consented_at", MARKETING)
        self.assertIn("source_path", MARKETING)
        self.assertIn("consent_text", MARKETING)
        self.assertIn("Email me YeetnGreet news and updates", MARKETING)
        self.assertIn("endpoint_not_configured", MARKETING)
        self.assertIn("tools/marketing-subscribe.md", MARKETING)

    def test_marketing_script_never_sends_email_to_ga(self) -> None:
        # generate_lead may fire, but the email must not be an event parameter.
        self.assertIn('ygTrack("generate_lead"', MARKETING)
        self.assertNotRegex(MARKETING, r'ygTrack\([^)]*email')
        self.assertNotRegex(MARKETING, r'gtag\([^)]*email')
        self.assertIn("Must never be passed to gtag", MARKETING)

    def test_design_doc_proposes_worker_and_d1_without_deploying(self) -> None:
        self.assertIn("not deployed", DESIGN.lower())
        self.assertIn("D1", DESIGN)
        self.assertIn("marketing_subscribers", DESIGN)
        self.assertIn("unsubscribed_at", DESIGN)
        self.assertIn("Do not deploy this Worker", DESIGN)
        self.assertIn("Google Form", DESIGN)

    def test_privacy_covers_marketing_and_unsubscribe(self) -> None:
        self.assertIn('id="marketing-emails"', PRIVACY)
        self.assertIn("support@yeetngreet.app", PRIVACY)
        self.assertIn("unsubscribe", PRIVACY.lower())
        self.assertIn("We do not send your email address to Google Analytics", PRIVACY)
        self.assertIn("only when that box is ticked", PRIVACY)

    def test_copy_rules(self) -> None:
        for name, text in (("marketing.js", MARKETING), ("go/waitlist", WAITLIST), ("go/founding", FOUNDING)):
            lower = text.lower()
            self.assertNotRegex(lower, r"\bseats?\b", name)
            self.assertNotRegex(lower, r"\bmsp\b", name)


if __name__ == "__main__":
    unittest.main()
