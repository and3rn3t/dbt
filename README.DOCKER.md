# 🐳 Quick Start - Docker Deployment

Get your dbt Analytics environment running in minutes with Docker!

---

## 🚀 One-Command Setup

### On Your Ubuntu Server

```bash
# 1. Clone and enter directory
git clone https://github.com/and3rn3t/dbt.git && cd dbt

# 2. Configure environment
cp .env.example .env
nano .env  # Edit passwords

# 3. Start everything
docker compose up -d

# 4. Test
docker compose exec dbt dbt debug
```

**That's it!** 🎉

---

## 📋 What You Get

- **PostgreSQL Database** - Running on port 5432 (internal)
- **dbt Analytics** - Ready to transform data
- **Jupyter Lab** - Access at `http://your-server-ip:8888`
- **Adminer** - Database UI at `http://your-server-ip:8080`

---

## 🎯 Common Tasks

### Run dbt Models

```bash
docker compose exec dbt dbt run
```

### Load Seed Data

```bash
docker compose exec dbt dbt seed
```

### Run Tests

```bash
docker compose exec dbt dbt test
```

### View Logs

```bash
docker compose logs -f dbt
```

### Backup Database

```bash
./backup-db.sh
```

### Open Shell in Container

```bash
docker compose exec dbt bash
```

---

## 📊 Using Jupyter Lab

1. Open browser to `http://your-server-ip:8888`
2. Navigate to `/notebooks/`
3. Create or open a notebook
4. Start analyzing!

---

## 🔧 Using Make (Easier Commands)

If you have `make` installed:

```bash
make help          # Show all commands
make up            # Start services
make dbt-run       # Run dbt models
make logs          # View logs
make backup        # Backup database
make shell         # Open bash in dbt container
```

---

## 🛑 Stopping Services

```bash
# Stop (data persists)
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v
```

---

## 📖 Full Documentation

- **Detailed Setup:** See `docs/DOCKER_DEPLOYMENT.md`
- **Checklist:** See `DEPLOYMENT_CHECKLIST.md`
- **dbt Guide:** See `dbt_project/README.md`

---

## ❓ Troubleshooting

### Containers won't start?

```bash
docker compose logs
```

### Database connection error?

```bash
docker compose exec dbt dbt debug
```

### Out of memory?

```bash
docker stats
```

### Need to rebuild?

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 🔒 Security Checklist

- [ ] Changed default passwords in `.env`
- [ ] `.env` file secured: `chmod 600 .env`
- [ ] Firewall configured (UFW)
- [ ] PostgreSQL not exposed publicly
- [ ] Backups configured

---

## 📞 Need Help?

Check these files:

- `docs/DOCKER_DEPLOYMENT.md` - Complete deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `docker-compose.yml` - Service configuration

---

**Quick Status Check:**

```bash
docker compose ps
```

**Your services should show "Up" status!** ✅
