# Admin permissions and consent

YeetnGreet changes users, mailboxes, licenses, and devices in your Microsoft 365 tenant. Microsoft requires an administrator in **each tenant you manage** to approve (grant **admin consent** for) the permissions below before YeetnGreet can run jobs there.

Use this page as the checklist for your Global Administrator, or for your own change ticket.

!!! note "Not the same as YeetnGreet roles"
    This page is about Microsoft 365 permissions in each tenant. Who can edit templates and tenants inside YeetnGreet is set by YeetnGreet's own [Admin and Tech roles](roles.md).

!!! important "Admin consent is per tenant"
    Consent granted in one tenant does **not** carry over to another. If you manage more than one tenant, repeat it for every tenant you add to YeetnGreet. Granting admin consent for Microsoft Graph application permissions needs a **Global Administrator** or **Privileged Role Administrator** in that tenant.

## How YeetnGreet signs in

| Sign-in mode | What runs the job | What your admin approves |
| --- | --- | --- |
| **App-only** (needed for scheduled jobs) | **Your own app registration in this tenant**, signing in with a certificate key that stays on the technician's PC. No admin account is signed in. | The **application permissions** and **roles** below, on your app registration |
| **Interactive** | An admin signs in to the tenant in the browser | The **delegated permissions** below, plus admin roles on the admin's account |

Either way, tokens are requested for the **tenant you selected**. YeetnGreet refuses to run a job if Microsoft returns a token for a different tenant.

## App-only: your own app in each tenant

YeetnGreet LLC doesn't own an app or hold a key for your tenant, and there's no shared YeetnGreet app to consent to. For app-only, each tenant gets **its own single-tenant app registration**, created in that tenant, and the technician's PC holds **its own certificate key** for it. One key can only ever open one tenant.

1. In the tenant: Entra admin center → **App registrations** → **New registration**. Supported account types: **Accounts in this organizational directory only (Single tenant)**. No redirect URI and no client secret.
2. Add the **application permissions** below and grant admin consent. Add the **roles** below.
3. In YeetnGreet: **Tenants** → select the tenant → **App-only for scheduled jobs** → paste the app's Application (client) ID → **Create key on this PC**.
4. Upload the `.cer` file YeetnGreet saved to the app registration (**Certificates & secrets** → **Certificates** → **Upload certificate**), then click **Save** in YeetnGreet.

About the key:

- It's created on the technician's PC and **can't be exported**: in the PC's TPM chip when it has one, otherwise in Windows key storage with export turned off. Only the public certificate (`.cer`) leaves the PC.
- It's valid for **12 months** at most. YeetnGreet warns **30 days** before it expires.
- **Client secrets and PFX files aren't supported.** Each PC that runs scheduled jobs creates its own key.

!!! tip "Rotating the key"
    1. **Create new key** on the Tenants page and upload the new `.cer` to the same app registration (keep the old one for now).
    2. Click **Save** in YeetnGreet to switch to the new key, and check the next job signs in.
    3. Delete the old certificate from the app registration, then **Delete old key** in YeetnGreet.

    If a PC is lost, delete its certificate from the app registration straight away. That alone stops the key working.

## App-only: application permissions

Grant these on **your app registration in this tenant** (App registrations → your app → **API permissions** → **Grant admin consent**). All are **Application** permissions.

### Microsoft Graph

| Permission | Why YeetnGreet needs it |
| --- | --- |
| `User.ReadWrite.All` | Create onboard accounts and update user details: manager, usage location, address-list visibility, and moving direct reports to a new manager. |
| `User.EnableDisableAccount.All` | Block sign-in for leavers and enable new hires' accounts. |
| `User-PasswordProfile.ReadWrite.All` | Reset the leaver's password and set the new hire's first password. |
| `User.RevokeSessions.All` | Sign the leaver out of every active session. |
| `UserAuthenticationMethod.ReadWrite.All` | Remove the leaver's MFA methods: Authenticator, phone, FIDO2, Windows Hello, software OATH, and email. |
| `LicenseAssignment.ReadWrite.All` | Assign licenses at onboard, remove them at offboard, and read license SKUs for the license audit. |
| `GroupMember.ReadWrite.All` | Add new hires to groups and remove leavers from groups. |
| `RoleManagement.ReadWrite.Directory` | **Optional — leave it out unless you need it.** Remove Entra admin role assignments from leavers. Only needed if you use **Remove Entra directory roles**. Without it, the app greys out that action and the job reports the step as **Skipped**. |
| `Directory.Read.All` | Read-only: tenant details, verified domains, and group and role memberships. YeetnGreet never writes with this permission. |
| `MailboxSettings.ReadWrite` | Set the leaver's out-of-office auto-reply. |
| `Files.ReadWrite.All` | Share the leaver's OneDrive with their manager or the handoff person. |
| `DeviceManagementManagedDevices.Read.All` | Find the leaver's Intune-managed devices (read only). Only needed if you use **Retire Intune devices**. |
| `DeviceManagementManagedDevices.PrivilegedOperations.All` | **Optional.** Retire those Intune devices. Requires **admin consent**. Without consent, the app greys out **Retire**. Only needed if you use **Retire Intune devices**. |
| `Reports.Read.All` | Read Microsoft 365 mail activity for the **Unused licenses** and **License audit** reports. |

YeetnGreet does **not** request application `Mail.Send`. Report email delivery is interactive-only (see below).

!!! tip "Why role removal is optional"
    `RoleManagement.ReadWrite.Directory` can assign any Entra role, including Global Administrator. YeetnGreet only uses it to **remove** admin roles from leavers, so you can leave it out. If it isn't granted, **Remove Entra directory roles** is greyed out with a short explanation, and offboarding jobs (including scheduled and batch jobs) skip that step and report it as **Skipped**, not failed. Remove the leaver's admin roles in the Entra admin center instead.

### Office 365 Exchange Online

| Permission | Why YeetnGreet needs it |
| --- | --- |
| `Exchange.ManageAsApp` | Connect to Exchange Online without a user, so YeetnGreet can convert the leaver's mailbox to shared, grant Full Access to the handoff person, and hide the mailbox from the address list. |

### Roles for your app registration

Microsoft requires a role on the app as well as the permissions above for some actions. Give it the smallest ones:

| Role | Why |
| --- | --- |
| **User Administrator** (Entra role) | Microsoft requires at least this role for an app to reset passwords. Assign it in Entra admin center → **Roles & admins** → User Administrator → **Add assignments** → your app. |
| **A custom Exchange role group** with `Mail Recipients`, `Distribution Groups` and `Security Group Creation and Membership` (recommended), **or** the **Exchange Recipient Administrator** Entra role | Exchange Online only accepts `Exchange.ManageAsApp` when the app also holds an Exchange role. These cover the mailbox steps: convert to shared, Full Access, hide from the address list, and remove the leaver from distribution lists. A custom role group can also be limited to some mailboxes. |

Don't give the app **Exchange Administrator** or **Global Administrator**. Neither is needed.

!!! warning "Offboarding an admin"
    Microsoft blocks lower-privileged roles from disabling, resetting, or removing MFA for **other administrators**. If you offboard someone who holds an admin role, the app may need **Privileged Authentication Administrator**. Otherwise, do those steps in the Entra admin center.

## Keeping app-only safe

- **Limit where the app can sign in from.** Conditional Access for workload identities can block the app's sign-ins from anywhere except your technicians' office IP addresses. It needs Microsoft Entra Workload ID Premium, and it works for single-tenant apps like this one.
- **Watch its sign-ins.** Entra admin center → **Sign-in logs** → **Service principal sign-ins**, filtered by the app's client ID. Alert on sign-ins from IP addresses you don't know.
- **Alert on changes.** Watch the audit log for new certificates or secrets on the app, new API permissions or consent, and the app being added to a role. If you didn't plan the change, treat it as an incident.
- **Turn it off fast.** Entra admin center → **Enterprise applications** → your app → **Properties** → **Enabled for users to sign in?** → **No**. That stops new sign-ins at once. Then delete its certificate from the app registration.

## Interactive: delegated permissions

When an admin signs in, YeetnGreet requests these **delegated** Microsoft Graph permissions.

**Required:**

`User.ReadWrite.All`, `User.EnableDisableAccount.All`, `User-PasswordProfile.ReadWrite.All`, `User.Read` (your organization's verified domains), `User.RevokeSessions.All`, `LicenseAssignment.ReadWrite.All`, `UserAuthenticationMethod.ReadWrite.All`, `MailboxSettings.ReadWrite`, `GroupMember.ReadWrite.All`, `Files.ReadWrite.All`, `Reports.Read.All`

**Optional** (each turns on one feature; without it, sign-in still works and that feature is greyed out):

| Permission | Feature |
| --- | --- |
| `DeviceManagementManagedDevices.Read.All` and `DeviceManagementManagedDevices.PrivilegedOperations.All` | **Retire Intune devices** |
| `Mail.Send` | Report email delivery |
| `RoleManagement.ReadWrite.Directory` | **Remove Entra directory roles** from leavers |

If your tenant hasn't consented to the optional permissions, YeetnGreet signs in with the required ones only and shows one note listing what's missing.

Interactive sign-in uses Microsoft's **Microsoft Graph Command Line Tools** app. The first time, approve the consent prompt and tick **Consent on behalf of your organization**, or grant admin consent to that app in your tenant.

Consent alone doesn't let an admin run the job. The signed-in account needs an active admin role too:

| Role on the signed-in account | Why |
| --- | --- |
| **User Administrator** (or Global Administrator / Privileged Role Administrator) | Required to disable accounts and reset passwords. YeetnGreet checks for it when it can read your roles and stops before a Live job if it's missing. |
| **Exchange Administrator** | Needed for the Exchange Online sign-in that runs the mailbox steps. |

!!! note "Report email delivery"
    Sending a report by email uses **delegated** `Mail.Send` and works only in **interactive** sign-in. In **app-only** mode, email delivery is unavailable — use a [webhook](../reports/delivery.md) or save the report locally instead. Application `Mail.Send` is not used.

## What YeetnGreet does *not* need

- **Broad directory write or site-wide access:** YeetnGreet doesn't request `Directory.ReadWrite.All`, `Directory.AccessAsUser.All`, `Sites.FullControl.All`, or `DeviceManagementManagedDevices.ReadWrite.All`. Each step uses the narrowest permission Microsoft offers for it.
- **Access beyond your work account to use YeetnGreet itself:** signing in to YeetnGreet for team and license features only uses `User.Read` against your own work account. It never grants access to your tenant's data.
- **On-premises Active Directory:** YeetnGreet works with cloud-only Microsoft 365 (Entra ID). On-premises and hybrid Active Directory aren't supported yet.
- **Application `Mail.Send`:** not requested. Email reports are interactive-only (delegated `Mail.Send`).

## Checklist for each tenant

1. Grant admin consent for every Microsoft Graph and Exchange Online permission above
2. App-only: create a **single-tenant app registration** in the tenant, give it **User Administrator** and the Exchange role group (or **Exchange Recipient Administrator**), then create its key in YeetnGreet and upload the `.cer`
3. Interactive: confirm the signed-in admin account has **User Administrator** (or higher) and **Exchange Administrator**
4. If you use **Retire Intune devices**: confirm admin consent for `DeviceManagementManagedDevices.Read.All` and `DeviceManagementManagedDevices.PrivilegedOperations.All` (otherwise Retire stays greyed out)
5. If you use **Remove Entra directory roles**: confirm admin consent for `RoleManagement.ReadWrite.Directory` (otherwise that action stays greyed out and is skipped)
6. Run a **Preview** in [First run](first-run.md) before any Live job

!!! note "Updating from an earlier version"
    Grant consent for the new permissions first (`Directory.Read.All` and `DeviceManagementManagedDevices.Read.All` for app-only; `User.Read` and `DeviceManagementManagedDevices.Read.All` for interactive), then remove the old ones. Removing a permission from the app doesn't take back consent your tenant already gave, so remove `Directory.ReadWrite.All`, `Sites.FullControl.All`, `Directory.AccessAsUser.All`, and `DeviceManagementManagedDevices.ReadWrite.All` in Enterprise applications → **Permissions** (on your app-only app registration, and on Microsoft Graph Command Line Tools for interactive) once the new set works. If you set up app-only with an earlier version, move to one single-tenant app per tenant with a key created in YeetnGreet, remove the **Exchange Administrator** role from the app, and delete any old client secrets and certificates from it.

## Related

- [Install](install.md)
- [First run](first-run.md)
- [Roles: admin and tech](roles.md)
- [Multi-tenant](../tenants/multi-tenant.md)
- [Report delivery](../reports/delivery.md)
