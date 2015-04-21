#! /usr/bin/python

import sys
import base64
import smtplib

args = sys.argv[1:]

if len(args) != 3:
	print "Incorrect number of arguments (expected 3)"
	print "  Correct usage: " + sys.argv[0] + " subj body recip"
	print "  where subj, body, and recip are encoded in base64"
	exit()

args = map(base64.b64decode,sys.argv[1:4])
(subj, body, recip) = (args[0],args[1],args[2])

# Import smtplib for the actual sending function
me = '"Your Past Self" <past.self@site.com>'

# Import the email modules we'll need
from email.mime.text import MIMEText

# Create a text/plain message
msg = MIMEText(body,'plain')

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = subj
msg['From'] = me
msg['To'] = recip

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP('localhost')
s.sendmail(me, [recip], msg.as_string())
s.quit()

print "Successfully sent mail"
