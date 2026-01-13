# Makefile for DocuForge

# Variables
BACKEND_SERVICE=backend
FRONTEND_SERVICE=frontend
COMPOSE=docker-compose

# Colors for help text
CN = \033[0m
CB = \033[36;1m

.PHONY: help build rebuild up down restart logs logs-backend logs-frontend shell clean prune

help: ## Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CB)%-20s$(CN) %s\n", $$1, $$2}'

# --- Main Lifecycle ---

up: ## Start the full application (Backend, Frontend, Qdrant) in detached mode
	$(COMPOSE) up -d

down: ## Stop and remove all containers and networks
	$(COMPOSE) down

stop: ## Stop containers without removing them
	$(COMPOSE) stop

restart: down up ## Restart the application completely

# --- Logging ---

logs: ## Tail logs from all services
	$(COMPOSE) logs -f

logs-backend: ## Tail logs from the backend only
	$(COMPOSE) logs -f $(BACKEND_SERVICE)

logs-frontend: ## Tail logs from the frontend only
	$(COMPOSE) logs -f $(FRONTEND_SERVICE)

# --- Build & Maintenance ---

build: ## Build the containers
	$(COMPOSE) build

rebuild: ## Force rebuild all containers without cache
	$(COMPOSE) build --no-cache

update: rebuild up ## Full update: Rebuild no-cache and restart

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