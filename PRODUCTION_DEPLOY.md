# 🚀 Production Deployment Instructions

## Prerequisites

Before deploying, ensure you have:

- [ ] Ubuntu 20.04+ server (physical or cloud VM)
- [ ] SSH access with sudo privileges
- [ ] At least 4GB RAM
- [ ] At least 20GB free disk space
- [ ] Server IP address or domain name
- [ ] Strong passwords ready for database

---

## Quick Deploy (Automated)

### Option 1: Use the Deploy Script (Easiest)

On your Ubuntu server:

```bash
# Clone repository
git clone https://github.com/and3rn3t/dbt.git
cd dbt

# Make script executable
chmod +x deploy-production.sh

# Run deployment script
./deploy-production.sh
```

The script will:
- ✅ Update system
- ✅ Install Docker
- ✅ Configure firewall
- ✅ Set up environment
- ✅ Build images
- ✅ Start services
- ✅ Verify installation

---

## Manual Deploy (Step-by-Step)

If you prefer manual control:

### 1. Update System

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### 2. Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Clone Repository

```bash
git clone https://github.com/and3rn3t/dbt.git
cd dbt
```

### 4. Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit with your settings
nano .env

# ⚠️ IMPORTANT: Change these in .env:
# - DB_PASSWORD: Use a strong password
# - DB_USER_PROD: Production database user
# - DB_PASSWORD_PROD: Production database password
# - All other sensitive values

# Secure the file
chmod 600 .env
```

### 5. Configure Firewall

```bash
sudo apt-get install -y ufw
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 8888/tcp  # Jupyter
sudo ufw allow 8080/tcp  # Adminer (optional for production)
sudo ufw status
```

### 6. Build and Deploy

```bash
# Build images
docker compose build

# Start services
docker compose up -d

# Check status
docker compose ps

# Test connection
docker compose exec dbt dbt debug
```

### 7. Verify Deployment

```bash
# Check all containers are running
docker compose ps

# View logs
docker compose logs

# Test dbt
docker compose exec dbt dbt run
```

---

## Post-Deployment Configuration

### Set Up Automated Backups

```bash
# Make backup script executable
chmod +x backup-db.sh

# Test backup
./backup-db.sh

# Add to crontab for daily backups at midnight
crontab -e

# Add this line:
0 0 * * * /home/ubuntu/dbt/backup-db.sh
```

### Set Up Automated dbt Runs

```bash
# Make run script executable
chmod +x run-dbt.sh

# Add to crontab for daily runs at 2 AM
crontab -e

# Add this line:
0 2 * * * /home/ubuntu/dbt/run-dbt.sh run
```

### Create Log Directory

```bash
sudo mkdir -p /var/log/dbt
sudo chown $USER:$USER /var/log/dbt
```

---

## Access Your Services

Get your server IP:
```bash
hostname -I | awk '{print $1}'
```

Then access:
- **Jupyter Lab:** `http://YOUR_SERVER_IP:8888`
- **Adminer:** `http://YOUR_SERVER_IP:8080`

### Adminer Login:
- Server: `postgres`
- Username: `dbt_user` (or your configured user)
- Password: (from your .env file)
- Database: `dbt_analytics`

---

## Security Hardening (Production)

### 1. Disable Adminer in Production

Edit `docker-compose.yml` and comment out the adminer service:

```yaml
#  adminer:
#    image: adminer:latest
#    ...
```

Then restart:
```bash
docker compose down
docker compose up -d
```

### 2. Set Jupyter Password

```bash
# Generate password hash
docker compose exec jupyter python -c "from jupyter_server.auth import passwd; print(passwd())"

# Edit docker-compose.yml and add to jupyter command:
# --NotebookApp.password='your_hash_here'

# Restart jupyter
docker compose restart jupyter
```

### 3. Set Up Nginx Reverse Proxy (HTTPS)

```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/jupyter

# Add configuration (see docs/DOCKER_DEPLOYMENT.md for full config)

# Enable site
sudo ln -s /etc/nginx/sites-available/jupyter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### 4. Restrict PostgreSQL

Ensure PostgreSQL is not exposed publicly. In `docker-compose.yml`, comment out:

```yaml
postgres:
  # ports:
  #   - "5432:5432"  # Remove this in production
```

---

## Monitoring & Maintenance

### Check Service Health

```bash
# Container status
docker compose ps

# Resource usage
docker stats

# Disk usage
df -h
docker system df
```

### View Logs

```bash
# All logs
docker compose logs -f

# Specific service
docker compose logs -f dbt
docker compose logs -f postgres

# Recent errors
docker compose logs --tail=100 | grep -i error
```

### Update Deployment

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker compose down
docker compose build
docker compose up -d

# Verify
docker compose ps
docker compose exec dbt dbt debug
```

---

## Troubleshooting

### Services won't start

```bash
# Check logs
docker compose logs

# Restart individual service
docker compose restart dbt

# Full restart
docker compose down
docker compose up -d
```

### Database connection issues

```bash
# Check PostgreSQL is running
docker compose exec postgres pg_isready

# Check environment variables
docker compose exec dbt env | grep DB_

# Test connection manually
docker compose exec postgres psql -U dbt_user -d dbt_analytics
```

### Out of disk space

```bash
# Check space
df -h

# Clean Docker resources
docker system prune -a
docker volume prune

# Remove old logs
find /var/log/dbt -name "*.log" -mtime +30 -delete
```

### Memory issues

```bash
# Check current usage
free -h
docker stats

# Add swap if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Rollback Procedure

If something goes wrong:

```bash
# Stop services
docker compose down

# Restore from backup
gunzip -c backups/dbt_backup_YYYYMMDD_HHMMSS.sql.gz | \
  docker compose exec -T postgres psql -U dbt_user -d dbt_analytics

# Restart services
docker compose up -d
```

---

## Performance Tuning

### Increase Docker Resources

Edit `docker-compose.yml` and add under services:

```yaml
services:
  dbt:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Optimize PostgreSQL

```bash
# Connect to database
docker compose exec postgres psql -U dbt_user -d dbt_analytics

# Run these optimizations:
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '128MB';
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET default_statistics_target = 100;

# Restart PostgreSQL
docker compose restart postgres
```

---

## Production Checklist

Before going live:

- [ ] All passwords changed from defaults
- [ ] `.env` file secured (chmod 600)
- [ ] Firewall configured and enabled
- [ ] PostgreSQL not exposed publicly
- [ ] Adminer disabled or password protected
- [ ] Jupyter password set
- [ ] SSL/TLS configured (if public)
- [ ] Automated backups scheduled
- [ ] Automated dbt runs scheduled
- [ ] Monitoring set up
- [ ] Team has access instructions
- [ ] Disaster recovery plan documented

---

## Support

- **Full Guide:** `docs/DOCKER_DEPLOYMENT.md`
- **Checklist:** `DEPLOYMENT_CHECKLIST.md`
- **Quick Reference:** `QUICK_REFERENCE.md`
- **Current Status:** `DEPLOYMENT_SUCCESS.md`

---

## Quick Commands Reference

```bash
# Start
docker compose up -d

# Stop
docker compose down

# Status
docker compose ps

# Logs
docker compose logs -f

# dbt run
docker compose exec dbt dbt run

# Backup
./backup-db.sh

# Update
git pull && docker compose build && docker compose up -d
```

---

**Ready to deploy?** Run `./deploy-production.sh` on your Ubuntu server! 🚀
