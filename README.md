# py-email-reminder

Set up a very simple python function call to send yourself an email reminder at some future time from a remote server

## Introduction

This set of scripts has a very simple purpose: Provide an optimally simple Python command to set up an email reminder to be sent at a future time from a remote server.  The python command provided has interface:

```
reminder("Message of email body text","Natural language date string")
```

Easy peasy!  The command then will print a descriptive message indicating the outcome of the call.


## Installation Instructions

1. Local dependencies: Python with the "parsedatetime" package (see https://pypi.python.org/pypi/parsedatetime/), ssh

2. Server dependencies: Python, the "at" Unix scheduler utility, ssh access

3. Either set up reminder.py to run as part of a special python session for use via console, or set up a GUI to input data to it on the Desktop (not implemented)

4. Place schedule_reminder.py and send_mail.py on a server with the "at" command, and ssh access

5. Replace location parameters in reminder.py, schedule_reminder.py and send_mail.py to accurately reflect the system configuration of the server, and desired preferences for the emails to be sent

6. Set up public key encryption for ssh on the server

7. (Optional, but recommended) Set up SPF verification for your server IP address (a setting in the DNS records) to send mail from your domain.  Gmail, for instance, will auto-spam emails if this is not set up properly--a filter detecting all email from your domain will bypass this behavior, but it's better to get it set up properly once and for all. :)

8. Enjoy!
