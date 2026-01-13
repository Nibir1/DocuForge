# Makefile for DocuForge

# Variables
BACKEND_SERVICE=backend
FRONTEND_SERVICE=frontend
COMPOSE=docker-compose

# Colors for help text
CN = \033[0m
CB = \033[36;1m

.PHONY: help build rebuild up down restart logs logs-backend logs-frontend shell test test-cov clean prune

help: ## Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CB)%-20s$(CN) %s\n", $$1, $$2}'

# --- Main Lifecycle ---

up: ## Start the full application (Backend, Frontend, Qdrant) in detached mode
	$(COMPOSE) up -d
	@echo "✅ Application running at http://localhost:5173"

down: ## Stop and remove all containers and networks
	$(COMPOSE) down

stop: ## Stop containers without removing them
	$(COMPOSE) stop

restart: ## Restart the application completely
	down up
	@echo "✅ Application running at http://localhost:5173"

# --- Logging ---

logs: ## Tail logs from all services
	$(COMPOSE) logs -f

logs-backend: ## Tail logs from the backend only
	$(COMPOSE) logs -f $(BACKEND_SERVICE)

logs-frontend: ## Tail logs from the frontend only
	$(COMPOSE) logs -f $(FRONTEND_SERVICE)

# --- Testing ---

test: ## Run the backend test suite (standard)
	$(COMPOSE) exec $(BACKEND_SERVICE) pytest tests/

test-cov: ## Run backend tests with coverage report
	$(COMPOSE) exec $(BACKEND_SERVICE) pytest --cov=app tests/

# --- Build & Maintenance ---

build: ## Build the containers
	$(COMPOSE) build

rebuild: ## Force rebuild all containers without cache
	$(COMPOSE) build --no-cache

update: ## Full update: Rebuild no-cache and restart the application
	rebuild up
	@echo "✅ Application running at http://localhost:5173"

shell: ## Open a shell inside the backend container
	$(COMPOSE) exec $(BACKEND_SERVICE) /bin/bash

# --- Cleanup ---

clean: ## Stop containers, remove volumes, and remove orphan containers
	$(COMPOSE) down --volumes --remove-orphans

clean-py: ## Remove local Python cache files (__pycache__, .pyc)
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

prune: ## DANGEROUS: Remove all unused containers, networks, and images
	docker system prune -a --volumes