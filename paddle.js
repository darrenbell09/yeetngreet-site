/*
 * Paddle Billing overlay on /pricing (Paddle.js v2).
 * Sandbox values ship so ?_ptxn=txn_… opens checkout today.
 * For live: set YG_PADDLE_TOKEN to a live_… client-side token and
 * YG_PADDLE_ENVIRONMENT to "production". Do not use API keys here.
 *
 * Price IDs: none are checked into this repo or Worker docs yet.
 * Replace every REPLACE_WITH_PADDLE_PRICE_ID_* value below with real
 * Paddle price IDs (pri_…) from the Paddle dashboard before go-live.
 */
var YG_PADDLE_TOKEN = "test_c665c31e7dbd12543f5dcd84304";
var YG_PADDLE_ENVIRONMENT = "sandbox"; // "sandbox" | "production"

/** @type {Record<string, { monthly: string, annual: string }>} */
var YG_PADDLE_PRICES = {
  // PLACEHOLDERS — replace with real Paddle price IDs (pri_…)
  starter: {
    monthly: "REPLACE_WITH_PADDLE_PRICE_ID_STARTER_MONTHLY",
    annual: "REPLACE_WITH_PADDLE_PRICE_ID_STARTER_ANNUAL"
  },
  growth: {
    monthly: "REPLACE_WITH_PADDLE_PRICE_ID_GROWTH_MONTHLY",
    annual: "REPLACE_WITH_PADDLE_PRICE_ID_GROWTH_ANNUAL"
  },
  business: {
    monthly: "REPLACE_WITH_PADDLE_PRICE_ID_BUSINESS_MONTHLY",
    annual: "REPLACE_WITH_PADDLE_PRICE_ID_BUSINESS_ANNUAL"
  },
  scale: {
    monthly: "REPLACE_WITH_PADDLE_PRICE_ID_SCALE_MONTHLY",
    annual: "REPLACE_WITH_PADDLE_PRICE_ID_SCALE_ANNUAL"
  },
  large: {
    monthly: "REPLACE_WITH_PADDLE_PRICE_ID_LARGE_MONTHLY",
    annual: "REPLACE_WITH_PADDLE_PRICE_ID_LARGE_ANNUAL"
  }
};

function ygPaddleOpenCheckout(priceId) {
  if (typeof Paddle === "undefined" || !Paddle.Checkout) {
    return;
  }
  if (!priceId || String(priceId).indexOf("REPLACE_WITH_PADDLE_PRICE_ID_") === 0) {
    console.warn(
      "YeetnGreet: set a real Paddle price ID in YG_PADDLE_PRICES before checkout can open."
    );
    return;
  }
  Paddle.Checkout.open({
    items: [{ priceId: priceId, quantity: 1 }]
  });
}

(function () {
  if (typeof Paddle === "undefined" || !YG_PADDLE_TOKEN) {
    return;
  }
  // Script-tag Billing docs: Environment.set before Initialize for sandbox.
  if (YG_PADDLE_ENVIRONMENT === "sandbox") {
    Paddle.Environment.set("sandbox");
  }
  Paddle.Initialize({ token: YG_PADDLE_TOKEN });
  // No Checkout.open on load — Paddle.js opens ?_ptxn= automatically.
  // Buy buttons call ygPaddleOpenCheckout after click.

  document.addEventListener("click", function (event) {
    var btn = event.target && event.target.closest
      ? event.target.closest("[data-paddle-plan][data-paddle-interval]")
      : null;
    if (!btn) {
      return;
    }
    event.preventDefault();
    var plan = btn.getAttribute("data-paddle-plan");
    var interval = btn.getAttribute("data-paddle-interval");
    var entry = YG_PADDLE_PRICES[plan];
    if (!entry || !entry[interval]) {
      console.warn("YeetnGreet: unknown Paddle plan/interval", plan, interval);
      return;
    }
    ygPaddleOpenCheckout(entry[interval]);
  });
})();
