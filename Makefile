# =========================
# Variables
# =========================
COMPOSE=docker compose
SERVICE=web
MANAGE=python manage.py
DOMAIN=${DOMAIN:-localhost}

.DEFAULT_GOAL := help

# =========================
# Help
# =========================
help:
	@echo "Available commands:"
	@echo " make certs           Generate self-signed SSL certificates"
	@echo " make up              Start all containers"
	@echo " make down            Stop all containers"
	@echo " make restart         Restart containers"
	@echo " make build           Build containers"
	@echo " make logs            Follow container logs"
	@echo " make ps              List containers"
	@echo " make migrate         Run Django migrations"
	@echo " make makemigrations  Create Django migrations"
	@echo " make superuser       Create Django superuser"
	@echo " make shell           Open Django shell"
	@echo " make dbshell         Open database shell"
	@echo " make check           Run Django system checks"
	@echo " make collectstatic   Collect static files"
	@echo " make startapp   	 Start new app (name=...)"
	@echo " make bash            Open bash in the web container"
	@echo " make update          Zero-downtime update (pull/build/reload Gunicorn)"

# =========================
# SSL Certificates
# =========================
certs:
	@echo "Generating self-signed SSL certificates for $(DOMAIN)..."
	@mkdir -p certs
	@openssl req -x509 -nodes -days 365 \
	  -newkey rsa:2048 \
	  -keyout certs/selfsigned.key \
	  -out certs/selfsigned.crt \
	  -subj "/C=AU/ST=NSW/L=Sydney/O=DocuPath/OU=Dev/CN=$(DOMAIN)"
	@echo "Certificates created in ./certs/"

# =========================
# Docker Commands
# =========================
up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

logs:
	$(COMPOSE) logs -f $(SERVICE)

ps:
	$(COMPOSE) ps

# =========================
# Container - Django Commands
# =========================
migrate:
	$(COMPOSE) exec $(SERVICE) $(MANAGE) migrate

makemigrations:
	$(COMPOSE) exec $(SERVICE) $(MANAGE) makemigrations

superuser:
	$(COMPOSE) exec $(SERVICE) $(MANAGE) createsuperuser

shell:
	$(COMPOSE) exec $(SERVICE) $(MANAGE) shell

dbshell:
	$(COMPOSE) exec $(SERVICE) $(MANAGE) dbshell

check:
	$(COMPOSE) exec $(SERVICE) $(MANAGE) check

collectstatic:
	$(COMPOSE) exec $(SERVICE) $(MANAGE) collectstatic --noinput



# =========================
# Local - Django Commands
# =========================
create_venv:
	python3 -m venv venv

install_requirements:
	pip install --upgrade pip
	pip install -r django/requirements.txt

freeze:
	pip freeze > django/requirements.txt



# =========================
# Utilities
# =========================
bash:
	$(COMPOSE) exec $(SERVICE) bash

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# =========================
# Zero-Downtime Update
# =========================
# update:
# 	$(COMPOSE) pull
# 	$(COMPOSE) build $(SERVICE)
# 	$(COMPOSE) up -d --no-deps $(SERVICE)
# 	# $(COMPOSE) up -d db
# 	# wait for postgres to accept connections
# 	# $(COMPOSE) exec db sh -lc 'until pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB; do sleep 1; done'
# 	# Run migrations and collect static automatically
# 	$(COMPOSE) exec $(SERVICE) $(MANAGE) migrate
# 	$(COMPOSE) exec $(SERVICE) $(MANAGE) collectstatic --noinput
# 	# Reload Gunicorn gracefully
# 	$(COMPOSE) exec $(SERVICE) pkill -HUP gunicorn || true


update:
	$(COMPOSE) down
	$(COMPOSE) pull
	$(COMPOSE) up -d --build --remove-orphans
	$(COMPOSE) exec db sh -lc 'until pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB; do sleep 1; done'
	$(COMPOSE) exec $(SERVICE) $(MANAGE) migrate
	$(COMPOSE) exec $(SERVICE) $(MANAGE) collectstatic --noinput
	# Reload Gunicorn gracefully
	$(COMPOSE) exec $(SERVICE) pkill -HUP gunicorn || true