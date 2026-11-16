# Marketing email subscribe

Waitlist and founding-beta answers still go to the existing Google Form
(YeetnGreet Founding Beta). Marketing opt-in is a separate, explicit
checkbox on `/go/waitlist/` and `/go/founding/`. `marketing.js` posts only
when the visitor ticks “Email me YeetnGreet news and updates”.

## Deployed Worker

- Worker name: `yeetngreet-marketing`
- Account: YeetnGreet business Cloudflare account (same as `yeetngreet-license-api`)
- URL (workers.dev only; no custom domain or DNS changes):
  `https://yeetngreet-marketing.darren-c9b.workers.dev`
- D1 database: `yeetngreet-marketing` (`1799af3b-2a74-47c1-aeac-352bd1d04524`)
- Source: `worker/marketing/`
- Free tier only. POST only. CORS limited to `https://yeetngreet.app`.
- No public read or list endpoint. Export through Wrangler:

```bash
npx wrangler d1 execute yeetngreet-marketing --remote --command "SELECT email, consented_at, source, source_path, consent_text, created_at, unsubscribed_at FROM marketing_subscribers ORDER BY created_at;"
```

Run that from `worker/marketing/` with the business account API token and
the `wrangler.jsonc` in that folder (it already has the account id).

## Payload

```json
{
  "email": "person@example.com",
  "consent": true,
  "consented_at": "2026-11-15T19:30:00.000Z",
  "source": "waitlist",
  "source_path": "/go/waitlist/",
  "consent_text": "Email me YeetnGreet news and updates",
  "website": ""
}
```

`website` is a honeypot; leave it empty. The Worker lowercases the email,
requires `consent=true`, upserts on email (idempotent), and stores
`unsubscribed_at` (null until someone unsubscribes). Until a one-click
unsubscribe ships, people can email support@yeetngreet.app.

Do not send these addresses to Google Analytics, and do not log emails
in the Worker.
