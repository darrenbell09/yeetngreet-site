# Admin permissions and consent

YeetnGreet changes users, mailboxes, licenses, and devices in your **customer** Microsoft 365 tenants. Microsoft requires an administrator in **each customer tenant** to approve (grant **admin consent** for) the permissions below before YeetnGreet can run jobs there.

Use this page as the checklist for your customer's Global Administrator, or for your own change ticket.

!!! important "Admin consent is per customer tenant"
    Consent granted in your MSP tenant, or in one customer, does **not** carry over to another customer. Repeat it for every tenant you add to YeetnGreet. Granting admin consent for Microsoft Graph application permissions needs a **Global Administrator** or **Privileged Role Administrator** in that tenant.

## How YeetnGreet signs in

| Sign-in mode | What runs the job | What the customer admin approves |
| --- | --- | --- |
| **App-only** (recommended for MSPs) | The YeetnGreet multi-tenant app, with a certificate, with no technician account in the customer tenant | The **application permissions** and **directory roles** below |
| **Interactive** | A technician signs in to the customer tenant in the browser | The **delegated permissions** below, plus admin roles on the technician's account |

Either way, tokens are requested for the **customer tenant you selected**. YeetnGreet refuses to run a job if Microsoft returns a token for a different tenant.

## App-only: application permissions

Grant these in the customer tenant for the YeetnGreet app (Enterprise applications → YeetnGreet → **Permissions** → **Grant admin consent**). All are **Application** permissions.

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
| `DeviceManagementManagedDevices.PrivilegedOperations.All` | Retire those Intune devices. Only needed if you use **Retire Intune devices**. |
| `Reports.Read.All` | Read Microsoft 365 mail activity for the **Unused seats** and **License audit** reports. |

### Office 365 Exchange Online

| Permission | Why YeetnGreet needs it |
| --- | --- |
| `Exchange.ManageAsApp` | Connect to Exchange Online without a user, so YeetnGreet can convert the leaver's mailbox to shared, grant Full Access to the handoff person, and hide the mailbox from the address list. |

### Directory roles for the YeetnGreet app

Microsoft requires an admin role on the app as well as the permissions above for some actions. In the customer tenant, assign these roles to the **YeetnGreet** enterprise application (Entra admin center → Roles & admins):

| Role | Why |
| --- | --- |
| **Exchange Administrator** | Exchange Online only accepts `Exchange.ManageAsApp` when the app also holds an Exchange admin role. Needed for the mailbox steps. |
| **User Administrator** | Microsoft requires at least this role for an app to reset passwords. |

!!! warning "Offboarding an admin"
    Microsoft blocks lower-privileged roles from disabling, resetting, or removing MFA for **other administrators**. If you offboard someone who holds an admin role, the app may need **Privileged Authentication Administrator**. Otherwise, do those steps in the Entra admin center.

## Interactive: delegated permissions

When a technician signs in, YeetnGreet requests these **delegated** Microsoft Graph permissions. They are the same names as the app-only list, plus `Directory.AccessAsUser.All`, which lets the app act as the signed-in admin:

`User.ReadWrite.All`, `User.EnableDisableAccount.All`, `User-PasswordProfile.ReadWrite.All`, `Directory.AccessAsUser.All`, `User.RevokeSessions.All`, `LicenseAssignment.ReadWrite.All`, `UserAuthenticationMethod.ReadWrite.All`, `MailboxSettings.ReadWrite`, `GroupMember.ReadWrite.All`, `RoleManagement.ReadWrite.Directory`, `Directory.ReadWrite.All`, `Files.ReadWrite.All`, `DeviceManagementManagedDevices.ReadWrite.All`, `Reports.Read.All`

Interactive sign-in uses Microsoft's **Microsoft Graph Command Line Tools** app. The first time, approve the consent prompt and tick **Consent on behalf of your organization**, or grant admin consent to that app in the customer tenant.

Consent alone doesn't let a technician run the job. The technician's account needs an active admin role too:

| Role on the technician account | Why |
| --- | --- |
| **User Administrator** (or Global Administrator / Privileged Role Administrator) | Required to disable accounts and reset passwords. YeetnGreet checks for it and stops before a Live job if it's missing. |
| **Exchange Administrator** | Needed for the Exchange Online sign-in that runs the mailbox steps. |

## What YeetnGreet does *not* need

- **Your MSP tenant:** MSP sign-in to YeetnGreet itself (team and license features) only uses `User.Read` against your own work account. It never grants access to customer data.
- **Hybrid AD:** on-premises Active Directory steps run against your domain from the technician PC, not through Microsoft Graph. See [Hybrid AD](../tenants/hybrid-ad.md).

## Checklist per customer tenant

1. Grant admin consent for every Microsoft Graph and Exchange Online permission above
2. App-only: assign **Exchange Administrator** and **User Administrator** to the YeetnGreet enterprise app
3. Interactive: confirm the technician account has **User Administrator** (or higher) and **Exchange Administrator**
4. Run a **Preview** in [First run](first-run.md) before any Live job

## Related

- [Install](install.md)
- [First run](first-run.md)
- [Multi-tenant](../tenants/multi-tenant.md)
