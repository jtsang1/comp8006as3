# File:		main.py
# Authors:	Kevin Eng, Jeremy Tsang
# Purpose:	COMP 8006 Assignment 3
# Notes:	An IPS monitoring /var/log/secure for failed ssh attempts
# Date:		March 10, 2014

import os
#import subprocess

output = os.popen("cat /var/log/secure | grep -a 'Failed' | awk -F' ' '{print $1,$2,$3,$11;}'").read()
print("what\n", output, sep='')

