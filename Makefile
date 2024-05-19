# Makefile for managing docker-compose and Alembic migrations

# Variables
DOCKER_COMPOSE = docker-compose
SERVICE = pump_backend

# Docker Compose commands
detached:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) build

restart: down up

logs:
	$(DOCKER_COMPOSE) logs -f

# Alembic migration commands
migrate:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic upgrade head

makemigration:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic revision --autogenerate -m "$(MESSAGE)"

downgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic downgrade $(REVISION)

# Help command
help:
	@echo "Usage:"
	@echo "  make detached          Start the application using docker-compose"
	@echo "  make down              Stop the application"
	@echo "  make build             Build the Docker images"
	@echo "  make restart           Restart the application"
	@echo "  make logs              Follow the logs of the application"
	@echo "  make migrate           Apply the latest Alembic migrations"
	@echo "  make makemigration MESSAGE=\"msg\"   Create a new Alembic migration with a message"
	@echo "  make downgrade REVISION=\"rev\"      Downgrade the database to a specific revision"

.PHONY: detached down build restart logs migrate makemigration downgrade help
