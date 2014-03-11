#!/bin/bash
echo "ips_log:"
tail ./ips_log
echo "ips_config:"
tail ./ips_config
echo "current_blocked:"
tail ./current_blocked
echo "current_attempts:"
tail ./current_attempts
