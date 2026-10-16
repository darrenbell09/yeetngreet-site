# What-if savings

Project **potential monthly reclaim** from license waste on the signed-in tenant — before you cut prepaid seats or clean up disabled accounts.

What-if is part of the **license report** on the Reports page. It is not a separate scenario builder: there is no named “move users to SKU B” model yet. The projection prices two reclaim buckets at your unit costs (or US list estimates until you save costs on the tenant).

## What it calculates

| Bucket | Meaning | How it is priced |
| --- | --- | --- |
| **Unused prepaid seats** | Seats you pay for that are not assigned (`enabled − consumed`) | Unused count × unit cost / mo |
| **Disabled + licensed** | Licenses still assigned to **blocked** accounts | Disabled-assigned count × unit cost / mo |

**Potential monthly savings** = unused seat cost + disabled-assigned cost, summed across SKUs.

### What is *not* priced in what-if

**Inactive licensed users** (enabled, but no mail send/receive/read in the last 90 days) appear under **User licensing** so you can review them. They are **not** added into what-if dollars. Those users still consume a prepaid seat; pricing them separately on top of “unused” would double-count the same capacity.

## When to use it

- Renewal or true-up prep — “how much are unused and disabled seats costing us?”
- After offboard waves — catch licenses left on disabled accounts
- Finance asks for a reclaim range before you change quantities in the admin center

## Steps

1. Select the managed tenant and **sign in** (customer Graph token).
2. Open **Reports**.
3. Click **Run license report**.
4. Open the **What-if savings** card:
   - Review per-SKU **Unused**, **Disabled**, **Unit / mo**, and **Savings / mo**
   - Edit unit costs if the list estimate is wrong for your agreement
   - Click **Save costs** to store costs on this managed tenant (reused on the next run)
5. Optionally export **HTML** / **PDF**, or [schedule](../jobs/schedules.md) / [deliver](delivery.md) recurring reports

!!! tip "Unit costs"
    Graph does not expose your invoice unit price. YeetnGreet prefers **tenant-saved** costs, then falls back to **US direct-purchase list estimates**. Always validate against your Microsoft bill before committing to a cut.

## Reading the summary

After a full (paid) report, the what-if summary looks like:

> Potential monthly savings: **USD X** (unused **A** + disabled-assigned **B**). Costs: *n* from tenant, *m* list estimate…

Community / Free preview shows a **savings bucket** (for example `$200–$500/mo`) without SKU-level dollars or named users — upgrade for full detail and exports.

## Related

- [Unused licenses](unused-licenses.md) — how unused and disabled signals are found
- [License audit](license-audit.md) — assigned users, including no-mail attention rows
- [Samples](samples.md) — anonymized numbers with checked arithmetic
- [Pricing and licensing](../pricing-and-licensing.md)
