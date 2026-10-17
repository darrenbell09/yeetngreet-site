# Unused licenses

Find prepaid licenses that are not assigned, and licenses still stuck on **disabled** accounts — before the renewal meeting.

In the app this is the **Unused** / **Disabled** columns on the license report’s **What-if** table (not a separate Reports submenu).

## Signals

| Signal | Meaning |
| --- | --- |
| **Unused** | Prepaid enabled licenses minus consumed (available capacity you are still paying for) |
| **Disabled** | License assignments on accounts with sign-in blocked |
| **No mail (90d)** | Enabled licensed users with no send/receive/read in the mail activity window — shown under **User licensing** for review. Not priced as reclaim because inactive is not confirmed waste. |

## When to use it

- Monthly license hygiene
- After offboard waves (catch stragglers still licensed while disabled)
- When finance asks “where can we cut?”

## Steps

1. Select the tenant and sign in
2. Open **Reports** → **Run license report**
3. On **What-if**, review Unused and Disabled per SKU
4. Open **User licensing** for named disabled+licensed and no-mail users
5. Validate in the Microsoft 365 admin center before you remove SKUs or reduce quantities
6. Export or [deliver](delivery.md) if needed

![What-if savings table for Contoso listing each license with its unused and disabled counts, unit price, and monthly savings](../assets/images/whatif-savings.png){ width="720" }
*Unused and Disabled columns per license, with the monthly savings for each.*

![User licensing table for Contoso listing seven disabled accounts that still hold licenses and one enabled user with no mail activity, each with their sign-in status, mail counts, and licenses](../assets/images/reports-unused-licenses.png){ width="720" }
*User licensing names the people behind the numbers: disabled but still licensed, or no mail in 90 days.*

!!! warning "Validate before reclaim"
    Unused and disabled signals are a starting point. Confirm with your process (shared mailboxes, break-glass accounts, seasonal staff) before you remove SKUs. Sample savings on the marketing site are **examples only — not a guarantee**.

## Pricing the reclaim

Pair this view with [What-if](what-if.md): set unit costs, then read **Savings / mo** for each license (unused plus disabled licenses, times the unit price). Use the scenario planner on the same card to model reclaim steps without changing the tenant.

## Related

- [What-if](what-if.md)
- [License audit](license-audit.md)
- [Sample reports](samples.md)
