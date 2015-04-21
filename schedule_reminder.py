#! /usr/bin/python

import sys
import shlex,subprocess
from subprocess import PIPE
import base64

send_mail_script = '/home/username/local/scheduler/send_mail.py'

# retrieve shell parameters -- must have 4 of them
args = sys.argv[1:]
if len(args) != 4:
	print "Incorrect number of arguments: " + str(len(args)) + " (expected 4)"
	print "Correct usage: " + sys.argv[0] + " subj body recip time"
	print "  where all parameters are encoded in base64"
	exit()
t_str = base64.b64decode(args[3])
data = {'script_loc':send_mail_script, 'subj':args[0], 'body':args[1], 'recip':args[2], 'time':t_str}

# format email command
email_cmd_fmt = "%(script_loc)s %(subj)s %(body)s %(recip)s"
cmd1 = email_cmd_fmt % data

# format scheduler command
sched_cmd_fmt = "at -M %(time)s"
cmd2 = sched_cmd_fmt % data

# execute scheduler command
cmd2_args = shlex.split(cmd2)
p = subprocess.Popen(cmd2_args,stdin=PIPE,stdout=PIPE,stderr=PIPE)

# pipe in email command for later execution
(out,err) = p.communicate(cmd1)

print "Message will be sent by email at %s" % t_str
