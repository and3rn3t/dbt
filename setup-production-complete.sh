#!/bin/bash
# Complete Production Setup Script
# Run this on the server to finish all configuration

set -e

echo "=========================================="
echo "🔧 Complete Production Setup"
echo "=========================================="
echo ""

# 1. Set Jupyter Password
echo "Step 1: Setting Jupyter Password"
echo "--------------------------------------"
echo "Please enter a password for Jupyter Lab:"
docker compose exec -T jupyter jupyter server password
echo "✅ Jupyter password set"
echo ""

# 2. Verify data files
echo "Step 2: Verifying Data Files"
echo "--------------------------------------"
ls -lh ~/dbt/data/processed/
echo "✅ Data files verified"
echo ""

# 3. Make backup script executable
echo "Step 3: Configuring Backup Script"
echo "--------------------------------------"
chmod +x ~/dbt/backup-db.sh
echo "✅ Backup script ready"
echo ""

# 4. Make dbt run script executable
echo "Step 4: Configuring dbt Run Script"
echo "--------------------------------------"
chmod +x ~/dbt/scripts/run-dbt.sh
echo "✅ dbt run script ready"
echo ""

# 5. Setup automated backups (cron)
echo "Step 5: Setting Up Automated Backups"
echo "--------------------------------------"
# Create a temporary crontab file
crontab -l > /tmp/mycron 2>/dev/null || true

# Check if backup job already exists
if ! grep -q "backup-db.sh" /tmp/mycron; then
    # Add daily backup at midnight
    echo "0 0 * * * /home/dbtuser/dbt/backup-db.sh" >> /tmp/mycron
    crontab /tmp/mycron
    echo "✅ Automated daily backups configured (midnight)"
else
    echo "✅ Backup cron job already exists"
fi

rm -f /tmp/mycron
echo ""

# 6. Setup automated dbt runs (cron)
echo "Step 6: Setting Up Automated dbt Runs"
echo "--------------------------------------"
# Create a temporary crontab file
crontab -l > /tmp/mycron 2>/dev/null || true

# Check if dbt run job already exists
if ! grep -q "run-dbt.sh" /tmp/mycron; then
    # Add daily dbt run at 2 AM
    echo "0 2 * * * /home/dbtuser/dbt/scripts/run-dbt.sh run" >> /tmp/mycron
    crontab /tmp/mycron
    echo "✅ Automated daily dbt runs configured (2 AM)"
else
    echo "✅ dbt run cron job already exists"
fi

rm -f /tmp/mycron
echo ""

# 7. Show current cron jobs
echo "Step 7: Current Automated Jobs"
echo "--------------------------------------"
echo "Your cron jobs:"
crontab -l
echo ""

# 8. Test Jupyter Lab access
echo "Step 8: Service Status"
echo "--------------------------------------"
docker compose ps
echo ""

# 9. Show connection info
echo "=========================================="
echo "✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "📊 Access Your Services:"
echo "--------------------------------------"
echo "Jupyter Lab: http://159.203.140.78:8888"
echo "Adminer:     http://159.203.140.78:8080"
echo ""
echo "🔒 Security:"
echo "--------------------------------------"
echo "✅ Jupyter password protected"
echo "✅ Firewall configured (UFW)"
echo "✅ Automated backups: Daily at 00:00"
echo "✅ Automated dbt runs: Daily at 02:00"
echo ""
echo "📁 Data Files:"
echo "--------------------------------------"
ls -1 ~/dbt/data/processed/
echo ""
echo "🎯 Next Steps:"
echo "--------------------------------------"
echo "1. Access Jupyter Lab and test environment"
echo "2. Create dbt staging models"
echo "3. Create dbt marts models"
echo "4. Run: docker compose exec dbt dbt seed"
echo "5. Run: docker compose exec dbt dbt run"
echo "6. Run: docker compose exec dbt dbt test"
echo ""
echo "📚 Useful Commands:"
echo "--------------------------------------"
echo "View logs:       docker compose logs -f"
echo "Restart:         docker compose restart"
echo "Stop all:        docker compose down"
echo "Start all:       docker compose up -d"
echo "Check services:  docker compose ps"
echo "dbt run:         docker compose exec dbt dbt run"
echo "dbt test:        docker compose exec dbt dbt test"
echo "Backup now:      ./backup-db.sh"
echo ""
