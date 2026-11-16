"""Legal pages required for Paddle Merchant of Record and product license."""

from __future__ import annotations

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
TERMS = (ROOT / "terms.html").read_text(encoding="utf-8")
PRIVACY = (ROOT / "privacy.html").read_text(encoding="utf-8")
REFUNDS = (ROOT / "refunds.html").read_text(encoding="utf-8")
EULA = (ROOT / "eula.html").read_text(encoding="utf-8")


class LegalPagesTests(unittest.TestCase):
    def test_required_pages_exist_and_are_linked(self) -> None:
        for name, html in (
            ("terms", TERMS),
            ("privacy", PRIVACY),
            ("refunds", REFUNDS),
            ("eula", EULA),
        ):
            self.assertIn("<h1>", html, name)
            self.assertIn("YeetnGreet LLC", html, name)
            self.assertIn("Louisiana", html, name)
            self.assertIn("support@yeetngreet.app", html, name)
            self.assertIn("email-only", html, name)

        self.assertIn('href="/eula.html"', TERMS)
        self.assertIn('href="/terms.html"', EULA)
        self.assertIn('href="/refunds.html"', TERMS)
        self.assertIn('href="/privacy.html"', TERMS)

    def test_paddle_is_merchant_of_record(self) -> None:
        for name, html in (("terms", TERMS), ("refunds", REFUNDS), ("eula", EULA), ("privacy", PRIVACY)):
            blob = re.sub(r"\s+", " ", html)
            self.assertTrue(
                "Merchant of Record" in blob or "Paddle.com is the Merchant of Record" in blob or "Paddle.com, the Merchant of Record" in blob,
                name,
            )
            self.assertIn("Paddle", html, name)

    def test_trial_and_refund_policy(self) -> None:
        self.assertIn("14-day trial", TERMS)
        self.assertIn("14-day trial", REFUNDS)
        self.assertIn("14-day trial", EULA)
        self.assertIn("30-day money-back", REFUNDS)
        self.assertIn("paddle.net", REFUNDS)
        self.assertIn("Paddle processes all refunds", REFUNDS)

    def test_copy_rules(self) -> None:
        for name, html in (
            ("terms", TERMS),
            ("privacy", PRIVACY),
            ("refunds", REFUNDS),
            ("eula", EULA),
        ):
            text = re.sub(r"<[^>]+>", " ", html)
            text = re.sub(r"\s+", " ", text)
            lower = text.lower()
            self.assertNotRegex(lower, r"\bseats?\b", name)
            self.assertNotRegex(lower, r"\bmsp\b", name)
            self.assertNotIn("open source", lower, name)
            self.assertRegex(lower, r"licensed[- ]users?", name)


if __name__ == "__main__":
    unittest.main()
