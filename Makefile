# Makefile for DocuForge Backend

# Variables
SERVICE_NAME=backend
COMPOSE=docker-compose

# Colors for help text
CN = \033[0m
CB = \033[36;1m

.PHONY: help build build-nc up down restart logs shell clean prune

help: ## Show this help menu
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(CB)%-15s$(CN) %s\n", $$1, $$2}'

# --- Main Lifecycle ---

up: ## Start the application in detached mode
	$(COMPOSE) up -d

down: ## Stop and remove containers and networks
	$(COMPOSE) down

stop: ## Stop containers without removing them
	$(COMPOSE) stop

restart: down up ## Restart the application

logs: ## Tail the logs of the backend service
	$(COMPOSE) logs -f $(SERVICE_NAME)

# --- Build & Maintenance ---

build: ## Build the containers (standard)
	$(COMPOSE) build

rebuild: ## Force rebuild WITHOUT cache (Fixes dependency mismatches)
	$(COMPOSE) build --no-cache

update: rebuild up ## Full update: Rebuild no-cache and restart

shell: ## Open a shell inside the running backend container
	$(COMPOSE) exec $(SERVICE_NAME) /bin/bash

# --- Cleanup ---

clean: ## Stop containers, remove volumes, and remove orphan containers
	$(COMPOSE) down --volumes --remove-orphans

clean-py: ## Remove local Python cache files (__pycache__, .pyc, etc)
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -delete

prune: ## DANGEROUS: Remove all unused containers, networks, images (both dangling and unreferenced)
	docker system prune -a --volumes