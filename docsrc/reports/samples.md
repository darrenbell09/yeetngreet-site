# Sample report output

Anonymized examples of what reports can look like. Your tenant names, SKUs, and counts will differ.

!!! note "Example only — not a guarantee"
    Figures below are synthetic demos for documentation. Always validate in the tenant before reclaiming. Savings shown here are illustrative, not promised results.

## License audit (excerpt)

| SKU | Assigned | Available | Notes |
| --- | ---: | ---: | --- |
| Microsoft 365 Business Premium | 180 | 6 | Field + branch |
| Microsoft 365 E3 | 60 | 4 | Leadership / HQ |
| Microsoft 365 Business Standard | 40 | 2 | Light roles |

**Attention rows (sample)**

| Display name | UPN | Issue | SKUs |
| --- | --- | --- | --- |
| Jordan Blake | jordan.blake@northshore.example | Disabled + licensed | Business Premium |
| Alex Morgan | alex.morgan@northshore.example | Disabled + licensed | E3 |
| Sam Rivera | sam.rivera@northshore.example | No mail activity (90d) | Business Premium |
| Casey Nguyen | casey.nguyen@northshore.example | No mail activity (90d) | Business Standard |

## What-if savings (excerpt)

Savings / mo = `(Unused + Disabled) × Unit`. Inactive (no-mail) users are **not** priced in this table.

| License | Unused | Disabled | Unit | Savings / mo |
| --- | ---: | ---: | ---: | ---: |
| Microsoft 365 Business Premium | 6 | 24 | 22.00 | 660.00 |
| Microsoft 365 E3 | 4 | 12 | 36.00 | 576.00 |
| Microsoft 365 Business Standard | 2 | 5 | 12.50 | 87.50 |
| **Total** | **12** | **41** | | **1,323.50** |

**Check:** `(6+24)×22 + (4+12)×36 + (2+5)×12.50 = 660 + 576 + 87.50 = 1,323.50`.

Estimated monthly spend for **280** licensed users (180×$22 + 60×$36 + 40×$12.50) = **USD 6,620**.

## Related

- [License audit](license-audit.md)
- [Unused licenses](unused-licenses.md)
- [What-if savings](what-if.md)
