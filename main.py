#!/bin/python3


'''*****************************************************************************
File:		main.py
Authors:	Kevin Eng, Jeremy Tsang
Purpose:	COMP 8006 Assignment 3
Date:		March 10, 2014

Notes:		An IPS monitoring /var/log/secure for failed ssh attempts and
		block users who reach a configurable limit of failed attempts. 
		The user is blocked by their IP address	using Linux Iptables for
		a configurable amount of time. This program keeps track of a set 
		of internal files to hold it's current data since it was
		designed to be run by Linux Crontab:

		1 ./current_attempts	A list of all current failed attempts (old entries are removed)
		2 ./current_blocked	A list of IP's currently blocked by Iptables
		3 ./ips_log		A log of every block/unblock action by this IPS
		4 ./ips_config		Variables used to keep track of this IPS
		
TODO		-cleanup code and comment
		-use current_attempts
'''


'''*****************************************************************************
Configuration
*****************************************************************************'''
logfile = "/var/log/secure"	# Log file to monitor
max_attempts = 3		# Max attempts before blocking
expiry_time = 60 * 60 * 24 * 4  # Time before failed attempts expire

# Internal files used (must exist)
path_current_attempts = "./current_attempts"
path_current_blocked = "./current_blocked"
path_ips_log = "./ips_log"
path_ips_config = "./ips_config"


'''*****************************************************************************
Functions
*****************************************************************************'''
# Imports
import os
import time
import datetime
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

# Block IP and add log entry
def block_IP(ip_addr):
	os.system("iptables -A INPUT -s " + ip_addr + " -j DROP")
	curtime = datetime.datetime.now().strftime("%b %d %Y %T")
	file_ips_log = open(path_ips_log,"a")
	file_ips_log.write("%s Blocking ip %s\n" % (curtime,ip_addr))
	file_ips_log.close()

# Unblock IP and add log entry
def unblock_IP(ip_addr):
	os.system("iptables -D INPUT -s " + ip_addr + " -j DROP")
	curtime = datetime.datetime.now().strftime("%b %d %Y %T")
	file_ips_log = open(path_ips_log,"a")
	file_ips_log.write("%s Unblocking ip %s\n" % (curtime,ip_addr))
	file_ips_log.close()


'''*****************************************************************************
Main Program
*****************************************************************************'''
# Read config file for current line
file_ips_config = open(path_ips_config,"r")
ips_config = file_ips_config.read().split("\n")
curline = 1
cursize = 0

for line in ips_config:
	words = line.split("=")
	if words[0] == "current_line":
		curline = int(words[1])
	elif words[0] == "logfile_size":
		cursize = int(words[1])

# If log file size has decreased, reset curline to 1
logfile_stat = os.stat(logfile)
if logfile_stat.st_size < cursize:
	curline = 1

# Get list of failed connections in "Month Date HH:MM:SS IP" format
new_attempts = os.popen("sed -n '%d,$p' %s | grep -a 'Failed' | awk -F' ' '{print $1,$2,$3,$11;}'" % (curline, logfile)).read().split("\n")

# Update current line
curline = sum(1 for line in open(logfile))
cursize = logfile_stat.st_size

file_ips_config.close()
file_ips_config = open(path_ips_config,"w")
file_ips_config.write("current_line=%d\n" % curline)
file_ips_config.write("logfile_size=%d\n" % cursize)
file_ips_config.close()

# Append new_attempts to current_attempts
file_current_attempts = open(path_current_attempts,"r")

# Loop through current_attempts and remove expired entries (Expiry set by user)
# Build current_summary of current_attempts
current_year = time.strftime("%Y")
current_timestamp = time.time()
current_attempts = []
for line in new_attempts:
	words = line.split(" ")
		
	# If invalid line (last line) then break
	if len(words) != 4:
		break
	
	# Convert string time to timestamp
	stringtime = words[0] + ' ' + words[1] + ' ' + words[2] + ' ' + current_year
	#timestamp = time.strptime(stringtime, "%b %d %H:%M:%S %Y")
	timestamp = calendar.timegm(time.strptime(stringtime, "%b %d %H:%M:%S %Y"))

	# If entry is expired, continue
	if current_timestamp > timestamp + expiry_time:
		continue
	else:
		# Add to current_attempts
		current_attempts.append([timestamp,words[3]])	
		# Account in current_summary
		current_summary_add(words[3])

print("current attempts:")
for line in current_attempts:
	print(line)

# Open current_blocked
file_current_blocked = open(path_current_blocked, "r")
current_blocked = file_current_blocked.read().split("\n")
current_blocked.pop()

# Get list of ips from current_summary
current_summary_ip = []
for line in current_summary:
	if line[1] >= max_attempts:
		current_summary_ip.append(line[0])

# If in current_summary but not in current_blocked
ips_to_block = list(set(current_summary_ip) - set(current_blocked))

for ip in ips_to_block:
	block_IP(ip)

# If not in current_summary but in current_blocked
ips_to_unblock = list(set(current_blocked) - set(current_summary_ip))

for ip in ips_to_unblock:
	unblock_IP(ip)

# Overwrite current_blocked with current_summary_ip
file_current_blocked.close()
file_current_blocked = open(path_current_blocked, "w")

for ip in current_summary_ip:
	file_current_blocked.write(ip+"\n")

