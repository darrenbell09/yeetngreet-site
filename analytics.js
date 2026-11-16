/*
 * YeetnGreet site analytics — privacy-first, opt-in.
 *
 * - Google Consent Mode defaults start denied; no GA tag loads before consent.
 * - ad_storage, ad_user_data, and ad_personalization stay denied even after opt-in.
 * - After the visitor accepts, GA4 (YG_GA_MEASUREMENT_ID) loads with IP anonymization
 *   and Google ads/signals turned off. Decline keeps the tag unloaded.
 * - Cloudflare Web Analytics stays off while YG_CF_BEACON_TOKEN is empty.
 */
var YG_GA_MEASUREMENT_ID = "G-4QZ4FZPC5X";
var YG_CF_BEACON_TOKEN = "";

var YG_CONSENT_STORAGE_KEY = "yeetngreet-analytics-consent";

(function () {
  var deniedAlways = {
    ad_storage: "denied",
    ad_user_data: "denied",
    ad_personalization: "denied"
  };

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

  function applyConsent(choice) {
    var granted = choice === "granted";
    gtag("consent", "update", Object.assign({
      analytics_storage: granted ? "granted" : "denied",
      functionality_storage: "denied",
      personalization_storage: "denied"
    }, deniedAlways));
    if (granted) {
      loadGaIfConfigured();
      loadCloudflareIfConfigured();
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
  window.ygAnalyticsReady = Promise.resolve(false);
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showBanner);
  } else {
    showBanner();
  }
})();
