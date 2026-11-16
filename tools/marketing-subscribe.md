# Marketing email subscribe (design only — not deployed)

Waitlist and founding-beta answers already go to the existing Google Form
(YeetnGreet Founding Beta). That form is the only place emails are stored
today. There is no first-party mailing-list backend yet.

This site can collect a separate, explicit marketing opt-in from
`/go/waitlist/` and `/go/founding/`. `marketing.js` posts only when the
visitor ticks “Email me YeetnGreet news and updates”. The payload is:

```json
{
  "email": "person@example.com",
  "consented_at": "2026-11-15T19:30:00.000Z",
  "source": "waitlist",
  "source_path": "/go/waitlist/",
  "consent_text": "Email me YeetnGreet news and updates"
}
```

`YG_MARKETING_SUBSCRIBE_URL` in `marketing.js` is left empty on purpose.
Do not deploy this Worker until Darren goes ahead.

## Proposed Worker + D1

- Cloudflare Worker on the business account, for example
  `POST https://api.yeetngreet.app/v1/marketing/subscribe`.
- Validate a single email, require `consented_at`, `source`
  (`waitlist` or `founding`), `source_path`, and the exact consent text.
- Reject requests that do not include a checked opt-in equivalent; the
  site only posts when the box is ticked.
- Store in D1, for example:

```sql
CREATE TABLE marketing_subscribers (
  email TEXT PRIMARY KEY COLLATE NOCASE,
  consented_at TEXT NOT NULL,
  source TEXT NOT NULL,
  source_path TEXT,
  consent_text TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  unsubscribed_at TEXT
);
```

- Upsert by email; do not insert when the box was not ticked.
- `POST /v1/marketing/unsubscribe` (and later a signed one-click link)
  sets `unsubscribed_at`. Until that ships, people can email
  support@yeetngreet.app.
- Do not send these addresses to Google Analytics or include them in
  Worker logs beyond operational error handling.
- After the Worker is live, set `YG_MARKETING_SUBSCRIBE_URL` to that
  endpoint and deploy the site change separately (needs a publish go).
