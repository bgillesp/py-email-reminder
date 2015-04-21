#! /usr/bin/python

import parsedatetime
import time
import base64
import shlex,subprocess
from subprocess import PIPE
from StringIO import StringIO

# t is of type time.struct_time
def _email_reminder(msg,t):
	ssh_target = "serverusername@site.com"
	schedule_script = "/home/serverusername/local/scheduler/schedule_reminder.py"
	email_recipient = 'emailaddress@gmail.com'
	
	# format subject line
	subject_fmt = '*** Reminder from %s ***'
	cur_time = time.strftime(r'%A, %B %d, %Y at %I:%M %p',time.localtime())
	subject_line = subject_fmt % cur_time
	
	# format send time
	send_time_fmt = r'%(hour)02d:%(min)02d %(mon)02d/%(day)02d/%(year)04d'
	time_params = {"mon":t.tm_mon, "day":t.tm_mday, "year":t.tm_year, "hour":t.tm_hour, "min":t.tm_min}
	send_time_str = send_time_fmt % time_params
	
	# format ssh command
	ssh_cmd_fmt = "ssh %(ssh_target)s %(script)s %(subj)s %(body)s %(recip)s %(send_time)s"
	format_data = {'subj':subject_line, 'body':msg, 'recip':email_recipient, 'send_time':send_time_str}
	# encode long-term parameters in base64
	for k in format_data.keys():
		format_data[k] = base64.b64encode(format_data[k])
	format_data['ssh_target'] = ssh_target
	format_data['script'] = schedule_script
	ssh_cmd_str = ssh_cmd_fmt % format_data
	
	try:
		ssh_cmd_args = shlex.split(ssh_cmd_str)
		output = StringIO()
		p = subprocess.Popen(ssh_cmd_args,stdout=PIPE,stderr=PIPE)
		p.wait()
		#output = p.stdout.readlines()
		#for l in output:
		#	print l
	except subprocess.CalledProcessError as e:
		print "Error with command.  Return code %d" % e.returncode
	else:
		code = p.returncode
		if code != 0:
			print "Error: Process returned with code %d.  Output:" % code
			print "-----"
			err = p.stderr.readlines()
			for l in err:
				print l
			print "-----"
			print "Message will (probably) not be sent."
			print "Contact your system administrator to troubleshoot this problem."
		else:
			print "Scheduling process returned with code %d" % code
			print "Message will be sent by email at %s" % send_time_str


def reminder(msg,t,method="email"):
	cal = parsedatetime.Calendar()
	parse = cal.parse(t)
	code = parse[1]
	try:
		if code == 0:
			raise Exception("Unable to generate reminder: Unable to parse time string: " + str(t))
		else:
			if type(parse[0]) == tuple:
				t = time.struct_time(parse[0])
			else:
				t = parse[0]
			now = cal.parse("now + 1 second")[0]
			if t < now:
				raise Exception("Unable to generate reminder: Specified time is in the past")
		if method == "email":
			_email_reminder(msg,t)
		else:
			raise Exception("Unable to generate reminder: Invalid reminder method: " + str(method))
	except Exception as e:
		print e.args[0]

if __name__ == "__main__":
    reminder("Try this out!","Tomorrow at noon")
