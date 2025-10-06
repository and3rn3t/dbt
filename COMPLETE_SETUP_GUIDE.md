# 🚀 Complete Production Setup Guide

**Server:** 159.203.140.78  
**Status:** ✅ Deployed, Data Uploaded  
**Next:** Complete configuration and testing

---

## ✅ What's Already Done

- [x] Docker environment deployed
- [x] All 4 services running (PostgreSQL, dbt, Jupyter, Adminer)
- [x] Database initialized with schemas
- [x] Data files uploaded (7 CSV files)
- [x] Firewall configured
- [x] Services accessible

---

## 📋 Complete Setup - Step by Step

### **Step 1: Connect to Server**

From your Windows PowerShell:

```powershell
ssh dbtuser@159.203.140.78
```

Password: `[your dbtuser password]`

---

### **Step 2: Navigate to Project Directory**

```bash
cd ~/dbt
```

---

### **Step 3: Run the Complete Setup Script**

This script will:
- Set Jupyter password
- Verify data files
- Configure backup scripts
- Configure dbt run scripts
- Set up automated cron jobs (daily backups & dbt runs)

```bash
chmod +x setup-production-complete.sh
./setup-production-complete.sh
```

**Follow the prompts:**
1. Enter a password for Jupyter Lab (use something secure!)
2. Re-enter the password to confirm
3. Review the output to verify all steps completed

---

### **Step 4: Verify Services**

```bash
docker compose ps
```

You should see:
- ✅ `dbt_postgres` - healthy
- ✅ `dbt_analytics` - healthy
- ✅ `dbt_jupyter` - healthy
- ✅ `dbt_adminer` - Up

---

### **Step 5: Test Jupyter Lab**

1. **Open in browser:** http://159.203.140.78:8888
2. **Enter the password** you just set
3. **Open the verification notebook:** `notebooks/production_verification.ipynb`
4. **Run all cells** (Cell → Run All)

The notebook will test:
- Python environment
- Database connection
- Data files
- Pandas/NumPy
- Matplotlib/Seaborn visualizations

---

## 🔒 Security Checklist

After setup completion, verify:

- [ ] Jupyter Lab requires password
- [ ] Firewall is active (ports 22, 8888, 8080 only)
- [ ] Automated backups configured (cron)
- [ ] Automated dbt runs configured (cron)
- [ ] .env file permissions are 600

---

## 📊 Access Your Services

### **Jupyter Lab**
- **URL:** http://159.203.140.78:8888
- **Use:** Data analysis, notebooks
- **Password:** ✅ Set during setup

### **Adminer** (Database UI)
- **URL:** http://159.203.140.78:8080
- **System:** PostgreSQL
- **Server:** postgres
- **Username:** andernet
- **Password:** LocalTestPassword123!
- **Database:** dbt_analytics

### **SSH Access**
```bash
ssh dbtuser@159.203.140.78
```

---

## 🗄️ Data Files Available

The following files are now on the server in `~/dbt/data/processed/`:

1. `nyc_education_analyzed.csv` - Main analyzed dataset
2. `top_50_nyc_schools.csv` - Top performing schools
3. `borough_summary.csv` - Borough-level statistics
4. `ml_features_dataset.csv` - ML features
5. `school_predictions.csv` - Model predictions
6. `feature_importance.csv` - Feature importance scores
7. `model_comparison.csv` - Model performance comparison

---

## 🤖 Automated Tasks

After running the setup script, these tasks run automatically:

### **Daily Backups** (00:00 UTC)
- Dumps PostgreSQL database
- Compresses with gzip
- Stores in `~/dbt/backups/`
- Keeps 7 days of backups
- Runs: `/home/dbtuser/dbt/backup-db.sh`

### **Daily dbt Runs** (02:00 UTC)
- Runs dbt transformations
- Logs to `~/dbt/logs/`
- Keeps 30 days of logs
- Runs: `/home/dbtuser/dbt/scripts/run-dbt.sh run`

### **View Scheduled Jobs**
```bash
crontab -l
```

---

## 📚 Essential Commands

### **Docker Commands**

```bash
# View all services
docker compose ps

# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f jupyter
docker compose logs -f dbt
docker compose logs -f postgres

# Restart all services
docker compose restart

# Restart specific service
docker compose restart jupyter

# Stop all services
docker compose down

# Start all services
docker compose up -d
```

### **dbt Commands**

```bash
# Run dbt debug (test connection)
docker compose exec dbt dbt debug

# Run dbt models
docker compose exec dbt dbt run

# Run dbt tests
docker compose exec dbt dbt test

# Load seed data
docker compose exec dbt dbt seed

# Generate documentation
docker compose exec dbt dbt docs generate

# Run specific model
docker compose exec dbt dbt run --select model_name
```

### **Database Commands**

```bash
# Connect to PostgreSQL (interactive)
docker compose exec postgres psql -U andernet -d dbt_analytics

# Run SQL query
docker compose exec postgres psql -U andernet -d dbt_analytics -c "SELECT COUNT(*) FROM staging.schools;"

# List all tables
docker compose exec postgres psql -U andernet -d dbt_analytics -c "\dt staging.*"
```

### **Backup Commands**

```bash
# Run backup manually
./backup-db.sh

# List backups
ls -lh ~/dbt/backups/

# Restore from backup
gunzip < ~/dbt/backups/dbt_analytics_YYYY-MM-DD.sql.gz | docker compose exec -T postgres psql -U andernet -d dbt_analytics
```

---

## 🎯 Next Steps - dbt Development

### **1. Create Staging Models**

Create files in `~/dbt/dbt_project/models/staging/`:

```bash
cd ~/dbt/dbt_project/models/staging
```

**Example:** `stg_nyc_schools.sql`

```sql
-- models/staging/stg_nyc_schools.sql
{{ config(materialized='view') }}

with source as (
    select * from {{ source('raw', 'nyc_education') }}
),

renamed as (
    select
        school_name,
        borough,
        grade_level,
        total_enrollment,
        avg_class_size,
        student_teacher_ratio,
        graduation_rate,
        college_career_rate,
        created_at
    from source
    where school_name is not null
)

select * from renamed
```

### **2. Create Marts Models**

Create files in `~/dbt/dbt_project/models/marts/`:

**Example:** `mart_school_performance.sql`

```sql
-- models/marts/mart_school_performance.sql
{{ config(materialized='table') }}

with schools as (
    select * from {{ ref('stg_nyc_schools') }}
),

performance as (
    select
        borough,
        count(*) as total_schools,
        avg(graduation_rate) as avg_graduation_rate,
        avg(college_career_rate) as avg_college_rate,
        avg(student_teacher_ratio) as avg_student_teacher_ratio
    from schools
    group by borough
)

select * from performance
order by avg_graduation_rate desc
```

### **3. Define Data Tests**

Create `~/dbt/dbt_project/models/staging/staging.yml`:

```yaml
version: 2

models:
  - name: stg_nyc_schools
    description: Staging layer for NYC school data
    columns:
      - name: school_name
        description: School name
        tests:
          - not_null
          - unique
      
      - name: borough
        description: NYC borough
        tests:
          - not_null
          - accepted_values:
              values: ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
      
      - name: graduation_rate
        description: Graduation rate (0-100)
        tests:
          - not_null
          - relationships:
              to: ref('stg_nyc_schools')
              field: graduation_rate
```

### **4. Run dbt Transformations**

```bash
# Run all models
docker compose exec dbt dbt run

# Run tests
docker compose exec dbt dbt test

# Generate documentation
docker compose exec dbt dbt docs generate
```

---

## 🔍 Monitoring & Maintenance

### **Check System Resources**

```bash
# Disk usage
df -h

# Docker disk usage
docker system df

# Memory usage
free -h

# CPU usage
top
```

### **Clean Up Old Data**

```bash
# Remove old Docker images
docker image prune -a

# Remove old logs (older than 30 days)
find ~/dbt/logs -name "*.log" -mtime +30 -delete

# Remove old backups (older than 7 days)
find ~/dbt/backups -name "*.sql.gz" -mtime +7 -delete
```

### **View Logs**

```bash
# dbt logs
tail -f ~/dbt/logs/dbt_run.log

# Cron logs
grep CRON /var/log/syslog | tail -20

# Docker logs
docker compose logs --tail=100 -f
```

---

## ⚠️ Troubleshooting

### **Jupyter Lab Not Accessible**

```bash
# Check if service is running
docker compose ps jupyter

# View logs
docker compose logs jupyter

# Restart Jupyter
docker compose restart jupyter
```

### **Database Connection Issues**

```bash
# Check if PostgreSQL is running
docker compose ps postgres

# Test connection
docker compose exec postgres psql -U andernet -d dbt_analytics -c "SELECT 1;"

# View logs
docker compose logs postgres
```

### **dbt Errors**

```bash
# Run debug
docker compose exec dbt dbt debug

# Check profiles
docker compose exec dbt cat /app/dbt_project/profiles.yml

# View dbt logs
docker compose logs dbt
```

### **Out of Disk Space**

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a --volumes

# Remove old backups
rm ~/dbt/backups/*.sql.gz.old
```

---

## 📖 Additional Resources

### **Documentation**
- dbt: https://docs.getdbt.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Docker: https://docs.docker.com/
- Jupyter: https://jupyter.org/documentation

### **Project Files**
- `/home/dbtuser/dbt/` - Project root
- `/home/dbtuser/dbt/dbt_project/` - dbt models
- `/home/dbtuser/dbt/data/` - Data files
- `/home/dbtuser/dbt/notebooks/` - Jupyter notebooks
- `/home/dbtuser/dbt/logs/` - Application logs
- `/home/dbtuser/dbt/backups/` - Database backups

---

## ✅ Setup Verification Checklist

Before proceeding with development, verify:

- [ ] All Docker services are healthy
- [ ] Jupyter Lab accessible with password
- [ ] Adminer accessible and can connect to database
- [ ] Data files present in `~/dbt/data/processed/`
- [ ] Verification notebook runs successfully
- [ ] dbt debug passes all checks
- [ ] Automated backups scheduled (cron)
- [ ] Automated dbt runs scheduled (cron)
- [ ] Firewall active and configured
- [ ] All passwords are secure

---

## 🎉 You're Ready!

Once the setup script completes and all services are verified, you're ready to:

1. **Analyze data** in Jupyter Lab
2. **Create dbt models** for transformations
3. **Build dashboards** from transformed data
4. **Automate workflows** with cron jobs

---

**Questions or Issues?**

Review the logs:
```bash
docker compose logs -f
tail -f ~/dbt/logs/dbt_run.log
```

Check service status:
```bash
docker compose ps
```

**Happy analyzing! 🚀📊**
