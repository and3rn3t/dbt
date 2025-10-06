#!/bin/bash
# PostgreSQL Backup Script for dbt Analytics
# Backs up the database and keeps last 7 days of backups

set -e

# Configuration
PROJECT_DIR="/home/ubuntu/dbt"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="dbt_analytics"
DB_USER="dbt_user"
RETENTION_DAYS=7

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Change to project directory
cd $PROJECT_DIR

# Log start
echo "[$DATE] Starting database backup..."

# Create backup
docker compose exec -T postgres pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/dbt_backup_$DATE.sql.gz

# Check if backup was successful
if [ $? -eq 0 ]; then
    BACKUP_SIZE=$(du -h $BACKUP_DIR/dbt_backup_$DATE.sql.gz | cut -f1)
    echo "[$DATE] Backup completed successfully: dbt_backup_$DATE.sql.gz ($BACKUP_SIZE)"
else
    echo "[$DATE] Backup FAILED"
    exit 1
fi

# Remove old backups
echo "[$DATE] Cleaning up old backups (keeping last $RETENTION_DAYS days)..."
find $BACKUP_DIR -name "dbt_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# List current backups
echo "[$DATE] Current backups:"
ls -lh $BACKUP_DIR/dbt_backup_*.sql.gz 2>/dev/null || echo "No backups found"

echo "[$DATE] Backup process completed"
exit 0
