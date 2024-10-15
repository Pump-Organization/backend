# Makefile for managing docker-compose and Alembic migrations

# Variables
DOCKER_COMPOSE = docker-compose
SERVICE = pump_backend

# Docker Compose commands
up:
	$(DOCKER_COMPOSE) up
	
detached:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down -v

build:
	$(DOCKER_COMPOSE) build

# Alembic migration commands
upgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic upgrade head

migration:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic revision --autogenerate -m "$(MESSAGE)"

downgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic downgrade $(REVISION)

test:
	$(DOCKER_COMPOSE) exec $(SERVICE) pytest --cov -vv

# Help command
help:
	@echo "Usage:"
	@echo "  make detached          Start the application using docker-compose"
	@echo "  make down              Delete application containers"
	@echo "  make build             Build the Docker images"
	@echo "  make test      	 Run unit tests and print coverage report"
	@echo "  make upgrade           Apply the latest Alembic migrations"
	@echo "  make migration MESSAGE=\"msg\"   Create a new Alembic migration with a message"
	@echo "  make downgrade REVISION=\"rev\"      Downgrade the database to a specific revision"

.PHONY: detached down build restart logs migrate makemigration downgrade test help
