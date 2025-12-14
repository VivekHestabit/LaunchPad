#!/bin/bash

SERVER="google.com"
LOG_FILE="logs/health.log"

while true
do
  ping -c 1 $SERVER > /dev/null

  if [ $? -ne 0 ]; then
    echo "$(date) - Server is DOWN" >> $LOG_FILE
  fi

  sleep 10
done
