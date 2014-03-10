# File:		main.py
# Authors:	Kevin Eng, Jeremy Tsang
# Purpose:	COMP 8006 Assignment 3
# Notes:	An IPS monitoring /var/log/secure for failed ssh attempts
# Date:		March 10, 2014

import os

os.system("cat /var/log/secure | grep 'Failed' | awk -F' ' '{print $11}'")
