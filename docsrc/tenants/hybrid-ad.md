# Hybrid AD

Optional **hybrid Active Directory** support can be enabled **per tenant** when an organization needs on-prem identity alongside Entra ID.

## What it is for

- Tenants still running hybrid join / synced identities
- Offboard and onboard paths that must respect on-prem + cloud steps your team defines

## How to think about it

| Topic | Guidance |
| --- | --- |
| Scope | Optional **per managed tenant** — enable only where needed |
| Where it runs | Still on the technician PC model; not “upload AD to YeetnGreet cloud” |
| Availability | Hybrid support is planned; pricing follows the same licensed-user bands on the [pricing page](https://yeetngreet.app/pricing.html) |

!!! note "Cloud-only tenants"
    If a tenant is cloud-only Entra, you can ignore hybrid settings entirely.

## Related

- [Multi-tenant](multi-tenant.md)
- [Pricing and licensing](../pricing-and-licensing.md)
