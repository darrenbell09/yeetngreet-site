# Unused licenses

Find prepaid seats that are not assigned, and licenses still stuck on **disabled** accounts — before the renewal meeting.

In the app this is the **Unused** / **Disabled** columns on the license report’s **What-if savings** table (not a separate Reports submenu).

## Signals

| Signal | Meaning |
| --- | --- |
| **Unused** | Prepaid enabled seats minus consumed (available capacity you are still paying for) |
| **Disabled** | License assignments on accounts with sign-in blocked |
| **No mail (90d)** | Enabled licensed users with no send/receive/read in the mail activity window — shown under **User licensing** for review, not as unused inventory |

## When to use it

- Monthly license hygiene
- After offboard waves (catch stragglers still licensed while disabled)
- When finance asks “where can we cut?”

## Steps

1. Select the tenant and sign in
2. Open **Reports** → **Run license report**
3. On **What-if savings**, review Unused and Disabled per SKU
4. Open **User licensing** for named disabled+licensed and no-mail users
5. Validate in the Microsoft 365 admin center before you remove SKUs or reduce quantities
6. Export or [deliver](delivery.md) if needed

![Screenshot: Reports — unused licenses](../assets/images/reports-unused-licenses.png){ width="720" }
*Example screenshot — idle licenses with per-SKU savings. Marketing sample numbers are synthetic and checked so row math totals correctly.*

!!! warning "Validate before reclaim"
    Unused and disabled signals are a starting point. Confirm with your process (shared mailboxes, break-glass accounts, seasonal staff) before you remove SKUs. Sample savings on the marketing site are **examples only — not a guarantee**.

## Pricing the reclaim

Pair this view with [What-if savings](what-if.md): set unit costs, then read **Savings / mo** = `(Unused + Disabled) × Unit` per SKU.

## Related

- [What-if savings](what-if.md)
- [License audit](license-audit.md)
- [Samples](samples.md)
