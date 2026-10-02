# Support

Need help with YeetnGreet? Start with the docs, then email us. This page is for **MSPs and IT admins** running the Windows app against customer Microsoft 365 tenants.

## How to get help

Email **[support@yeetngreet.app](mailto:support@yeetngreet.app)**.

That is the public support address. Please do **not** open GitHub Issues for product support — the application repository is private, and Issues are not a customer support channel.

## Check the docs first

Many how-tos are already covered here:

| Topic | Docs |
| --- | --- |
| Download and launch | [Install](getting-started/install.md) |
| First tenant sign-in and preview | [First run](getting-started/first-run.md) |
| Offboard / onboard / schedules | [Jobs](jobs/offboard.md) |
| License and unused-seat reports | [Reports](reports/overview.md) |
| Switching customers | [Multi-tenant](tenants/multi-tenant.md) |
| Plans and limits | [Pricing and licensing](pricing-and-licensing.md) |
| What we store | [Privacy](privacy.md) |

If the docs answer it, you save a round-trip — and we can spend support time on the harder cases.

## What to include in your email

The more context you send up front, the faster we can help. Please include:

1. **App version** — Help → About in YeetnGreet (or the version shown on the About screen)
2. **Windows version** — for example Windows 11 23H2, or `winver` output
3. **Plan** — Community, Team, or MSP (Founding if applicable)
4. **Tenant domain** — the customer Microsoft 365 domain you were working in (for example `contoso.com`), not passwords or secrets
5. **Steps to reproduce** — what you clicked or ran, what you expected, and what happened
6. **Screenshots** — if the issue is in the UI (redact customer PII where you can)

!!! tip "Do not send secrets"
    Do not include passwords, refresh tokens, client secrets, or full mailbox contents. Tenant domain and a short error message are enough for most Graph failures.

## Response expectations

We monitor **support@yeetngreet.app** and reply on **business days**. Timing varies with volume and how much detail is in the initial email — we do not publish a formal SLA here.

Urgent production blockers still go to the same address; put a clear subject line (for example `MSP offboard blocked — Graph 403`) so we can prioritize.

## Related

- [Install](getting-started/install.md)
- [Pricing and licensing](pricing-and-licensing.md)
- [Homepage](https://yeetngreet.app/)
