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
    def test_ga_measurement_id_is_configured(self) -> None:
        self.assertRegex(ANALYTICS, r'YG_GA_MEASUREMENT_ID\s*=\s*"G-4QZ4FZPC5X"')
        self.assertIn("googletagmanager.com/gtag/js", ANALYTICS)
        self.assertIn("anonymize_ip: true", ANALYTICS)
        self.assertIn("allow_google_signals: false", ANALYTICS)
        self.assertIn("allow_ad_personalization_signals: false", ANALYTICS)

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
        self.assertIn("Google Analytics 4", PRIVACY)
        self.assertIn("IP anonymization", PRIVACY)
        self.assertNotIn("Until a measurement ID is configured", PRIVACY)

    def test_homepage_has_no_search_console_meta_tag(self) -> None:
        self.assertNotIn("google-site-verification", INDEX)
        self.assertNotIn("Google Search Console HTML tag verification", INDEX)
        parser = _MetaCollector()
        parser.feed(INDEX)
        matches = [
            m for m in parser.metas if m.get("name") == "google-site-verification"
        ]
        self.assertEqual(matches, [])

    def test_copy_rules_on_consent_surfaces(self) -> None:
        for name, text in (("analytics.js", ANALYTICS), ("privacy.html", PRIVACY)):
            lower = text.lower()
            self.assertNotRegex(lower, r"\bseats?\b", name)
            self.assertNotRegex(lower, r"\bmsp\b", name)
            self.assertNotIn("open source", lower, name)

    def test_events_are_consent_gated_and_named(self) -> None:
        for needle in (
            "function ygTrack",
            "consentState === \"granted\"",
            'ygTrack("select_item"',
            'ygTrack("begin_checkout"',
            'ygTrack("purchase"',
            'ygTrack("checkout_closed"',
            'ygTrack("checkout_payment_failed"',
            'ygTrack("file_download"',
            'ygTrack("trial_cta_click"',
            'ygTrack("generate_lead"',
            'ygTrack("docs_page_view"',
            'ygTrack("click"',
            'ygTrack("mailto_click"',
            'ygTrack("pricing_toggle"',
            'ygTrack("scroll"',
            'ygTrack("search"',
            "percent_scrolled",
            "item_name",
            "transaction_id",
            "lead_type",
            "contact_type: \"support\"",
        ):
            self.assertIn(needle, ANALYTICS, needle)
        self.assertIn("checkout.loaded", ANALYTICS)
        self.assertIn("checkout.completed", ANALYTICS)
        self.assertIn("checkout.closed", ANALYTICS)
        self.assertIn("checkout.payment.failed", ANALYTICS)

    def test_analytics_strips_emails_and_never_tracks_raw_event_data(self) -> None:
        self.assertIn("function sanitizeParams", ANALYTICS)
        self.assertIn("looksLikeEmail", ANALYTICS)
        self.assertIn("safeTransactionId", ANALYTICS)
        self.assertNotIn("ygTrack(event.data", ANALYTICS)
        self.assertIn('window.gtag("event", eventName, sanitizeParams', ANALYTICS)
        # Search redacts email-like terms; track helpers do not pass email fields.
        self.assertIn("sanitizeSearchTerm", ANALYTICS)
        self.assertNotRegex(ANALYTICS, r'ygTrack\([^)]*email')

    def test_privacy_lists_collected_events_and_marketing(self) -> None:
        self.assertIn("Scroll-depth milestones", PRIVACY)
        self.assertIn("transaction ID", PRIVACY)
        self.assertIn("id=\"marketing-emails\"", PRIVACY)
        self.assertIn("news and updates", PRIVACY.lower())
        self.assertIn("unsubscribe", PRIVACY.lower())
        self.assertIn("We do not send your email address to Google Analytics", PRIVACY)


if __name__ == "__main__":
    unittest.main()

