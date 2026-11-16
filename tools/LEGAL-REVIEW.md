# Legal review — site pages (draft)

These notes are for Darren and a lawyer. They are not customer-facing.
This PR must stay unmerged until it is reviewed; merging publishes the site.

The pages themselves use only facts already in the repos or on the live
site. Items below are gaps, ambiguities, or lawyer questions — not new
commitments.

## What this PR changes

- **Terms** (`terms.html`): already existed. Adds the 14-day trial on paid
  plans, points at the new EULA, and clarifies that product support is
  email-only at support@yeetngreet.app, while Paddle (Merchant of Record)
  handles billing, receipts, taxes, and refunds.
- **Privacy** (`privacy.html`): already existed and already covered
  opt-in GA4, marketing emails, Paddle, and GitHub Pages. Adds that
  YeetnGreet LLC is a Louisiana limited liability company, and that
  support is email-only.
- **Refunds** (`refunds.html`): already existed (30-day money-back on
  first paid purchase; Paddle processes refunds). Adds a short 14-day
  trial section and the same support / Paddle split.
- **EULA** (`eula.html`): new. The license grant, licensed-user definition,
  proprietary-software restriction, and acceptable use are copied from
  Terms §§2–3 and §6. Warranty, liability, termination, and Louisiana
  governing law are incorporated by reference to the Terms rather than
  rewritten.

Paddle as Merchant of Record already required Terms, Privacy, and a
Refund policy to be reachable from the site. Those three were already
linked in the marketing footer. The EULA is additional.

## Needs legal review

1. **14-day trial mechanics.** The Worker and site copy say paid plans
   include a 14-day trial. This draft does **not** state whether a payment
   method is required to start the trial, when the first charge happens,
   or whether Paddle's trial and the Worker trial are the same period.
   Confirm those facts before publication, then say them plainly.
2. **Trial vs 30-day money-back.** The refund policy still starts the
   30-day guarantee at "your first purchase of a paid plan." Confirm
   whether a trial that converts to a paid charge is that first purchase,
   and whether days in trial count toward the 30 days.
3. **Paddle buyer-support boilerplate.** The previous Terms said Paddle
   "provides all customer service inquiries and handles returns." Product
   policy is that YeetnGreet support is email-only at
   support@yeetngreet.app. This draft splits product support (us) from
   billing and refunds (Paddle). Confirm that split matches the Paddle
   merchant agreement.
4. **No street address.** Pages name YeetnGreet LLC, a Louisiana limited
   liability company, and support@yeetngreet.app. No mailing address is
   given because none is in the repos. Add one if counsel or Paddle
   requires it.
5. **EULA vs Terms overlap.** The EULA restates the license grant and
   defers warranty, liability, and governing law to the Terms, and says
   the Terms control if the two conflict. Counsel may prefer a single
   document, or a standalone EULA with the warranty language copied in
   full.
6. **International / consumer law.** Terms and Refunds already say they
   do not limit non-waivable consumer rights where the customer lives.
   Confirm whether further GDPR, CCPA, or withdrawal-right language is
   required for Paddle-sold subscriptions.
7. **Data retention, children, and data-subject requests.** Privacy
   describes what is stored and how to email for waitlist or marketing
   changes. It does not state retention periods, an age limit, or a
   formal data-subject request process. Do not invent those in copy
   until they are decided.
8. **Effective date.** Changed pages are dated November 16, 2026. If
   publication slips, update the date on merge.

## Sources used (no new facts invented)

- Existing `terms.html`, `privacy.html`, and `refunds.html` on site main.
- PLAN.md pricing, 14-day trial, Louisiana LLC, email-only support,
  "licensed users," Free, and Paddle as Merchant of Record.
- Live site footer already linked Terms, Refunds, and Privacy from
  marketing pages.
