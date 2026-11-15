"""Privacy-first consent banner and Google Consent Mode defaults."""

from __future__ import annotations

import pathlib
import re
import unittest
from html.parser import HTMLParser


ROOT = pathlib.Path(__file__).resolve().parents[1]
ANALYTICS = (ROOT / "analytics.js").read_text(encoding="utf-8")
PRIVACY = (ROOT / "privacy.html").read_text(encoding="utf-8")
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
STYLES = (ROOT / "styles.css").read_text(encoding="utf-8")


class _MetaCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.metas: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "meta":
            return
        data = {k: (v or "") for k, v in attrs}
        self.metas.append(data)


class ConsentAnalyticsTests(unittest.TestCase):
    def test_ga_measurement_id_is_empty_placeholder(self) -> None:
        self.assertRegex(ANALYTICS, r'YG_GA_MEASUREMENT_ID\s*=\s*""')
        self.assertIn("PLACEHOLDER", ANALYTICS)
        self.assertIn("googletagmanager.com/gtag/js", ANALYTICS)

    def test_consent_mode_defaults_deny_ads_and_analytics(self) -> None:
        self.assertIn('gtag("consent", "default"', ANALYTICS)
        for key in (
            "ad_storage",
            "ad_user_data",
            "ad_personalization",
            "analytics_storage",
        ):
            self.assertRegex(
                ANALYTICS,
                rf"{key}:\s*\"denied\"",
                msg=f"expected default denied for {key}",
            )
        self.assertIn("deniedAlways", ANALYTICS)
        self.assertIn("ad_storage: \"denied\"", ANALYTICS.split("deniedAlways", 1)[1])

    def test_no_ga_tag_loads_before_opt_in(self) -> None:
        self.assertIn('data-yg-consent="granted"', ANALYTICS)
        self.assertIn("loadGaIfConfigured", ANALYTICS)
        # GA script is created only inside loadGaIfConfigured after grant.
        self.assertIn('choice === "granted"', ANALYTICS)
        self.assertIn("yg-consent-banner", ANALYTICS)
        self.assertIn("Accept analytics", ANALYTICS)
        self.assertIn("Decline", ANALYTICS)

    def test_consent_banner_styles_exist(self) -> None:
        self.assertIn(".yg-consent-banner", STYLES)
        self.assertIn(".yg-consent-actions", STYLES)

    def test_privacy_policy_documents_optional_analytics(self) -> None:
        self.assertIn('id="optional-analytics"', PRIVACY)
        self.assertIn("opt-in", PRIVACY.lower())
        self.assertIn("Consent Mode", PRIVACY)
        self.assertIn("advertising storage", PRIVACY.lower())

    def test_homepage_has_empty_search_console_verification_hook(self) -> None:
        self.assertIn("google-site-verification", INDEX)
        self.assertIn("Google Search Console HTML tag verification", INDEX)
        parser = _MetaCollector()
        parser.feed(INDEX)
        matches = [
            m for m in parser.metas if m.get("name") == "google-site-verification"
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].get("content", "missing"), "")

    def test_copy_rules_on_consent_surfaces(self) -> None:
        for name, text in (("analytics.js", ANALYTICS), ("privacy.html", PRIVACY)):
            lower = text.lower()
            self.assertNotRegex(lower, r"\bseats?\b", name)
            self.assertNotRegex(lower, r"\bmsp\b", name)
            self.assertNotIn("open source", lower, name)


if __name__ == "__main__":
    unittest.main()
