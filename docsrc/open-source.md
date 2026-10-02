# Open source

YeetnGreet is a commercial desktop product. It incorporates third-party open-source and redistributable components under their respective licenses.

## Acknowledgements (summary)

| Component | License (SPDX / name) | Role |
| --- | --- | --- |
| Microsoft.Web.WebView2 | BSD-3-Clause (BSD-style) | Embedded browser host UI |
| Azure.Identity, Azure.Core | MIT | Entra ID / Azure credentials |
| Microsoft.Identity.Client (MSAL.NET), Extensions.Msal | MIT | Token acquisition / cache |
| System.IdentityModel.Tokens.Jwt | MIT | JWT handling |
| .NET runtime & Windows Forms | Microsoft redistributable terms | Self-contained Windows host |
| Inter, IBM Plex Mono | OFL-1.1 | UI fonts (loaded when online) |

Microsoft Graph PowerShell, Exchange Online PowerShell, and RSAT Active Directory are **customer-installed** on the technician PC when needed. They are **not** bundled inside `YeetnGreet.exe`.

## Notices file with the app

Full attribution for these components ships with YeetnGreet as **`THIRD_PARTY_NOTICES.txt`** next to the published app (and in the product source tree). That file includes SPDX identifiers, copyright holders, and short license summaries suitable for commercial redistribution under the stated licenses.

Customer docs for install and privacy:

- [Install](getting-started/install.md)
- [Privacy](privacy.md)
