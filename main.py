'''
File:		main.py
Authors:	Kevin Eng, Jeremy Tsang
Purpose:	COMP 8006 Assignment 3
Date:		March 10, 2014

Notes:		An IPS monitoring /var/log/secure for failed ssh attempts and block users who reach
		a configurable limit of failed attempts. The user is blocked by their IP address
		using Linux Iptables for a configurable amount of time. This program keeps track of
		a set of files to hold it's current data since it was designed to be run by Linux
		Crontab shown below:

		1 ./current_attempts	A list of all current failed attempts (old entries are removed)
		2 ./current_blocked	A list of IP's currently blocked by Iptables
		3 ./ips_log		A log of every block/unblock action by this IPS
		4 ./ips_config		Variables used to keep track of this IPS
'''

import os
import time
import calendar

# Globals
current_summary = []

# Add attempt to current_summary
def current_summary_add(ip_address):
	found = 0
	for line in current_summary:
		if line[0] == ip_address:
			line[1] += 1
			found = 1
			break
	
	if not found:
		current_summary.append([ip_address,1])

# Read config file for current line
	# If log file size has decreased, reset curline to 1
curline = 100

# Get list of failed connections in "Month Date HH:MM:SS IP" format
new_attempts = os.popen("sed -n '%d,$p' /var/log/secure-20140310 | grep -a 'Failed' | awk -F' ' '{print $1,$2,$3,$11;}'" % curline).read().split("\n")

# Append new_attempts to current_attempts

# Loop through current_attempts and remove expired entries (Expiry set by user)
# Build current_summary of current_attempts
current_year = time.strftime("%Y")
current_timestamp = time.time()
expiry_time = 60 * 60 * 24 * 4
current_attempts = []
for line in new_attempts:
	words = line.split(" ")
		
	# If invalid line (last line) then break
	if len(words) != 4:
		break
	
	# Convert string time to timestamp
	stringtime = words[0] + ' ' + words[1] + ' ' + words[2] + ' ' + current_year
	#print(stringtime)
	#timestamp = time.strptime(stringtime, "%b %d %H:%M:%S %Y")
	timestamp = calendar.timegm(time.strptime(stringtime, "%b %d %H:%M:%S %Y"))
	print(timestamp)

	# If entry is expired, continue
	if current_timestamp > timestamp + expiry_time:
		continue
	else:
		# Else add to current_attempts
		current_attempts.append([timestamp,words[3]])	
		# Account in current_summary
		current_summary_add(words[3])
		#print(words[3])
	#print(line)

for line in current_attempts:
	print(line)

# Compare current_summary with current_blocked
for line in current_summary:
	# If in current_summary but not in current_blocked
	if(line[1] >= 
		# Block this IP
		# Log this block
	# If in current_summary and in current_blocked
		# Do nothing
	# If not in current_summary but in current_blocked
		# Unblock this IP
		# Log this unblock
	
# Replace current_blocked with current_summary



