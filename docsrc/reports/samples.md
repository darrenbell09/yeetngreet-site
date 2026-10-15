# Sample report output

Anonymized examples of what reports can look like. Your tenant names, SKUs, and counts will differ.

!!! note "Example only — not a guarantee"
    Figures below are synthetic demos for documentation. Always validate in the tenant before reclaiming. Savings shown here are illustrative, not promised results.

## License audit (excerpt)

| SKU | Assigned | Available | Notes |
| --- | ---: | ---: | --- |
| Microsoft 365 E3 | 520 | 140 | Core productivity |
| Microsoft 365 Business Premium | 180 | 40 | Field + branch |
| Power BI Pro | 210 | 55 | Finance + ops |
| Exchange Online Plan 2 | 95 | 25 | Shared / legacy |
| Visio Plan 2 | 85 | 20 | Engineering |

**Named users (sample rows)**

| Display name | UPN | SKUs |
| --- | --- | --- |
| Alex Rivera | alex.rivera@contoso-example.com | M365 E3 |
| Jordan Lee | jordan.lee@contoso-example.com | M365 E3; Power BI Pro |
| Sam Okonkwo | sam.okonkwo@contoso-example.com | Exchange Online Plan 2 |

## Unused licenses (excerpt)

Savings per row = (Unused + Disabled) × Unit. The homepage sample uses the same arithmetic.

| License | Unused | Disabled | Unit | Savings / mo |
| --- | ---: | ---: | ---: | ---: |
| Microsoft 365 E3 | 140 | 30 | 36.00 | 6,120.00 |
| Microsoft 365 Business Premium | 40 | 10 | 22.00 | 1,100.00 |
| Power BI Pro | 55 | 9 | 10.00 | 640.00 |
| Exchange Online (Plan 2) | 25 | 5 | 8.00 | 240.00 |
| Visio Plan 2 | 20 | 4 | 15.00 | 360.00 |
| **Total** | **280** | **58** | | **8,460.00** |

**Check:** `(140+30)×36 + (40+10)×22 + (55+9)×10 + (25+5)×8 + (20+4)×15 = 8,460`.

Against an estimated monthly license cost of **USD 28,200** for **940** licensed users, potential savings are **exactly 30%** (`8,460 ÷ 28,200`). Disabled column total (**58**) matches the licensed + disabled KPI.

## What-if (excerpt)

```text
Scenario: Q4 reclaim wave
- Remove unused + disabled capacity above (280 unused, 58 disabled)
- Keep active licensed users unchanged
Projected monthly reclaim: USD 8,460 (list unit costs; customer price may differ)
Share of estimated spend: 30%
```

## Related

- [License audit](license-audit.md)
- [Unused licenses](unused-licenses.md)
- [What-if](what-if.md)
