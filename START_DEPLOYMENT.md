# 🚀 DEPLOY TO PRODUCTION NOW - STEP BY STEP

**Status:** ✅ Ready to Deploy  
**Repository:** https://github.com/and3rn3t/dbt  
**Latest Commit:** Synced and pushed

---

## 🎯 **QUICK DEPLOY (3 Commands)**

SSH into your Ubuntu server and run:

```bash
git clone https://github.com/and3rn3t/dbt.git && cd dbt
chmod +x deploy-production.sh
./deploy-production.sh
```

**That's it!** The script handles everything automatically.

---

## 📋 **Pre-Deployment Checklist**

Before you start, ensure you have:

- [ ] Ubuntu 20.04+ server (physical or cloud)
- [ ] SSH access: `ssh user@your-server-ip`
- [ ] Sudo privileges
- [ ] At least 4GB RAM
- [ ] At least 20GB disk space
- [ ] Strong passwords prepared

---

## 🖥️ **Deployment Process**

### **Step 1: Connect to Your Server**

```bash
# From your Windows machine
ssh username@your-server-ip

# Example:
# ssh ubuntu@192.168.1.100
# or
# ssh root@your-droplet-ip
```

### **Step 2: Run Deployment Commands**

Once connected to your Ubuntu server, run:

```bash
# Clone repository
git clone https://github.com/and3rn3t/dbt.git

# Enter directory
cd dbt

# Make script executable
chmod +x deploy-production.sh

# Run deployment (interactive)
./deploy-production.sh
```

### **Step 3: Follow the Prompts**

The script will:

1. **Update system** ⏱️ 2-3 minutes
   - Updates Ubuntu packages
   - Installs prerequisites

2. **Install Docker** ⏱️ 2-3 minutes
   - Installs Docker Engine
   - Configures user permissions

3. **Configure environment** ⏱️ 1-2 minutes
   - Opens `.env` file for editing
   - **⚠️ IMPORTANT:** Change all passwords here!

4. **Set up firewall** ⏱️ 1 minute
   - Enables UFW
   - Opens necessary ports

5. **Build Docker images** ⏱️ 5-10 minutes
   - Downloads Python base image
   - Installs all dependencies
   - Builds dbt service

6. **Start services** ⏱️ 1-2 minutes
   - Starts PostgreSQL
   - Starts dbt
   - Starts Jupyter
   - Starts Adminer

7. **Verify installation** ⏱️ 1 minute
   - Tests dbt connection
   - Checks service health

**Total Time:** ~15-20 minutes

---

## 🔐 **CRITICAL: Configure .env File**

When the script opens the `.env` file, **CHANGE THESE VALUES:**

```bash
# ⚠️ CHANGE THIS PASSWORD - CRITICAL!
DB_PASSWORD=YourSuperSecurePassword123!

# Database configuration (keep these)
DB_HOST=postgres
DB_PORT=5432
DB_NAME=dbt_analytics
DB_USER=dbt_user

# Production database (if using separate prod DB)
DB_HOST_PROD=your-prod-server
DB_USER_PROD=prod_user
DB_PASSWORD_PROD=AnotherSecurePassword456!
DB_NAME_PROD=prod_database

# Ports (can keep defaults)
JUPYTER_PORT=8888
ADMINER_PORT=8080
```

**Security Rules:**
- ✅ Use strong passwords (12+ characters)
- ✅ Include uppercase, lowercase, numbers, symbols
- ✅ Never use default passwords in production
- ✅ Different passwords for dev and prod

**Example Strong Password:** `Tr@nsf0rm!Data#2025`

---

## 🌐 **After Deployment - Access Services**

### **Get Your Server IP:**

```bash
# On your server, run:
hostname -I | awk '{print $1}'

# Or check with:
ip addr show | grep "inet " | grep -v 127.0.0.1
```

### **Access Points:**

**Jupyter Lab:**
- URL: `http://YOUR_SERVER_IP:8888`
- No password (set one later for security)
- Full data science environment

**Adminer (Database UI):**
- URL: `http://YOUR_SERVER_IP:8080`
- Server: `postgres`
- Username: `dbt_user`
- Password: (what you set in .env)
- Database: `dbt_analytics`

**PostgreSQL:**
- Internal only (not exposed)
- Host: `postgres` (from within containers)
- Port: 5432 (internal)

---

## ✅ **Verify Deployment**

After the script completes, verify everything:

```bash
# Check all containers are running
docker compose ps

# Expected output:
# dbt_postgres    Up (healthy)
# dbt_analytics   Up (health: starting)
# dbt_jupyter     Up (healthy)
# dbt_adminer     Up

# Test dbt connection
docker compose exec dbt dbt debug

# Should see: "All checks passed!"

# View logs
docker compose logs --tail=50

# Check resource usage
docker stats --no-stream
```

---

## 🎮 **Post-Deployment Tasks**

### **1. Set Up Automated Backups**

```bash
# Make backup script executable
chmod +x backup-db.sh

# Test backup
./backup-db.sh

# Add to crontab (daily at midnight)
crontab -e

# Add this line:
0 0 * * * /home/ubuntu/dbt/backup-db.sh
```

### **2. Set Up Automated dbt Runs**

```bash
# Make run script executable
chmod +x scripts/run-dbt.sh

# Add to crontab (daily at 2 AM)
crontab -e

# Add this line:
0 2 * * * /home/ubuntu/dbt/scripts/run-dbt.sh run
```

### **3. Secure Jupyter (if public)**

```bash
# Generate password hash
docker compose exec jupyter jupyter server password

# Follow prompts to set password
```

### **4. Test Everything**

```bash
# Run dbt models
docker compose exec dbt dbt run

# Load seed data (if you have any)
docker compose exec dbt dbt seed

# Run tests
docker compose exec dbt dbt test

# Open shell
docker compose exec dbt bash
```

---

## 📊 **Common Commands Reference**

```bash
# Service Management
docker compose up -d              # Start services
docker compose down               # Stop services
docker compose restart            # Restart all
docker compose ps                 # Check status

# Logs
docker compose logs -f            # Live logs (all)
docker compose logs -f dbt        # Live logs (dbt only)
docker compose logs --tail=100    # Last 100 lines

# dbt Commands
docker compose exec dbt dbt run           # Run models
docker compose exec dbt dbt test          # Run tests
docker compose exec dbt dbt seed          # Load seeds
docker compose exec dbt dbt debug         # Test connection
docker compose exec dbt bash              # Open shell

# Database
docker compose exec postgres psql -U dbt_user -d dbt_analytics
docker compose exec postgres pg_dump -U dbt_user dbt_analytics > backup.sql

# Maintenance
docker compose pull               # Pull latest images
docker compose build              # Rebuild images
docker system prune -a            # Clean up
```

---

## 🔧 **Troubleshooting**

### **Issue: Script fails at Docker installation**

```bash
# Try manual Docker install
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker

# Then continue with:
./deploy-production.sh
```

### **Issue: Can't access Jupyter/Adminer**

```bash
# Check firewall
sudo ufw status

# Should show 8888 and 8080 as ALLOW

# If not, add them:
sudo ufw allow 8888/tcp
sudo ufw allow 8080/tcp

# Check containers
docker compose ps

# Restart services
docker compose restart
```

### **Issue: dbt connection fails**

```bash
# Check PostgreSQL is running
docker compose exec postgres pg_isready

# Check environment variables
docker compose exec dbt env | grep DB_

# Check logs
docker compose logs postgres
docker compose logs dbt

# Restart database
docker compose restart postgres
sleep 10
docker compose exec dbt dbt debug
```

### **Issue: Out of disk space**

```bash
# Check space
df -h

# Clean Docker
docker system prune -a
docker volume prune

# Check again
df -h
```

### **Issue: Service won't start**

```bash
# Check specific service logs
docker compose logs <service_name>

# Try rebuilding
docker compose down
docker compose build --no-cache
docker compose up -d

# Check status
docker compose ps
```

---

## 🎯 **Success Checklist**

After deployment, verify:

- [ ] All 4 containers running (ps shows "Up")
- [ ] dbt debug passes ("All checks passed!")
- [ ] Can access Jupyter at http://SERVER_IP:8888
- [ ] Can access Adminer at http://SERVER_IP:8080
- [ ] Can login to Adminer with configured password
- [ ] Backups directory created
- [ ] Scripts are executable
- [ ] Firewall configured (ufw status)
- [ ] .env file secured (ls -la .env shows 600)

---

## 🔒 **Production Security Checklist**

Before going live:

- [ ] Changed all default passwords
- [ ] Set Jupyter password
- [ ] Disabled or secured Adminer
- [ ] Configured SSL/TLS (if public)
- [ ] Set up automated backups
- [ ] Configured monitoring
- [ ] Documented access credentials (in password manager)
- [ ] Tested backup restore procedure
- [ ] Set up log rotation
- [ ] Configured alerts

---

## 📞 **Get Help**

**Documentation:**
- Full guide: `docs/DOCKER_DEPLOYMENT.md`
- Checklist: `docs/DEPLOYMENT_CHECKLIST.md`
- Quick ref: `QUICK_REFERENCE.md`
- Production guide: `PRODUCTION_DEPLOY.md`

**Support:**
- Check logs: `docker compose logs`
- Check status: `docker compose ps`
- Test connection: `docker compose exec dbt dbt debug`

---

## 🎉 **You're Ready!**

**Everything is prepared:**
- ✅ Code pushed to GitHub
- ✅ Deployment script ready
- ✅ Documentation complete
- ✅ Security best practices included

**Time to deploy:** ~15-20 minutes  
**Difficulty:** Easy (automated script)  
**What you need:** Ubuntu server access

---

## 🚀 **LET'S GO!**

**Copy these commands to your Ubuntu server:**

```bash
git clone https://github.com/and3rn3t/dbt.git && cd dbt
chmod +x deploy-production.sh
./deploy-production.sh
```

**Then access your services at:**
- Jupyter: http://YOUR_IP:8888
- Adminer: http://YOUR_IP:8080

**Good luck! You've got this! 💪**

---

**Questions during deployment?** Check the logs or refer to the documentation!
