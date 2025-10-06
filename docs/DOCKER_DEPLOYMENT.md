# 🐳 Docker Deployment Guide - Ubuntu Server

Complete guide to deploying your dbt Analytics project on Ubuntu using Docker.

---

## 📋 Prerequisites

- Ubuntu 20.04+ server
- Root or sudo access
- At least 4GB RAM
- 20GB free disk space

---

## 🚀 Quick Start Installation

### 1. Prepare Ubuntu Server

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git
```

### 2. Install Docker

```bash
# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up stable repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Verify installation
sudo docker --version
sudo docker compose version
```

### 3. Configure Docker (Optional but Recommended)

```bash
# Add your user to docker group (avoid using sudo)
sudo usermod -aG docker $USER

# Apply group changes (log out and back in, or run)
newgrp docker

# Enable Docker to start on boot
sudo systemctl enable docker
sudo systemctl start docker

# Verify docker works without sudo
docker ps
```

---

## 📦 Deploy Your Project

### 1. Clone Repository

```bash
# Clone your repository
git clone https://github.com/and3rn3t/dbt.git
cd dbt

# Or if already cloned, pull latest
git pull origin main
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
nano .env
```

**Edit the `.env` file:**
```bash
DB_USER=dbt_user
DB_PASSWORD=YourSecurePasswordHere123!
DB_NAME=dbt_analytics
DB_PORT=5432
JUPYTER_PORT=8888
ADMINER_PORT=8080
```

**Secure the file:**
```bash
chmod 600 .env
```

### 3. Build and Start Services

```bash
# Build the Docker image
docker compose build

# Start all services in background
docker compose up -d

# View logs
docker compose logs -f

# Check status
docker compose ps
```

**Expected output:**
```
NAME              IMAGE            STATUS         PORTS
dbt_postgres      postgres:15      Up (healthy)   0.0.0.0:5432->5432/tcp
dbt_analytics     dbt:latest       Up             
dbt_jupyter       dbt:latest       Up             0.0.0.0:8888->8888/tcp
dbt_adminer       adminer:latest   Up             0.0.0.0:8080->8080/tcp
```

---

## 🧪 Test the Installation

### 1. Test Database Connection

```bash
# Check if PostgreSQL is running
docker compose exec postgres pg_isready -U dbt_user

# Connect to database
docker compose exec postgres psql -U dbt_user -d dbt_analytics

# Inside psql:
\l              # List databases
\dn             # List schemas
\q              # Quit
```

### 2. Test dbt

```bash
# Test dbt connection
docker compose exec dbt dbt debug

# Run dbt models
docker compose exec dbt dbt run

# Run tests
docker compose exec dbt dbt test

# Generate documentation
docker compose exec dbt dbt docs generate
```

### 3. Access Services

**Jupyter Lab:**
- URL: `http://your-server-ip:8888`
- No password required (for development)

**Adminer (Database UI):**
- URL: `http://your-server-ip:8080`
- System: `PostgreSQL`
- Server: `postgres`
- Username: `dbt_user`
- Password: (from your .env)
- Database: `dbt_analytics`

---

## 📊 Working with Data

### Load Data into Database

```bash
# Copy CSV files to container
docker compose cp data/raw/sample_sales_data.csv dbt:/app/data/raw/

# Load seed data
docker compose exec dbt dbt seed

# Or load specific file
docker compose exec dbt dbt seed --select sample_sales_data
```

### Run Analysis Scripts

```bash
# Run Python scripts
docker compose exec dbt python /app/scripts/example_analysis.py

# Run with data
docker compose exec dbt python /app/scripts/fetch_data_gov.py
```

---

## 🔄 Daily Operations

### Start/Stop Services

```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart a specific service
docker compose restart dbt

# View logs
docker compose logs -f dbt
docker compose logs -f postgres
```

### Run Scheduled dbt Jobs

```bash
# Run dbt models
docker compose exec dbt dbt run

# Run specific model
docker compose exec dbt dbt run --select staging

# Run with full refresh
docker compose exec dbt dbt run --full-refresh
```

### Monitor Resources

```bash
# View resource usage
docker stats

# View container details
docker compose ps
docker compose top
```

---

## ⏰ Automate with Cron

### Set up Daily dbt Runs

```bash
# Edit crontab
crontab -e

# Add these lines:
# Run dbt daily at 2 AM
0 2 * * * cd /home/ubuntu/dbt && docker compose exec -T dbt dbt run >> /var/log/dbt-cron.log 2>&1

# Run tests daily at 3 AM
0 3 * * * cd /home/ubuntu/dbt && docker compose exec -T dbt dbt test >> /var/log/dbt-test-cron.log 2>&1

# Create log directory
sudo mkdir -p /var/log
sudo touch /var/log/dbt-cron.log /var/log/dbt-test-cron.log
sudo chmod 666 /var/log/dbt-*.log
```

### Create a Helper Script

```bash
# Create run script
cat > /home/ubuntu/dbt/run-dbt.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/dbt
docker compose exec -T dbt dbt run
EOF

chmod +x /home/ubuntu/dbt/run-dbt.sh

# Now in cron:
# 0 2 * * * /home/ubuntu/dbt/run-dbt.sh >> /var/log/dbt-cron.log 2>&1
```

---

## 🔒 Security Best Practices

### 1. Secure Database

```bash
# Change default passwords immediately
# Edit .env file with strong passwords

# Restrict PostgreSQL to local network only
# Edit docker-compose.yml, comment out ports for postgres:
#   ports:
#     - "5432:5432"  # Remove this line in production
```

### 2. Configure Firewall

```bash
# Install UFW
sudo apt-get install -y ufw

# Allow SSH
sudo ufw allow ssh

# Allow only specific ports
sudo ufw allow 8888/tcp  # Jupyter (if needed)
sudo ufw allow 8080/tcp  # Adminer (if needed)

# Do NOT expose PostgreSQL publicly
# sudo ufw deny 5432/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

### 3. Use Nginx Reverse Proxy (Recommended)

```bash
# Install Nginx
sudo apt-get install -y nginx

# Create config
sudo nano /etc/nginx/sites-available/dbt-jupyter

# Add:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/dbt-jupyter /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 📈 Backup and Recovery

### Backup Database

```bash
# Create backup script
cat > backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p $BACKUP_DIR
DATE=$(date +%Y%m%d_%H%M%S)

docker compose exec -T postgres pg_dump -U dbt_user dbt_analytics | gzip > $BACKUP_DIR/dbt_backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "dbt_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: dbt_backup_$DATE.sql.gz"
EOF

chmod +x backup-db.sh

# Add to cron (daily at midnight)
# 0 0 * * * /home/ubuntu/dbt/backup-db.sh
```

### Restore Database

```bash
# Restore from backup
gunzip -c /home/ubuntu/backups/dbt_backup_YYYYMMDD_HHMMSS.sql.gz | \
  docker compose exec -T postgres psql -U dbt_user -d dbt_analytics
```

---

## 🔧 Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs dbt
docker compose logs postgres

# Rebuild
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Database connection issues

```bash
# Test connection
docker compose exec dbt psql -h postgres -U dbt_user -d dbt_analytics

# Check environment variables
docker compose exec dbt env | grep DB_
```

### Out of disk space

```bash
# Clean up old images
docker system prune -a

# Remove unused volumes
docker volume prune

# Check disk usage
df -h
docker system df
```

### Permission issues

```bash
# Fix ownership
sudo chown -R $USER:$USER /home/ubuntu/dbt

# Fix permissions
chmod -R 755 /home/ubuntu/dbt
chmod 600 /home/ubuntu/dbt/.env
```

---

## 🚀 Updating Your Project

```bash
# Stop services
docker compose down

# Pull latest changes
git pull origin main

# Rebuild images
docker compose build

# Start services
docker compose up -d

# Run migrations if needed
docker compose exec dbt dbt run
```

---

## 📊 Production Considerations

### 1. Use Production Target

```bash
# Set production environment in .env
DB_HOST_PROD=prod-db-server
DB_USER_PROD=prod_user
DB_PASSWORD_PROD=secure_password
DB_NAME_PROD=prod_database

# Run against production
docker compose exec dbt dbt run --target prod
```

### 2. Resource Limits

Add to `docker-compose.yml`:
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

### 3. Health Monitoring

```bash
# Install monitoring (optional)
docker run -d \
  --name=grafana \
  -p 3000:3000 \
  grafana/grafana

# Or use cloud monitoring solutions
```

---

## 📞 Support & Next Steps

- **View logs:** `docker compose logs -f`
- **Check status:** `docker compose ps`
- **Restart service:** `docker compose restart <service>`
- **Full restart:** `docker compose down && docker compose up -d`

**Your services are accessible at:**
- Jupyter Lab: http://your-server-ip:8888
- Adminer: http://your-server-ip:8080
- PostgreSQL: localhost:5432 (inside containers)

---

## 🎯 Quick Reference Commands

```bash
# Start everything
docker compose up -d

# Run dbt
docker compose exec dbt dbt run

# Open shell in dbt container
docker compose exec dbt bash

# View all logs
docker compose logs -f

# Stop everything
docker compose down

# Backup database
docker compose exec postgres pg_dump -U dbt_user dbt_analytics > backup.sql

# Monitor resources
docker stats
```

---

**Next:** Check out `PRODUCTION_DEPLOYMENT.md` for advanced production setup.
