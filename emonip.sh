#!/bin/bash
# Requires nmap to be installed
NEWIP=`nmap -P 192.168.1.0/24|grep emonpi|grep -oE "([0-9]{1,3}\.){3}[0-9]{1,3}"`
sleep 1

if [[ -z "$NEWIP" ]];
  then
    echo "New IP is: $NEWIP"
    echo "192.168.1.100">/home/pi/emonpi
  else
    echo "$NEWIP">/home/pi/emonpi
    echo "$NEWIP is the new IP"
fi
