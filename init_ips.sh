#!/bin/bash

# Clear Iptables
iptables -F
iptables -X

# Make paths and copy files to path
mkdir /root/Documents
mkdir /root/Documents/ips_ssh
chmod 777 /root/Documents/ips_ssh
cp ./main.py /root/Documents/ips_ssh/
cp ./file_init.sh /root/Documents/ips_ssh/
cp ./file_tail.sh /root/Documents/ips_ssh/
cp ./file_reset.sh /root/Documents/ips_ssh/
cp ./ips.sh /root/Documents/ips_ssh/
chmod 777 /root/Documents/ips_ssh/ips.sh

# Init files
. /root/Documents/ips_ssh/file_init.sh

# Add cron job
echo "* * * * * root /root/Documents/ips_ssh/ips.sh" >> /etc/crontab
