/**
 * YeetnGreet marketing opt-in Worker.
 * POST only. CORS limited to https://yeetngreet.app.
 * Never log email addresses or request bodies.
 */

const ALLOWED_ORIGIN = "https://yeetngreet.app";
const MAX_BODY_BYTES = 4096;
const RATE_LIMIT_WINDOW_MS = 60_000;
const RATE_LIMIT_MAX = 8;
const EMAIL_MAX = 254;
const TEXT_MAX = 200;
const PATH_MAX = 200;
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const ALLOWED_SOURCES = new Set(["waitlist", "founding"]);
const ALLOWED_PATHS = new Set(["/", "/v1/marketing/subscribe"]);

/** @type {Map<string, { start: number, count: number }>} */
const rateByIp = new Map();

function corsHeaders(request) {
  const origin = request.headers.get("Origin") || "";
  if (origin !== ALLOWED_ORIGIN) {
    return {};
  }
  return {
    "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type, accept",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function jsonResponse(request, status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      ...corsHeaders(request),
    },
  });
}

function clientIp(request) {
  return request.headers.get("CF-Connecting-IP") || "unknown";
}

function rateLimited(ip) {
  const now = Date.now();
  if (rateByIp.size > 2000) {
    for (const [key, rec] of rateByIp) {
      if (now - rec.start >= RATE_LIMIT_WINDOW_MS) {
        rateByIp.delete(key);
      }
    }
  }
  const rec = rateByIp.get(ip);
  if (!rec || now - rec.start >= RATE_LIMIT_WINDOW_MS) {
    rateByIp.set(ip, { start: now, count: 1 });
    return false;
  }
  rec.count += 1;
  return rec.count > RATE_LIMIT_MAX;
}

function isTruthyConsent(value) {
  return value === true || value === "true";
}

function honeypotFilled(body) {
  const fields = ["website", "hp", "company_url"];
  for (const key of fields) {
    if (typeof body[key] === "string" && body[key].trim() !== "") {
      return true;
    }
  }
  return false;
}

function normalizeEmail(value) {
  if (typeof value !== "string") {
    return "";
  }
  return value.trim().toLowerCase();
}

function validEmail(email) {
  return email.length > 0 && email.length <= EMAIL_MAX && EMAIL_RE.test(email);
}

function clip(value, max) {
  if (typeof value !== "string") {
    return "";
  }
  return value.trim().slice(0, max);
}

function normalizeConsentedAt(value) {
  if (typeof value === "string" && value.trim()) {
    const ms = Date.parse(value);
    if (!Number.isNaN(ms)) {
      return new Date(ms).toISOString();
    }
  }
  return new Date().toISOString();
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const headers = corsHeaders(request);

    if (request.method === "OPTIONS") {
      if (!ALLOWED_PATHS.has(url.pathname)) {
        return new Response(null, { status: 404, headers });
      }
      if (request.headers.get("Origin") && request.headers.get("Origin") !== ALLOWED_ORIGIN) {
        return new Response(null, { status: 403 });
      }
      return new Response(null, { status: 204, headers });
    }

    if (request.method !== "POST") {
      return jsonResponse(request, 405, { ok: false, error: "method_not_allowed" });
    }

    if (!ALLOWED_PATHS.has(url.pathname)) {
      return jsonResponse(request, 404, { ok: false, error: "not_found" });
    }

    if (rateLimited(clientIp(request))) {
      return new Response(JSON.stringify({ ok: false, error: "rate_limited" }), {
        status: 429,
        headers: {
          "content-type": "application/json; charset=utf-8",
          "Retry-After": "60",
          ...headers,
        },
      });
    }

    const declaredLength = Number(request.headers.get("content-length") || "0");
    if (declaredLength > MAX_BODY_BYTES) {
      return jsonResponse(request, 413, { ok: false, error: "payload_too_large" });
    }

    let raw;
    try {
      raw = await request.arrayBuffer();
    } catch {
      return jsonResponse(request, 400, { ok: false, error: "invalid_body" });
    }
    if (raw.byteLength > MAX_BODY_BYTES) {
      return jsonResponse(request, 413, { ok: false, error: "payload_too_large" });
    }

    let body;
    try {
      body = JSON.parse(new TextDecoder().decode(raw));
    } catch {
      return jsonResponse(request, 400, { ok: false, error: "invalid_json" });
    }
    if (body === null || typeof body !== "object" || Array.isArray(body)) {
      return jsonResponse(request, 400, { ok: false, error: "invalid_json" });
    }

    if (honeypotFilled(body)) {
      return jsonResponse(request, 200, { ok: true });
    }

    if (!isTruthyConsent(body.consent)) {
      return jsonResponse(request, 400, { ok: false, error: "consent_required" });
    }

    const email = normalizeEmail(body.email);
    if (!validEmail(email)) {
      return jsonResponse(request, 400, { ok: false, error: "invalid_email" });
    }

    const source = clip(body.source, TEXT_MAX);
    if (!ALLOWED_SOURCES.has(source)) {
      return jsonResponse(request, 400, { ok: false, error: "invalid_source" });
    }

    const consentText = clip(body.consent_text, TEXT_MAX);
    if (!consentText) {
      return jsonResponse(request, 400, { ok: false, error: "invalid_consent_text" });
    }

    const sourcePath = clip(body.source_path, PATH_MAX);
    const consentedAt = normalizeConsentedAt(body.consented_at);

    try {
      await env.DB.prepare(
        `INSERT INTO marketing_subscribers (
            email, consented_at, source, source_path, consent_text, created_at, unsubscribed_at
          ) VALUES (?, ?, ?, ?, ?, datetime('now'), NULL)
          ON CONFLICT(email) DO UPDATE SET
            consented_at = excluded.consented_at,
            source = excluded.source,
            source_path = excluded.source_path,
            consent_text = excluded.consent_text,
            unsubscribed_at = NULL`
      )
        .bind(email, consentedAt, source, sourcePath || null, consentText)
        .run();
    } catch {
      return jsonResponse(request, 500, { ok: false, error: "store_failed" });
    }

    return jsonResponse(request, 200, { ok: true });
  },
};
