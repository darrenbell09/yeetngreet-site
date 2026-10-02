# Report delivery

Send report output to the channels your practice already uses.

## Supported channels

| Channel | Notes |
| --- | --- |
| **Email** | Sent via **Microsoft Graph** from the technician context / tenant you configure |
| **Microsoft Teams** | Incoming webhook or Teams workflow URL as configured in the app |
| **Slack** | Incoming webhook URL |
| **Webhooks** | Generic HTTPS endpoint for your RMM / automation |

## Setup tips

1. Create the destination (mailbox, Teams workflow, Slack app webhook, or HTTPS listener)
2. Paste the destination into YeetnGreet report delivery settings
3. Run a small test report before attaching it to a [schedule](../jobs/schedules.md)

!!! important "Credentials stay with you"
    Webhook URLs and Graph mail send from the technician environment. Treat webhook URLs like secrets in your password vault.

## Related

- [Reports overview](overview.md)
- [Schedules](../jobs/schedules.md)
- [Samples](samples.md)
