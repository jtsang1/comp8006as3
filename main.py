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

def blockIP(ip_addr):
	os.system("iptables -A INPUT -s " + ip_addr + " -j DROP")
	
def unblockIP(ip_addr):
	os.system("iptables -D INPUT -s " + ip_addr + " -j DROP")

# Read config file for current line
	# If log file size has decreased, reset curline to 1
curline = 100

# Get list of failed connections in "Month Date HH:MM:SS IP" format
new_attempts = os.popen("sed -n '%d,$p' /var/log/secure-20140310 | grep -a 'Failed' | awk -F' ' '{print $1,$2,$3,$11;}'" % curline).read().split("\n")

# Append new_attempts to current_attempts

# Loop through current_attempts and remove expired entries (Expiry set by user)
for line in new_attempts:
	words = line.split(" ")
	
	# If invalid line (last line) then break
	if len(words) != 4:
		break

	print(words[3])
	#print(line)



# Build current_summary of current_attempts


# Compare current_summary with current_blocked
	# If in current_summary but not in current_blocked
		# Block this IP
		# Log this block
	# If in current_summary and in current_blocked
		# Do nothing
	# If not in current_summary but in current_blocked
		# Unblock this IP
		# Log this unblock
	
# Replace current_blocked with current_summary




