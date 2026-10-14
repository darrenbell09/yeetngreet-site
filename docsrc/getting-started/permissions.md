# Admin permissions and consent

YeetnGreet changes users, mailboxes, licenses, and devices in your Microsoft 365 tenant. Microsoft requires an administrator in **each tenant you manage** to approve (grant **admin consent** for) the permissions below before YeetnGreet can run jobs there.

Use this page as the checklist for your Global Administrator, or for your own change ticket.

!!! important "Admin consent is per tenant"
    Consent granted in one tenant does **not** carry over to another. If you manage more than one tenant, repeat it for every tenant you add to YeetnGreet. Granting admin consent for Microsoft Graph application permissions needs a **Global Administrator** or **Privileged Role Administrator** in that tenant.

## How YeetnGreet signs in

| Sign-in mode | What runs the job | What your admin approves |
| --- | --- | --- |
| **App-only** (recommended for unattended and scheduled jobs) | The YeetnGreet app, with a certificate, with no admin account signed in | The **application permissions** and **directory roles** below |
| **Interactive** | An admin signs in to the tenant in the browser | The **delegated permissions** below, plus admin roles on the admin's account |

Either way, tokens are requested for the **tenant you selected**. YeetnGreet refuses to run a job if Microsoft returns a token for a different tenant.

## App-only: application permissions

Grant these in your tenant for the YeetnGreet app (Enterprise applications → YeetnGreet → **Permissions** → **Grant admin consent**). All are **Application** permissions.

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
| `RoleManagement.ReadWrite.Directory` | Remove Entra admin role assignments from leavers. |
| `Directory.ReadWrite.All` | Read tenant details, memberships, and direct reports, and update directory links the narrower permissions above don't cover. |
| `MailboxSettings.ReadWrite` | Set the leaver's out-of-office auto-reply. |
| `Files.ReadWrite.All` | Share the leaver's OneDrive with their manager or the handoff person. |
| `DeviceManagementManagedDevices.ReadWrite.All` | Find the leaver's Intune-managed devices. |
| `DeviceManagementManagedDevices.PrivilegedOperations.All` | Retire those Intune devices. Requires **admin consent**. Without consent, the app greys out **Retire**. Only needed if you use **Retire Intune devices**. |
| `Reports.Read.All` | Read Microsoft 365 mail activity for the **Unused seats** and **License audit** reports. |

YeetnGreet does **not** request application `Mail.Send`. Report email delivery is interactive-only (see below).

### Office 365 Exchange Online

| Permission | Why YeetnGreet needs it |
| --- | --- |
| `Exchange.ManageAsApp` | Connect to Exchange Online without a user, so YeetnGreet can convert the leaver's mailbox to shared, grant Full Access to the handoff person, and hide the mailbox from the address list. |

### Directory roles for the YeetnGreet app

Microsoft requires an admin role on the app as well as the permissions above for some actions. In your tenant, assign these roles to the **YeetnGreet** enterprise application (Entra admin center → Roles & admins):

| Role | Why |
| --- | --- |
| **Exchange Administrator** | Exchange Online only accepts `Exchange.ManageAsApp` when the app also holds an Exchange admin role. Needed for the mailbox steps. |
| **User Administrator** | Microsoft requires at least this role for an app to reset passwords. |

!!! warning "Offboarding an admin"
    Microsoft blocks lower-privileged roles from disabling, resetting, or removing MFA for **other administrators**. If you offboard someone who holds an admin role, the app may need **Privileged Authentication Administrator**. Otherwise, do those steps in the Entra admin center.

## Interactive: delegated permissions

When an admin signs in, YeetnGreet requests these **delegated** Microsoft Graph permissions. They match the app-only Graph names above, plus `Directory.AccessAsUser.All` (act as the signed-in admin) and `Mail.Send` (report email):

`User.ReadWrite.All`, `User.EnableDisableAccount.All`, `User-PasswordProfile.ReadWrite.All`, `Directory.AccessAsUser.All`, `User.RevokeSessions.All`, `LicenseAssignment.ReadWrite.All`, `UserAuthenticationMethod.ReadWrite.All`, `MailboxSettings.ReadWrite`, `GroupMember.ReadWrite.All`, `RoleManagement.ReadWrite.Directory`, `Directory.ReadWrite.All`, `Files.ReadWrite.All`, `DeviceManagementManagedDevices.ReadWrite.All`, `DeviceManagementManagedDevices.PrivilegedOperations.All`, `Reports.Read.All`, `Mail.Send`

Interactive sign-in uses Microsoft's **Microsoft Graph Command Line Tools** app. The first time, approve the consent prompt and tick **Consent on behalf of your organization**, or grant admin consent to that app in your tenant.

Consent alone doesn't let an admin run the job. The signed-in account needs an active admin role too:

| Role on the signed-in account | Why |
| --- | --- |
| **User Administrator** (or Global Administrator / Privileged Role Administrator) | Required to disable accounts and reset passwords. YeetnGreet checks for it and stops before a Live job if it's missing. |
| **Exchange Administrator** | Needed for the Exchange Online sign-in that runs the mailbox steps. |

!!! note "Report email delivery"
    Sending a report by email uses **delegated** `Mail.Send` and works only in **interactive** sign-in. In **app-only** mode, email delivery is unavailable — use a [webhook](../reports/delivery.md) or save the report locally instead. Application `Mail.Send` is not used.

## What YeetnGreet does *not* need

- **Access beyond your work account to use YeetnGreet itself:** signing in to YeetnGreet for team and license features only uses `User.Read` against your own work account. It never grants access to your tenant's data.
- **On-premises Active Directory:** YeetnGreet works with cloud-only Microsoft 365 (Entra ID). On-premises and hybrid Active Directory aren't supported yet.
- **Application `Mail.Send`:** not requested. Email reports are interactive-only (delegated `Mail.Send`).

## Checklist for each tenant

1. Grant admin consent for every Microsoft Graph and Exchange Online permission above
2. App-only: assign **Exchange Administrator** and **User Administrator** to the YeetnGreet enterprise app
3. Interactive: confirm the signed-in admin account has **User Administrator** (or higher) and **Exchange Administrator**
4. If you use **Retire Intune devices**: confirm admin consent for `DeviceManagementManagedDevices.PrivilegedOperations.All` (otherwise Retire stays greyed out)
5. Run a **Preview** in [First run](first-run.md) before any Live job

## Related

- [Install](install.md)
- [First run](first-run.md)
- [Multi-tenant](../tenants/multi-tenant.md)
- [Report delivery](../reports/delivery.md)
