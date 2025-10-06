# 🚀 DO THIS NOW - Quick Start

**Your production server is ready! Follow these 3 simple steps.**

---

## Step 1: SSH to Server

Open PowerShell and connect:

```powershell
ssh dbtuser@159.203.140.78
```

---

## Step 2: Run Complete Setup

Once connected, run these commands:

```bash
cd ~/dbt
chmod +x setup-production-complete.sh
./setup-production-complete.sh
```

**When prompted:**

1. Enter a secure password for Jupyter Lab
2. Re-enter the password to confirm
3. Wait for all steps to complete (~1 minute)

---

## Step 3: Open Jupyter Lab

1. Open your browser
2. Go to: <http://159.203.140.78:8888>
3. Enter the password you just set
4. Open: `notebooks/production_verification.ipynb`
5. Click: **Cell → Run All**

---

## ✅ That's It

If the verification notebook runs successfully, you're all set! 🎉

---

## 📚 What's Next?

See the **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** for:

- dbt model development
- Database queries
- Automated tasks
- Troubleshooting
- All available commands

---

## 🔗 Quick Access

| Service | URL | Notes |
|---------|-----|-------|
| **Jupyter Lab** | <http://159.203.140.78:8888> | Password required |
| **Adminer (DB UI)** | <http://159.203.140.78:8080> | Username: andernet |
| **SSH Access** | `ssh dbtuser@159.203.140.78` | Server access |

---

## ⚡ Useful Commands (After Setup)

```bash
# View service status
docker compose ps

# View logs
docker compose logs -f

# Run dbt models
docker compose exec dbt dbt run

# Run dbt tests
docker compose exec dbt dbt test

# Backup database now
./backup-db.sh
```

---

## 🎯 What You Get After Setup

✅ **Jupyter Lab** - Ready for data analysis  
✅ **PostgreSQL** - Database with your NYC education data  
✅ **dbt** - Data transformation engine  
✅ **Automated Backups** - Daily at midnight  
✅ **Automated dbt Runs** - Daily at 2 AM  
✅ **7 CSV Files** - All uploaded and ready to use

---

**Questions? Check the [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)!**
