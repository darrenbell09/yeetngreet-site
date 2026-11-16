/*
 * Optional marketing-email opt-in on /go/waitlist/ and /go/founding/.
 *
 * Waitlist answers still go to the existing Google Form. This script only
 * submits an email to the first-party marketing list when the visitor ticks
 * the unticked consent box. Posts to the yeetngreet-marketing Worker
 * (see worker/marketing/). Never send the email address to Google Analytics.
 */
var YG_GOOGLE_FORM_URL =
  "https://docs.google.com/forms/d/e/1FAIpQLSddlwVg9FklzgEKhfQf8RRNzlv9BNJipgWBOsotXISDmg5OTw/viewform";
var YG_GOOGLE_FORM_EMAIL_ENTRY = "824231051";
var YG_MARKETING_SUBSCRIBE_URL =
  "https://yeetngreet-marketing.darren-c9b.workers.dev";
var YG_MARKETING_CONSENT_TEXT = "Email me YeetnGreet news and updates";

(function () {
  var form = document.getElementById("yg-signup-form");
  if (!form) {
    return;
  }
  var optIn = document.getElementById("yg-marketing-optin");
  var emailWrap = document.getElementById("yg-marketing-email-wrap");
  var emailInput = document.getElementById("yg-marketing-email");
  var honeypot = document.getElementById("yg-marketing-website");
  var errorEl = document.getElementById("yg-marketing-error");
  var source = form.getAttribute("data-yg-source") || "waitlist";
  var gone = false;

  function showEmailField() {
    var on = !!(optIn && optIn.checked);
    if (emailWrap) {
      if (on) {
        emailWrap.removeAttribute("hidden");
      } else {
        emailWrap.setAttribute("hidden", "");
      }
    }
    if (emailInput) {
      emailInput.required = on;
      if (!on) {
        emailInput.value = "";
      }
    }
    if (errorEl) {
      errorEl.textContent = "";
    }
  }

  function validEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(value || "").trim());
  }

  function googleFormUrl(email) {
    var url = YG_GOOGLE_FORM_URL;
    if (email && YG_GOOGLE_FORM_EMAIL_ENTRY) {
      url +=
        (url.indexOf("?") >= 0 ? "&" : "?") +
        "usp=pp_url&entry." +
        encodeURIComponent(YG_GOOGLE_FORM_EMAIL_ENTRY) +
        "=" +
        encodeURIComponent(email);
    }
    return url;
  }

  function goToForm(email) {
    if (gone) {
      return;
    }
    gone = true;
    window.location.assign(googleFormUrl(email));
  }

  function marketingPayload(email) {
    return {
      email: String(email || "").trim(),
      consent: true,
      consented_at: new Date().toISOString(),
      source: source,
      source_path: window.location.pathname || "",
      consent_text: YG_MARKETING_CONSENT_TEXT,
      website: honeypot ? String(honeypot.value || "") : ""
    };
  }

  // Exported for tests. Must never be passed to gtag / ygTrack.
  window.ygMarketingPayload = marketingPayload;

  function subscribeMarketing(email) {
    if (!YG_MARKETING_SUBSCRIBE_URL) {
      return Promise.resolve({ stored: false, reason: "endpoint_not_configured" });
    }
    return fetch(YG_MARKETING_SUBSCRIBE_URL, {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify(marketingPayload(email))
    }).then(function (res) {
      return { stored: res.ok, reason: res.ok ? "ok" : "http_" + res.status };
    }).catch(function () {
      return { stored: false, reason: "network" };
    });
  }

  if (optIn) {
    optIn.checked = false;
    optIn.addEventListener("change", showEmailField);
    showEmailField();
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (errorEl) {
      errorEl.textContent = "";
    }
    var opted = !!(optIn && optIn.checked);
    var email = emailInput ? String(emailInput.value || "").trim() : "";
    if (opted && !validEmail(email)) {
      if (errorEl) {
        errorEl.textContent = "Enter a work email to get news and updates, or untick the box to continue without joining the mailing list.";
      }
      if (emailInput) {
        emailInput.focus();
      }
      return;
    }
    // Analytics: only the existing generate_lead handoff (no email, no field values).
    if (typeof window.ygTrack === "function") {
      window.ygTrack("generate_lead", {
        lead_type: source,
        method: opted ? "form_redirect_with_marketing_intent" : "form_redirect"
      });
    }
    var continueEmail = opted ? email : "";
    if (!opted) {
      goToForm("");
      return;
    }
    subscribeMarketing(email).then(function () {
      goToForm(continueEmail);
    });
  });
})();
