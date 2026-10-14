# Multi-tenant

Some IT teams manage more than one Microsoft 365 tenant — for example a parent company with subsidiaries, or separate tenants per business unit. YeetnGreet lets you switch between the tenants you manage without mixing up context, as long as you confirm the active tenant before Live work.

## Switching tenants

1. Open the tenant switcher in YeetnGreet
2. Select the tenant you are about to work in
3. Confirm domain / display name matches the request or ticket
4. Continue with onboard, offboard, or reports

![Screenshot: Tenants — switcher](../assets/images/multi-tenant.png){ width="720" }
*Placeholder — multi-tenant switcher.*

!!! danger "Wrong-tenant rule"
    Preview and type-to-confirm protect actions, but they do not fix picking the wrong tenant. Habit: read the tenant name before every confirm.

## Plan limits

| Plan | Managed tenants |
| --- | --- |
| Community | 1 |
| Team | 1 |
| Founding | Up to 5 |

See [Pricing and licensing](../pricing-and-licensing.md).

!!! note "Cloud-only Microsoft 365"
    Hybrid and on-premises Active Directory are not supported yet. Each tenant must be cloud-only Microsoft 365 (Entra ID).

## Related

- [Admin permissions and consent](../getting-started/permissions.md)
- [First run](../getting-started/first-run.md)
