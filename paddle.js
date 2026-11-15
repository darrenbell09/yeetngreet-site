/*
 * Paddle Billing overlay on /pricing (Paddle.js v2).
 * Sandbox values ship so ?_ptxn=txn_… opens checkout today.
 * For live: set YG_PADDLE_TOKEN to a live_… client-side token and
 * YG_PADDLE_ENVIRONMENT to "production". Do not use API keys here.
 *
 * YG_PADDLE_PRICES below are SANDBOX price IDs matched to the sandbox
 * client token. Swap every pri_… for live price IDs at release when
 * flipping the token/environment to production.
 */
var YG_PADDLE_TOKEN = "test_c665c31e7dbd12543f5dcd84304";
var YG_PADDLE_ENVIRONMENT = "sandbox"; // "sandbox" | "production"

/** @type {Record<string, { monthly: string, yearly: string }>} */
var YG_PADDLE_PRICES = {
  // SANDBOX only — replace with live pri_… IDs at release.
  starter: {
    monthly: "pri_01m63yp7ktegz147hrcarqqwxp",
    yearly: "pri_01m63yppecwe5wqx2n80hy2a6f"
  },
  growth: {
    monthly: "pri_01m63yq7hwkmnm5brnqerrpnxs",
    yearly: "pri_01m63yqhc6zdmc3a9ffgscyrgr"
  },
  business: {
    monthly: "pri_01m63yr35xcqp138dbrb65qshb",
    yearly: "pri_01m63yrcnc6sp58rk72wa0zqah"
  },
  scale: {
    monthly: "pri_01m63ys3s0r2egmx4r5tv8rv9y",
    yearly: "pri_01m63yscyxt8vjfg6zq18kdzeq"
  },
  large: {
    monthly: "pri_01m63ytfp22f89hbx8ttxnn0qa",
    yearly: "pri_01m63ytsaqqx19hzf2ayq3skwd"
  }
};

function ygPaddleOpenCheckout(priceId) {
  if (typeof Paddle === "undefined" || !Paddle.Checkout) {
    return;
  }
  if (!priceId || String(priceId).indexOf("pri_") !== 0) {
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
