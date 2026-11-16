# yeetngreet-marketing

Marketing opt-in Worker for yeetngreet.app. Lives on the YeetnGreet
business Cloudflare account, with its own D1 database, on the free
tier. The public URL is the workers.dev hostname only — do not add a
custom domain, route, or DNS record, and do not touch darrenbell.net.

- Worker: `yeetngreet-marketing`
- URL: `https://yeetngreet-marketing.darren-c9b.workers.dev`
- D1: `yeetngreet-marketing` (`1799af3b-2a74-47c1-aeac-352bd1d04524`)
- Binding: `DB`
- Methods: `POST` (and `OPTIONS` for CORS preflight)
- Allowed origin: `https://yeetngreet.app`
- No public read or list endpoint

## Export the mailing list

From this directory, with the business account API token in
`CLOUDFLARE_API_TOKEN` (do not print the token):

```bash
npx wrangler d1 execute yeetngreet-marketing --remote --command "SELECT email, consented_at, source, source_path, consent_text, created_at, unsubscribed_at FROM marketing_subscribers ORDER BY created_at;"
```

## Deploy

```bash
npx wrangler deploy
```

The table is already created on the remote D1 database. Re-apply the
schema only if you need to, with:

```bash
npx wrangler d1 execute yeetngreet-marketing --remote --file=./schema.sql
```
