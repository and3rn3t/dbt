# 🚀 Quick Reference - Docker Deployment

## ⚡ Essential Commands

### Start/Stop

```powershell
docker compose up -d          # Start all services
docker compose down           # Stop all services
docker compose restart        # Restart all services
docker compose ps             # Check status
```

### dbt Commands

```powershell
docker compose exec dbt dbt run         # Run models
docker compose exec dbt dbt test        # Run tests
docker compose exec dbt dbt seed        # Load seeds
docker compose exec dbt dbt debug       # Test connection
docker compose exec dbt bash            # Open shell
```

### Monitoring

```powershell
docker compose logs -f                  # All logs
docker compose logs -f dbt              # dbt logs only
docker stats                            # Resource usage
```

### Maintenance

```powershell
git pull origin main                    # Update code
docker compose build                    # Rebuild images
docker compose up -d                    # Apply changes
./backup-db.sh                          # Backup database
```

---

## 🌐 Access Points

- **Jupyter Lab:** <http://localhost:8888>
- **Adminer:** <http://localhost:8080>
- **PostgreSQL:** localhost:5432 (internal only)

### Adminer Login

- **Server:** postgres
- **Username:** dbt_user
- **Password:** (from .env file)
- **Database:** dbt_analytics

---

## 📁 Key Files

```
Dockerfile              # Image definition
docker-compose.yml      # Services config
.env                   # Your secrets (NEVER commit!)
.env.example           # Template
init-db/01-init.sql    # DB initialization
```

---

## 🔧 Troubleshooting

**Container won't start:**

```powershell
docker compose logs <service>
docker compose restart <service>
```

**Rebuild everything:**

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
```

**Clean up space:**

```powershell
docker system prune -a
docker volume prune
```

---

## 📚 Documentation

- `README.DOCKER.md` - Quick start
- `docs/DOCKER_DEPLOYMENT.md` - Full guide (573 lines)
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step
- `DEPLOYMENT_SUCCESS.md` - Current status

---

## ✅ Current Status (Local)

- [x] Images built
- [x] Services running
- [x] dbt connected
- [x] Jupyter accessible
- [x] Adminer accessible

## 🎯 For Server Deployment

See `docs/DOCKER_DEPLOYMENT.md` Section 1-7
