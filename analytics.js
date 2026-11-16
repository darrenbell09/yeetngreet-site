/*
 * YeetnGreet site analytics — privacy-first, opt-in.
 *
 * - Google Consent Mode defaults start denied; no GA tag loads before consent.
 * - ad_storage, ad_user_data, and ad_personalization stay denied even after opt-in.
 * - After the visitor accepts, GA4 (YG_GA_MEASUREMENT_ID) loads with IP anonymization
 *   and Google ads/signals turned off. Decline keeps the tag unloaded, and no events fire.
 * - Cloudflare Web Analytics stays off while YG_CF_BEACON_TOKEN is empty.
 */
var YG_GA_MEASUREMENT_ID = "G-4QZ4FZPC5X";
var YG_CF_BEACON_TOKEN = "";

var YG_CONSENT_STORAGE_KEY = "yeetngreet-analytics-consent";

/** Display prices for ecommerce events. Currency is USD. */
var YG_PLAN_CATALOG = {
  starter: { name: "Starter", monthly: 19, yearly: 182 },
  growth: { name: "Growth", monthly: 49, yearly: 470 },
  business: { name: "Business", monthly: 99, yearly: 950 },
  scale: { name: "Scale", monthly: 149, yearly: 1430 },
  large: { name: "Large", monthly: 249, yearly: 2390 }
};

(function () {
  var deniedAlways = {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied"
  };

  var consentState = "unknown";
  var EMAIL_RE = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/i;
  var BLOCKED_PARAM_RE = /^(email|e-?mail|name|first_name|last_name|full_name|customer|customer_id|customer_email|customer_name|address|phone|tel|postal|zip|card|payment_method)$/i;
  var FILE_EXT_RE = /\.(pdf|csv|exe|zip|msi|dmg|pkg|docx?|xlsx?)$/i;
  var scrollFired = {};
  var lastSearchTerm = "";
  var searchTimer = null;
  var leadFired = false;

  window.dataLayer = window.dataLayer || [];
  function gtag() {
    window.dataLayer.push(arguments);
  }
  window.gtag = gtag;

  // Consent Mode defaults before any tag: everything denied.
  gtag("consent", "default", {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied",
    analytics_storage: "denied",
    functionality_storage: "denied",
    personalization_storage: "denied",
    security_storage: "granted",
    wait_for_update: 500
  });

  function loadGaIfConfigured() {
    var id = YG_GA_MEASUREMENT_ID;
    if (!id || id.indexOf("G-") !== 0) {
      return false;
    }
    if (document.getElementById("yg-ga-gtag")) {
      return true;
    }
    var s = document.createElement("script");
    s.id = "yg-ga-gtag";
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", id, {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
    return true;
  }

  function loadCloudflareIfConfigured() {
    var token = YG_CF_BEACON_TOKEN;
    if (!token) {
      return false;
    }
    if (document.querySelector('script[data-cf-beacon]')) {
      return true;
    }
    var s = document.createElement("script");
    s.defer = true;
    s.src = "https://static.cloudflareinsights.com/beacon.min.js";
    s.setAttribute("data-cf-beacon", JSON.stringify({ token: token }));
    document.head.appendChild(s);
    return true;
  }

  function isBlockedKey(key) {
    return BLOCKED_PARAM_RE.test(String(key || ""));
  }

  function looksLikeEmail(value) {
    return typeof value === "string" && EMAIL_RE.test(value);
  }

  function sanitizeParams(params) {
    var out = {};
    if (!params || typeof params !== "object") {
      return out;
    }
    Object.keys(params).forEach(function (key) {
      if (isBlockedKey(key)) {
        return;
      }
      var value = params[key];
      if (looksLikeEmail(value)) {
        return;
      }
      if (Array.isArray(value)) {
        out[key] = value.map(function (item) {
          return item && typeof item === "object" ? sanitizeParams(item) : item;
        }).filter(function (item) {
          return !looksLikeEmail(item);
        });
        return;
      }
      if (value && typeof value === "object") {
        out[key] = sanitizeParams(value);
        return;
      }
      out[key] = value;
    });
    return out;
  }

  function hasConsent() {
    return consentState === "granted";
  }

  function ygTrack(eventName, params) {
    if (!hasConsent()) {
      return false;
    }
    if (!eventName || typeof window.gtag !== "function") {
      return false;
    }
    if (!YG_GA_MEASUREMENT_ID || YG_GA_MEASUREMENT_ID.indexOf("G-") !== 0) {
      return false;
    }
    window.gtag("event", eventName, sanitizeParams(params || {}));
    return true;
  }
  window.ygTrack = ygTrack;

  function planEntry(plan) {
    return YG_PLAN_CATALOG[plan] || null;
  }

  function ecommerceItem(plan, interval) {
    var entry = planEntry(plan);
    if (!entry || (interval !== "monthly" && interval !== "yearly")) {
      return null;
    }
    var price = entry[interval];
    return {
      item_id: plan + "-" + interval,
      item_name: entry.name,
      item_category: "subscription",
      item_variant: interval,
      price: price,
      quantity: 1
    };
  }

  function ecommercePayload(plan, interval) {
    var item = ecommerceItem(plan, interval);
    if (!item) {
      return null;
    }
    return {
      currency: "USD",
      value: item.price,
      items: [item]
    };
  }
  window.ygEcommercePayload = ecommercePayload;

  function safeTransactionId(value) {
    if (typeof value !== "string") {
      return "";
    }
    return /^txn_[A-Za-z0-9]+$/.test(value) ? value : "";
  }

  function moneyValue(raw) {
    if (raw == null) {
      return undefined;
    }
    if (typeof raw === "number" && isFinite(raw)) {
      return raw;
    }
    if (typeof raw === "object") {
      if (raw.total != null && raw.total !== raw) {
        return moneyValue(raw.total);
      }
      if (raw.amount != null) {
        return moneyValue(raw.amount);
      }
    }
    var n = parseFloat(String(raw).replace(/,/g, ""), 10);
    return isFinite(n) ? n : undefined;
  }

  function priceIdToPlan(priceId) {
    var prices = window.YG_PADDLE_PRICES;
    if (!priceId || !prices) {
      return null;
    }
    var plans = Object.keys(prices);
    for (var i = 0; i < plans.length; i++) {
      var plan = plans[i];
      var entry = prices[plan];
      if (entry && entry.monthly === priceId) {
        return { plan: plan, interval: "monthly" };
      }
      if (entry && entry.yearly === priceId) {
        return { plan: plan, interval: "yearly" };
      }
    }
    return null;
  }

  function firstPriceId(data) {
    var items = data && data.items;
    if (!Array.isArray(items) || !items.length) {
      return "";
    }
    var first = items[0] || {};
    return first.price_id || (first.price && first.price.id) || first.priceId || "";
  }

  function payloadFromPaddleData(data) {
    var mapped = priceIdToPlan(firstPriceId(data)) || window.ygLastPaddleSelection || null;
    var payload = mapped ? ecommercePayload(mapped.plan, mapped.interval) : { currency: "USD", items: [] };
    if (!payload) {
      payload = { currency: "USD", items: [] };
    }
    var currency = data && typeof data.currency_code === "string" && /^[A-Z]{3}$/.test(data.currency_code)
      ? data.currency_code
      : payload.currency;
    var value = moneyValue(data && data.totals) ;
    if (value == null && payload.value != null) {
      value = payload.value;
    }
    payload.currency = currency;
    if (value != null) {
      payload.value = value;
    }
    return payload;
  }

  function handlePaddleEvent(event) {
    if (!event || typeof event.name !== "string") {
      return false;
    }
    var data = event.data && typeof event.data === "object" ? event.data : {};
    if (event.name === "checkout.loaded") {
      return ygTrack("begin_checkout", Object.assign({ source: "paddle" }, payloadFromPaddleData(data)));
    }
    if (event.name === "checkout.completed") {
      var purchase = Object.assign({ source: "paddle" }, payloadFromPaddleData(data));
      var txn = safeTransactionId(data.transaction_id);
      if (txn) {
        purchase.transaction_id = txn;
      }
      return ygTrack("purchase", purchase);
    }
    if (event.name === "checkout.closed") {
      return ygTrack("checkout_closed", { source: "paddle" });
    }
    if (event.name === "checkout.payment.failed" || event.name === "checkout.error") {
      var failed = { source: "paddle" };
      var failedTxn = safeTransactionId(data.transaction_id);
      if (failedTxn) {
        failed.transaction_id = failedTxn;
      }
      if (data.error && typeof data.error.code === "string") {
        failed.error_code = data.error.code.slice(0, 64);
      } else if (typeof data.error_code === "string") {
        failed.error_code = data.error_code.slice(0, 64);
      }
      return ygTrack("checkout_payment_failed", failed);
    }
    return false;
  }
  window.ygHandlePaddleEvent = handlePaddleEvent;

  function trackBuyClick(plan, interval) {
    var payload = ecommercePayload(plan, interval);
    if (!payload) {
      return false;
    }
    window.ygLastPaddleSelection = { plan: plan, interval: interval };
    ygTrack("select_item", {
      item_list_id: "pricing",
      item_list_name: "Plans",
      items: payload.items
    });
    ygTrack("begin_checkout", Object.assign({ source: "button" }, payload));
    return true;
  }
  window.ygTrackBuyClick = trackBuyClick;

  function sameSite(url) {
    try {
      var parsed = new URL(url, window.location.href);
      var host = parsed.hostname.replace(/^www\./, "");
      var here = window.location.hostname.replace(/^www\./, "");
      return host === here;
    } catch (err) {
      return true;
    }
  }

  function safeHref(url) {
    try {
      var parsed = new URL(url, window.location.href);
      return parsed.origin + parsed.pathname;
    } catch (err) {
      return "";
    }
  }

  function pathnameOf(url) {
    try {
      return new URL(url, window.location.href).pathname;
    } catch (err) {
      return "";
    }
  }

  function leadTypeFromUrl(url) {
    var path = pathnameOf(url);
    if (/\/go\/founding\/?$/.test(path)) {
      return "founding";
    }
    if (/\/go\/waitlist\/?$/.test(path)) {
      return "waitlist";
    }
    if (/docs\.google\.com\/forms\//i.test(String(url))) {
      if (/\/go\/founding\/?/.test(window.location.pathname)) {
        return "founding";
      }
      if (/\/go\/waitlist\/?/.test(window.location.pathname)) {
        return "waitlist";
      }
      return "waitlist";
    }
    return "";
  }

  function isFileDownload(url, link) {
    if (link && (link.getAttribute("data-yg-cta") === "download" || link.hasAttribute("download"))) {
      return true;
    }
    var path = pathnameOf(url);
    if (FILE_EXT_RE.test(path)) {
      return true;
    }
    return /\/assets\/samples\//.test(path);
  }

  function fileMeta(url) {
    var path = pathnameOf(url);
    var name = path.split("/").pop() || "";
    var match = name.match(/\.([A-Za-z0-9]+)$/);
    return {
      file_name: name.slice(0, 200),
      file_extension: match ? match[1].toLowerCase() : "",
      link_url: safeHref(url)
    };
  }

  function isTrialCta(link, url) {
    if (link && link.getAttribute("data-yg-cta") === "trial") {
      return true;
    }
    var path = pathnameOf(url) + (link && link.getAttribute("href") ? link.getAttribute("href") : "");
    return /\/trial(?:\/|$|\?|#)/i.test(path);
  }

  function sanitizeSearchTerm(term) {
    var value = String(term || "").trim().slice(0, 100);
    if (!value) {
      return "";
    }
    if (looksLikeEmail(value) || /^\+?\d[\d\s().-]{6,}$/.test(value)) {
      return "";
    }
    return value;
  }

  function fireSearch(term) {
    var clean = sanitizeSearchTerm(term);
    if (!clean || clean === lastSearchTerm) {
      return;
    }
    lastSearchTerm = clean;
    ygTrack("search", { search_term: clean });
  }

  function currentPath() {
    return window.location.pathname || "/";
  }

  function fireDocsPageView() {
    if (!/^\/docs(\/|$)/.test(currentPath())) {
      return;
    }
    ygTrack("docs_page_view", { page_path: currentPath() });
  }

  function fireGoLead() {
    var type = leadTypeFromUrl(window.location.href);
    if (!type || leadFired) {
      return;
    }
    leadFired = true;
    ygTrack("generate_lead", { lead_type: type, method: "form_redirect" });
  }

  function measureScrollPercent() {
    var el = document.documentElement;
    var body = document.body;
    var scrollTop = window.scrollY || (el && el.scrollTop) || 0;
    var height = Math.max(
      (el && el.scrollHeight) || 0,
      (body && body.scrollHeight) || 0
    ) - window.innerHeight;
    if (height <= 0) {
      return 100;
    }
    return Math.floor((scrollTop / height) * 100);
  }

  function onScrollDepth() {
    if (!hasConsent()) {
      return;
    }
    var pct = measureScrollPercent();
    [25, 50, 75, 90].forEach(function (mark) {
      if (pct >= mark && !scrollFired[mark]) {
        scrollFired[mark] = true;
        ygTrack("scroll", { percent_scrolled: mark });
      }
    });
  }

  function onDocumentClick(event) {
    var target = event.target && event.target.closest ? event.target.closest("a, button, [data-yg-cta], [data-paddle-plan]") : null;
    if (!target) {
      return;
    }

    if (target.matches && target.matches("[data-paddle-plan][data-paddle-interval]")) {
      trackBuyClick(
        target.getAttribute("data-paddle-plan"),
        target.getAttribute("data-paddle-interval")
      );
      return;
    }

    var href = target.getAttribute && target.getAttribute("href");
    if (!href) {
      var cta = target.getAttribute && target.getAttribute("data-yg-cta");
      if (cta === "trial") {
        ygTrack("trial_cta_click", { cta_name: "trial" });
      } else if (cta === "download") {
        ygTrack("file_download", { cta_name: "download" });
      }
      return;
    }

    if (href.indexOf("mailto:") === 0) {
      ygTrack("mailto_click", { contact_type: "support" });
      return;
    }

    var leadType = leadTypeFromUrl(href);
    if (leadType) {
      ygTrack("generate_lead", { lead_type: leadType, method: "cta_click" });
      return;
    }

    if (isTrialCta(target, href)) {
      ygTrack("trial_cta_click", { link_url: safeHref(href) });
      return;
    }

    if (isFileDownload(href, target)) {
      ygTrack("file_download", fileMeta(href));
      return;
    }

    if (/^(https?:)?\/\//i.test(href) || href.indexOf("//") === 0) {
      if (!sameSite(href)) {
        ygTrack("click", {
          outbound: true,
          link_url: safeHref(href),
          link_domain: (function () {
            try {
              return new URL(href, window.location.href).hostname;
            } catch (err) {
              return "";
            }
          })()
        });
      }
    }
  }

  function onPricingToggle(event) {
    var target = event.target;
    if (!target) {
      return;
    }
    var toggle = target.closest
      ? target.closest("[data-yg-pricing-toggle], [data-pricing-interval-toggle], .pricing-toggle, input[name='billing-period']")
      : null;
    if (!toggle) {
      return;
    }
    var interval = toggle.getAttribute("data-interval") || toggle.getAttribute("value") || toggle.value || "";
    interval = String(interval).toLowerCase();
    if (interval !== "monthly" && interval !== "yearly") {
      return;
    }
    ygTrack("pricing_toggle", { billing_period: interval });
  }

  function bindSearch() {
    var form = document.querySelector(".md-search__form");
    var input = document.querySelector("[data-md-component='search-query']");
    if (form && !form.dataset.ygSearchBound) {
      form.dataset.ygSearchBound = "1";
      form.addEventListener("submit", function (event) {
        var field = form.querySelector("[data-md-component='search-query']");
        fireSearch(field ? field.value : "");
      });
    }
    if (input && !input.dataset.ygSearchBound) {
      input.dataset.ygSearchBound = "1";
      input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
          fireSearch(input.value);
        }
      });
      input.addEventListener("input", function () {
        if (searchTimer) {
          clearTimeout(searchTimer);
        }
        searchTimer = setTimeout(function () {
          fireSearch(input.value);
        }, 800);
      });
    }
  }

  function bindEngagement() {
    if (document.documentElement.dataset.ygEngageBound) {
      bindSearch();
      return;
    }
    document.documentElement.dataset.ygEngageBound = "1";
    document.addEventListener("click", onDocumentClick, true);
    document.addEventListener("change", onPricingToggle, true);
    document.addEventListener("click", onPricingToggle, true);
    window.addEventListener("scroll", onScrollDepth, { passive: true });
    bindSearch();
    if (document.readyState !== "loading") {
      onScrollDepth();
    } else {
      document.addEventListener("DOMContentLoaded", function () {
        bindSearch();
        onScrollDepth();
      });
    }
  }

  function onConsentGranted() {
    fireDocsPageView();
    fireGoLead();
    onScrollDepth();
    bindSearch();
  }

  function applyConsent(choice) {
    var granted = choice === "granted";
    consentState = granted ? "granted" : "denied";
    window.ygAnalyticsConsent = consentState;
    gtag("consent", "update", Object.assign({
      analytics_storage: granted ? "granted" : "denied",
      functionality_storage: "denied",
      personalization_storage: "denied"
    }, deniedAlways));
    if (granted) {
      loadGaIfConfigured();
      loadCloudflareIfConfigured();
      onConsentGranted();
    }
  }

  function hideBanner(banner) {
    if (banner && banner.parentNode) {
      banner.parentNode.removeChild(banner);
    }
  }

  function showBanner() {
    if (document.getElementById("yg-consent-banner")) {
      return;
    }
    var banner = document.createElement("div");
    banner.id = "yg-consent-banner";
    banner.className = "yg-consent-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-labelledby", "yg-consent-title");
    banner.setAttribute("aria-describedby", "yg-consent-desc");
    banner.innerHTML =
      '<div class="yg-consent-inner">' +
      '<p id="yg-consent-title" class="yg-consent-title">Optional analytics</p>' +
      '<p id="yg-consent-desc" class="yg-consent-desc">' +
      "We use optional, privacy-respecting analytics only if you opt in. " +
      "Advertising and personalization storage stay off. " +
      '<a href="/privacy.html#optional-analytics">Privacy policy</a>.' +
      "</p>" +
      '<div class="yg-consent-actions">' +
      '<button type="button" class="btn ghost" data-yg-consent="denied">Decline</button>' +
      '<button type="button" class="btn primary" data-yg-consent="granted">Accept analytics</button>' +
      "</div>" +
      "</div>";
    document.body.appendChild(banner);
    banner.addEventListener("click", function (event) {
      var target = event.target && event.target.closest
        ? event.target.closest("[data-yg-consent]")
        : null;
      if (!target) {
        return;
      }
      var choice = target.getAttribute("data-yg-consent");
      try {
        localStorage.setItem(YG_CONSENT_STORAGE_KEY, choice);
      } catch (err) {
        /* ignore quota / private mode */
      }
      applyConsent(choice);
      hideBanner(banner);
    });
  }

  bindEngagement();

  var stored = null;
  try {
    stored = localStorage.getItem(YG_CONSENT_STORAGE_KEY);
  } catch (err) {
    stored = null;
  }

  if (stored === "granted" || stored === "denied") {
    applyConsent(stored);
    window.ygAnalyticsReady = Promise.resolve(stored === "granted");
    return;
  }

  // No choice yet: load nothing (no GA tag). Banner asks for opt-in.
  window.ygAnalyticsConsent = "unknown";
  window.ygAnalyticsReady = Promise.resolve(false);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showBanner);
  } else {
    showBanner();
  }
})();
