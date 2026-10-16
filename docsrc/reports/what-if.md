# What-if

Plan license changes **before** you touch the admin center. What-if lives on the **Reports** page after you run a license report. It is **read-only** — nothing in the tenant changes.

The same card has two layers:

1. **Reclaim savings** — price unused prepaid licenses and licenses on disabled accounts
2. **Scenario planner** — name a plan, stack steps, see before/after counts and cost deltas

## Price sources

Unit costs power both reclaim and scenarios. Graph does not expose your invoice price. Each SKU shows where the number came from:

| Label | Meaning |
| --- | --- |
| **list-price estimate** | US direct-purchase list fallback until you save |
| **enter cost** | You edited the unit cost but have not saved yet |
| **saved tenant price** | Stored on this managed tenant after **Save costs** |

Always validate against your Microsoft bill before committing to a cut or buy.

## Reclaim savings

| Bucket | Meaning | How it is priced |
| --- | --- | --- |
| **Unused prepaid licenses** | Enabled licenses you pay for that are not assigned (`enabled − consumed`) | Unused count × unit cost / mo |
| **Disabled + licensed** | Licenses still assigned to **blocked** accounts | Disabled-assigned count × unit cost / mo |

**Potential monthly savings** = unused cost + disabled-assigned cost, summed across SKUs.

### What is *not* priced in reclaim

**Inactive licensed users** (enabled, but no mail send/receive/read in the last 90 days) appear under **User licensing** so you can review them. They are **not** added into reclaim dollars because inactive is **not confirmed waste** — someone may still need that license.

## Scenario planner

Start from the tenant’s current licenses (from the latest full report) and build a named scenario:

| Step | What it models |
| --- | --- |
| **Remove unused licenses** | Drop prepaid capacity that is not assigned (blank quantity = all) |
| **Remove disabled-assigned licenses** | Unassign licenses from blocked accounts |
| **Move licenses (SKU → SKU)** | Move N users/licenses from one SKU to another (for example E3 → Business Premium) |
| **Add licenses (planned hires)** | Increase prepaid + assigned for upcoming headcount |
| **Remove licenses (planned cuts)** | Reduce prepaid + assigned for planned reductions |

For each scenario the app shows:

- Before / after **prepaid enabled** license counts per SKU
- Unit cost with its **price source** label
- Monthly and annual **cost difference** (after − before)

Scenarios are saved **per managed tenant**, can be reopened later, and export or [deliver](delivery.md) like other reports (HTML, CSV, optional PDF). Delivery uses the tenant’s existing channels.

!!! tip "Keep scenarios named"
    Use clear names (“Q4 reclaim + E3→Business Premium”) so the next tech on the account can reuse them.

## When to use it

- Renewal or true-up prep — reclaim unused and disabled licenses
- Quote a right-size move (E3 → Business Premium) before you buy
- Model planned hires or cuts without changing Graph
- Pair with [unused licenses](unused-licenses.md) and the [license audit](license-audit.md)

## Steps

1. Select the managed tenant and **sign in** (customer Graph token).
2. Open **Reports** → **Run license report**.
3. On **What-if savings**:
   - Review reclaim **Unused**, **Disabled**, **Unit / mo**, and **Savings / mo**
   - Edit unit costs if needed; click **Save costs** for a saved tenant price
4. In **Scenario planner**:
   - Name the scenario and add steps
   - Review before/after counts and monthly/annual deltas
   - **Save** to store on this tenant, or **Open** a saved scenario
5. Optionally **Export** / **Export PDF**, or [deliver](delivery.md) via the tenant’s report channels

Community / Free preview shows a **savings bucket** without SKU-level dollars, named users, or scenario export — upgrade for full detail.

## Related

- [Unused licenses](unused-licenses.md) — how unused and disabled signals are found
- [License audit](license-audit.md) — assigned users, including no-mail attention rows
- [Samples](samples.md) — anonymized numbers with checked arithmetic
- [Pricing and licensing](../pricing-and-licensing.md)
