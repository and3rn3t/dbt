# 🚀 Deployment Checklist - Ubuntu Server with Docker

Use this checklist to ensure a smooth deployment.

---

## Pre-Deployment

- [ ] Ubuntu server provisioned (20.04+ recommended)
- [ ] SSH access configured
- [ ] At least 4GB RAM available
- [ ] At least 20GB disk space free
- [ ] Backup plan in place
- [ ] Domain/IP address ready (if needed)

---

## Server Setup

- [ ] System updated: `sudo apt-get update && sudo apt-get upgrade -y`
- [ ] Docker installed and verified: `docker --version`
- [ ] Docker Compose installed: `docker compose version`
- [ ] User added to docker group: `sudo usermod -aG docker $USER`
- [ ] Docker service enabled: `sudo systemctl enable docker`
- [ ] Git installed: `git --version`

---

## Project Deployment

- [ ] Repository cloned: `git clone https://github.com/and3rn3t/dbt.git`
- [ ] `.env` file created from `.env.example`
- [ ] Strong passwords set in `.env` file
- [ ] `.env` file secured: `chmod 600 .env`
- [ ] Docker images built: `docker compose build`
- [ ] Services started: `docker compose up -d`
- [ ] All containers running: `docker compose ps`

---

## Testing & Validation

- [ ] PostgreSQL healthy: `docker compose exec postgres pg_isready`
- [ ] Database accessible: `docker compose exec postgres psql -U dbt_user -d dbt_analytics`
- [ ] Schemas created: Check staging, marts, seeds schemas exist
- [ ] dbt connection works: `docker compose exec dbt dbt debug`
- [ ] Sample dbt run successful: `docker compose exec dbt dbt run`
- [ ] Jupyter Lab accessible: http://your-server-ip:8888
- [ ] Adminer accessible: http://your-server-ip:8080

---

## Security Configuration

- [ ] Default passwords changed
- [ ] Firewall configured (UFW)
- [ ] SSH port secured (if not default 22)
- [ ] PostgreSQL NOT exposed to internet (port 5432 not public)
- [ ] Jupyter password set (if exposing to internet)
- [ ] Adminer disabled in production (or password protected)
- [ ] SSL/TLS configured (if using HTTPS)
- [ ] Nginx reverse proxy configured (optional)

---

## Automation Setup

- [ ] Backup script created: `backup-db.sh`
- [ ] Backup script executable: `chmod +x backup-db.sh`
- [ ] dbt run script created: `run-dbt.sh`
- [ ] Run script executable: `chmod +x run-dbt.sh`
- [ ] Cron jobs configured for:
  - [ ] Daily dbt runs
  - [ ] Daily backups
  - [ ] Log cleanup
- [ ] Log directories created: `/var/log/dbt/`
- [ ] Test cron jobs manually

---

## Monitoring & Logging

- [ ] Log rotation configured
- [ ] Disk space monitoring in place
- [ ] Container health checks verified
- [ ] Alert system configured (email/Slack)
- [ ] Backup verification process in place
- [ ] Resource monitoring enabled: `docker stats`

---

## Documentation

- [ ] Deployment notes documented
- [ ] Credentials stored securely (password manager)
- [ ] Team members have access instructions
- [ ] Backup/restore procedures documented
- [ ] Troubleshooting guide available
- [ ] Contact information for support

---

## Production Readiness

- [ ] Development environment tested thoroughly
- [ ] Production database configured (if separate)
- [ ] Production target tested: `dbt run --target prod`
- [ ] Resource limits set in docker-compose.yml
- [ ] Rollback plan prepared
- [ ] Maintenance window scheduled
- [ ] Stakeholders notified

---

## Post-Deployment

- [ ] System monitored for 24 hours
- [ ] First automated run successful
- [ ] Backups verified and restorable
- [ ] Performance metrics baseline established
- [ ] Documentation updated with production details
- [ ] Team training completed (if needed)

---

## Maintenance Schedule

**Daily:**
- [ ] Check container status
- [ ] Review error logs
- [ ] Verify backup completion

**Weekly:**
- [ ] Review disk space usage
- [ ] Check dbt run duration trends
- [ ] Review and clear old logs

**Monthly:**
- [ ] Test backup restoration
- [ ] Update Docker images: `docker compose pull`
- [ ] Review and update dependencies
- [ ] Security audit

---

## Emergency Contacts

- **Server Admin:** _______________________
- **Database Admin:** _______________________
- **Application Owner:** _______________________
- **On-Call:** _______________________

---

## Quick Reference

```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Run dbt
docker compose exec dbt dbt run

# Backup database
./backup-db.sh

# Check status
docker compose ps

# Restart services
docker compose restart

# Stop services
docker compose down
```

---

**Date Completed:** _______________________  
**Deployed By:** _______________________  
**Notes:** _______________________
