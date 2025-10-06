# Makefile for dbt Analytics Docker Project
# Quick commands for managing your deployment

.PHONY: help build up down restart logs shell test backup clean

# Default target
.DEFAULT_GOAL := help

help: ## Show this help message
	@echo "dbt Analytics - Docker Commands"
	@echo "================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Build Docker images
	docker compose build

up: ## Start all services
	docker compose up -d
	@echo "Services started. Access:"
	@echo "  Jupyter Lab: http://localhost:8888"
	@echo "  Adminer:     http://localhost:8080"

down: ## Stop all services
	docker compose down

restart: ## Restart all services
	docker compose restart

logs: ## View logs (add SERVICE=name for specific service)
	docker compose logs -f $(SERVICE)

shell: ## Open bash shell in dbt container
	docker compose exec dbt bash

psql: ## Open PostgreSQL shell
	docker compose exec postgres psql -U dbt_user -d dbt_analytics

# dbt commands
dbt-debug: ## Test dbt connection
	docker compose exec dbt dbt debug

dbt-run: ## Run all dbt models
	docker compose exec dbt dbt run

dbt-test: ## Run dbt tests
	docker compose exec dbt dbt test

dbt-docs: ## Generate dbt documentation
	docker compose exec dbt dbt docs generate

dbt-clean: ## Clean dbt artifacts
	docker compose exec dbt dbt clean

# Data management
seed: ## Load seed data
	docker compose exec dbt dbt seed

backup: ## Backup database
	./backup-db.sh

restore: ## Restore database (use BACKUP=filename)
	gunzip -c backups/$(BACKUP) | docker compose exec -T postgres psql -U dbt_user -d dbt_analytics

# Maintenance
clean: ## Remove unused Docker resources
	docker system prune -f

clean-all: ## Remove all Docker resources (WARNING: destructive)
	docker compose down -v
	docker system prune -af

status: ## Show status of all services
	docker compose ps

stats: ## Show resource usage
	docker stats --no-stream

# Development
dev: up logs ## Start services and follow logs

jupyter: ## Open Jupyter Lab
	@echo "Opening Jupyter Lab at http://localhost:8888"
	@which xdg-open > /dev/null && xdg-open http://localhost:8888 || open http://localhost:8888 || echo "Please open http://localhost:8888 in your browser"

adminer: ## Open Adminer
	@echo "Opening Adminer at http://localhost:8080"
	@which xdg-open > /dev/null && xdg-open http://localhost:8080 || open http://localhost:8080 || echo "Please open http://localhost:8080 in your browser"

# Installation
install: build up dbt-debug ## Initial installation
	@echo ""
	@echo "✅ Installation complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run 'make seed' to load sample data"
	@echo "  2. Run 'make dbt-run' to execute dbt models"
	@echo "  3. Access Jupyter at http://localhost:8888"
	@echo ""
