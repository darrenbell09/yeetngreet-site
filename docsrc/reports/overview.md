# Reports overview

YeetnGreet reports help you see Microsoft 365 license waste from the same technician PC model as onboard/offboard jobs. You run Graph queries locally, then export or deliver results yourself.

## Report types

| Report | Purpose |
| --- | --- |
| [License audit](license-audit.md) | Who is licensed, mail activity (90d), disabled+licensed and no-mail attention rows |
| [Unused licenses](unused-licenses.md) | Unused prepaid licenses and licenses on disabled accounts |
| [What-if](what-if.md) | Reclaim savings plus named scenario planning (moves, hires, cuts) |
| [Samples](samples.md) | Anonymized example output |

In the app these appear together on **Reports** after you run a **license report** — not as separate menu items.

## How to run

1. Select the managed tenant and **sign in**
2. Open **Reports** → **Run license report**
3. Review **User licensing** (audit) and **What-if** (reclaim + scenario planner)
4. Edit unit costs on the what-if card and **Save costs** for a saved tenant price
5. Optionally build a named scenario, then export HTML/PDF, [schedule](../jobs/schedules.md) a recurring run, or send via [Delivery](delivery.md)

![Screenshot: Reports — license audit](../assets/images/reports-license-audit.png){ width="720" }
*Placeholder — license audit summary in the app.*

!!! note "Plans"
    **Free** includes a limited license-report **preview** (bucketed savings, no SKU/$ detail or named users). Full SKU tables, exact savings, named users, scenario export, and deliveries are on paid plans. See [Pricing and licensing](../pricing-and-licensing.md).

!!! note "Data path"
    Report queries use Microsoft Graph from the technician PC (`Reports.Read.All` for mail activity). Exports and delivery stay under your control — YeetnGreet does not host a data lake of customer report content. What-if scenarios are projections only; they never change licenses in the tenant.

## Related

- [Pricing and licensing](../pricing-and-licensing.md)
- [Delivery](delivery.md)
