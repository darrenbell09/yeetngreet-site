# Hybrid AD

Optional **hybrid Active Directory** support can be enabled **per tenant** when a customer needs on-prem identity alongside Entra ID.

## What it is for

- Customers still running hybrid join / synced identities
- Offboard and onboard paths that must respect on-prem + cloud steps your practice defines

## How to think about it

| Topic | Guidance |
| --- | --- |
| Scope | Optional **per managed tenant** — not an all-or-nothing MSP toggle |
| Where it runs | Still on the technician PC model; not “upload AD to YeetnGreet cloud” |
| Availability | Called out on Founding (hybrid AD free for that cohort when it ships). Broader MSP Hybrid packaging is planned separately on the [homepage](https://yeetngreet.app/) |

!!! note "Customer tone"
    If a tenant is cloud-only Entra, you can ignore hybrid settings entirely.

## Related

- [Multi-tenant](multi-tenant.md)
- [Pricing and licensing](../pricing-and-licensing.md)
