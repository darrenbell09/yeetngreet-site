"""Pricing page loads Paddle.js Billing v2; Buy opens overlay; no open on load."""

from __future__ import annotations

import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
PRICING = (ROOT / "pricing.html").read_text(encoding="utf-8")
PADDLE = (ROOT / "paddle.js").read_text(encoding="utf-8")


class PaddlePricingTests(unittest.TestCase):
    def test_pricing_includes_cdn_then_local_init(self) -> None:
        cdn = PRICING.find('src="https://cdn.paddle.com/paddle/v2/paddle.js"')
        local = PRICING.find('src="paddle.js')
        self.assertNotEqual(cdn, -1)
        self.assertNotEqual(local, -1)
        self.assertLess(cdn, local)
        self.assertIn("theme.js", PRICING)
        self.assertIn("analytics.js", PRICING)
        self.assertIn("theme-toggle", PRICING)
        self.assertIn("/go/waitlist/", PRICING)
        self.assertIn("Payments are processed by Paddle", PRICING)

    def test_init_is_sandbox_with_public_client_token(self) -> None:
        self.assertIn('YG_PADDLE_TOKEN = "test_c665c31e7dbd12543f5dcd84304"', PADDLE)
        self.assertIn('YG_PADDLE_ENVIRONMENT = "sandbox"', PADDLE)
        self.assertIn('Paddle.Environment.set("sandbox")', PADDLE)
        self.assertIn("Paddle.Initialize({ token: YG_PADDLE_TOKEN })", PADDLE)
        self.assertIn("YG_PADDLE_ENVIRONMENT", PADDLE)
        self.assertRegex(PADDLE, r"live_")
        self.assertIn("production", PADDLE)

    def test_does_not_open_checkout_with_items_on_load(self) -> None:
        # Initialize must not open checkout; Buy click handler may call Checkout.open.
        init_block = PADDLE.split("Paddle.Initialize({ token: YG_PADDLE_TOKEN });", 1)[1]
        self.assertNotRegex(
            init_block.split("document.addEventListener", 1)[0],
            r"Checkout\.open\s*\(",
        )
        self.assertIn("No Checkout.open on load", PADDLE)
        self.assertIn("_ptxn", PADDLE)
        self.assertIn("ygPaddleOpenCheckout", PADDLE)
        self.assertIn("Paddle.Checkout.open", PADDLE)
        self.assertIn("YG_PADDLE_PRICES", PADDLE)
        self.assertIn("REPLACE_WITH_PADDLE_PRICE_ID_", PADDLE)

    def test_paid_plans_have_buy_buttons_free_waitlist_enterprise_email(self) -> None:
        for plan in ("starter", "growth", "business", "scale", "large"):
            self.assertIn(f'data-paddle-plan="{plan}"', PRICING)
            self.assertIn(
                f'data-paddle-plan="{plan}" data-paddle-interval="monthly"',
                PRICING,
            )
            self.assertIn(
                f'data-paddle-plan="{plan}" data-paddle-interval="annual"',
                PRICING,
            )
        self.assertIn("Buy monthly", PRICING)
        self.assertIn("Buy annual", PRICING)
        self.assertIn("14-day trial", PRICING)
        self.assertIn('href="/go/waitlist/"', PRICING)
        self.assertIn("Join the waitlist", PRICING)
        self.assertIn('mailto:support@yeetngreet.app">Contact us', PRICING)
        self.assertNotIn('data-paddle-plan="enterprise"', PRICING)
        self.assertNotIn('data-paddle-plan="free"', PRICING)

    def test_pricing_copy_rules_still_hold(self) -> None:
        text = re.sub(r"\s+", " ", PRICING)
        self.assertNotRegex(text, r"\bseats?\b")
        self.assertNotRegex(text.lower(), r"\bmsp\b")
        self.assertNotIn("open source", text.lower())
        self.assertIn("licensed users", text)
        self.assertIn("<h3>Free</h3>", PRICING)
        self.assertIn("support@yeetngreet.app", PRICING)
        self.assertIn("<h1>Pricing</h1>", PRICING)
        self.assertIn(
            "Billed by licensed users pooled across every tenant on your account.",
            text,
        )


if __name__ == "__main__":
    unittest.main()
