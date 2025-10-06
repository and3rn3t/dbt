#!/bin/bash
# dbt Run Script for Cron Jobs
# Usage: ./run-dbt.sh [command]
# Example: ./run-dbt.sh run
#          ./run-dbt.sh test
#          ./run-dbt.sh "run --select staging"

set -e

# Configuration
PROJECT_DIR="/home/ubuntu/dbt"
LOG_DIR="/var/log/dbt"
DATE=$(date +%Y%m%d_%H%M%S)

# Create log directory if it doesn't exist
mkdir -p $LOG_DIR

# Change to project directory
cd $PROJECT_DIR

# Default command
COMMAND=${1:-"run"}

# Log start
echo "[$DATE] Starting dbt $COMMAND" >> $LOG_DIR/dbt-runs.log

# Run dbt command
docker compose exec -T dbt dbt $COMMAND 2>&1 | tee -a $LOG_DIR/dbt-$COMMAND-$DATE.log

# Check exit status
if [ $? -eq 0 ]; then
    echo "[$DATE] dbt $COMMAND completed successfully" >> $LOG_DIR/dbt-runs.log
else
    echo "[$DATE] dbt $COMMAND FAILED" >> $LOG_DIR/dbt-runs.log
    exit 1
fi

# Clean up old logs (keep last 30 days)
find $LOG_DIR -name "dbt-*.log" -mtime +30 -delete

exit 0
