/*
 * Paddle Billing overlay on /pricing (Paddle.js v2).
 * Sandbox values ship so ?_ptxn=txn_… opens checkout today.
 * For live: set YG_PADDLE_TOKEN to a live_… client-side token and
 * YG_PADDLE_ENVIRONMENT to "production". Do not use API keys here.
 */
var YG_PADDLE_TOKEN = "test_c665c31e7dbd12543f5dcd84304";
var YG_PADDLE_ENVIRONMENT = "sandbox"; // "sandbox" | "production"

(function () {
  if (typeof Paddle === "undefined" || !YG_PADDLE_TOKEN) {
    return;
  }
  // Script-tag Billing docs: Environment.set before Initialize for sandbox.
  if (YG_PADDLE_ENVIRONMENT === "sandbox") {
    Paddle.Environment.set("sandbox");
  }
  Paddle.Initialize({ token: YG_PADDLE_TOKEN });
  // No items payload on load — Paddle.js opens ?_ptxn= automatically.
})();
