# Sample report output

Anonymized examples of what paid-plan reports can look like. Your tenant names, SKUs, and counts will differ.

## License audit (excerpt)

| SKU | Assigned | Available | Notes |
| --- | ---: | ---: | --- |
| Microsoft 365 E3 | 142 | 8 | Core productivity |
| Exchange Online Plan 2 | 12 | 0 | Shared / legacy |
| Power BI Pro | 18 | 5 | Finance + ops |
| Microsoft Defender for Office 365 P2 | 142 | 0 | Bundled with E3 wave |

**Named users (sample rows)**

| Display name | UPN | SKUs |
| --- | --- | --- |
| Alex Rivera | alex.rivera@contoso-example.com | M365 E3 |
| Jordan Lee | jordan.lee@contoso-example.com | M365 E3; Power BI Pro |
| Sam Okonkwo | sam.okonkwo@contoso-example.com | Exchange Online Plan 2 |

## Unused seats (excerpt)

| UPN | SKU | Last signal | Est. monthly |
| --- | --- | --- | ---: |
| temp.contractor@contoso-example.com | M365 E3 | No sign-in 90d | $36 |
| archive.bot@contoso-example.com | Power BI Pro | No activity 60d | $10 |
| leavers.hold@contoso-example.com | M365 E3 | Disabled + licensed | $36 |

!!! note "Illustrative only"
    Figures are fictional for documentation. Always validate in the customer tenant before reclaiming.

## What-if (excerpt)

```text
Scenario: Q4 reclaim wave
- Remove 6× Microsoft 365 E3 (unused)
- Move 10× E3 → Business Premium (dept B)
Projected assigned E3: 142 → 126
Projected monthly delta: about -$580 (list; customer price may differ)
```

## Related

- [License audit](license-audit.md)
- [Unused seats](unused-seats.md)
- [What-if](what-if.md)
