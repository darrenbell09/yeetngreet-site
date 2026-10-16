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

## What-if reclaim savings (excerpt)

Savings / mo = `(Unused + Disabled) × Unit`. Inactive (no-mail) users are **not** priced here — inactive is not confirmed waste.

| License | Unused | Disabled | Unit | Price source | Savings / mo |
| --- | ---: | ---: | ---: | --- | ---: |
| Microsoft 365 Business Premium | 6 | 24 | 22.00 | saved tenant price | 660.00 |
| Microsoft 365 E3 | 4 | 12 | 36.00 | list-price estimate | 576.00 |
| Microsoft 365 Business Standard | 2 | 5 | 12.50 | enter cost | 87.50 |
| **Total** | **12** | **41** | | | **1,323.50** |

**Check:** `(6+24)×22 + (4+12)×36 + (2+5)×12.50 = 660 + 576 + 87.50 = 1,323.50`.

Estimated monthly spend for **280** licensed users (180×$22 + 60×$36 + 40×$12.50) = **USD 6,620**.

## What-if scenario (excerpt)

Same reclaim baseline: BP enabled **186** / consumed **180** / disabled-assigned **24** at **$22**; E3 enabled **64** / consumed **60** / disabled-assigned **12** at **$36**.

Example plan (app math):

1. **Remove unused** on Business Premium (all 6)
2. **Remove disabled-assigned** on E3 (all 12) — drops enabled and consumed together
3. **Move 10** licenses E3 → Business Premium

| License | Before | After | Unit | Price source | Δ / mo | Δ / yr |
| --- | ---: | ---: | ---: | --- | ---: | ---: |
| Microsoft 365 Business Premium | 186 | 190 | 22.00 | saved tenant price | +88.00 | +1,056.00 |
| Microsoft 365 E3 | 64 | 42 | 36.00 | list-price estimate | −792.00 | −9,504.00 |
| **Net** | | | | | **−704.00** | **−8,448.00** |

**Check:**

- Before: `186×22 + 64×36 = 4,092 + 2,304 = 6,396`
- After step 1: BP enabled 180. After step 2: E3 enabled 52 / consumed 48. After move 10: BP 190, E3 42.
- After: `190×22 + 42×36 = 4,180 + 1,512 = 5,692`
- Delta: `5,692 − 6,396 = −704` / mo (`−8,448` / yr)

Scenarios stay read-only: export HTML/CSV/PDF or deliver like other reports; Graph license assignments are unchanged.

## Related

- [License audit](license-audit.md)
- [Unused licenses](unused-licenses.md)
- [What-if](what-if.md)
