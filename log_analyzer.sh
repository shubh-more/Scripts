#!/bin/bash
LOG_FILE="/var/log/app.log"
BACKUP_DIR="/var/log/backup"
REPORT_FILE="/var/log/report.txt"
TODAY=$(date +"%Y-%m-%d")
if [ ! -f "$LOG_FILE" ]; then
    echo "[$TODAY] Log file not found!" >> "$REPORT_FILE"
    exit 1
fi

echo "Strating the applicatio">>/var/log/app.log
