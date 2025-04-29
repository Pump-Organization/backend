# Makefile for managing docker-compose and Alembic migrations

# Variables
DOCKER_COMPOSE = docker compose
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

shell:
	$(DOCKER_COMPOSE) exec -it $(SERVICE) sh

# Alembic migration commands
upgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic upgrade head

migration:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

downgrade:
	$(DOCKER_COMPOSE) exec $(SERVICE) alembic downgrade -1

test:
	$(DOCKER_COMPOSE) exec $(SERVICE) pytest --cov -vv

format:
	$(DOCKER_COMPOSE) exec $(SERVICE) black .

# Help command
help:
	@echo "Usage:"
	@echo "  make detached          Start the application using docker-compose"
	@echo "  make down              Delete application containers"
	@echo "  make build             Build the Docker images"
	@echo "  make shell             Open a shell in the application container"
	@echo "  make format            Format the repo using Black"
	@echo "  make test      	 Run unit tests and print coverage report"
	@echo "  make upgrade           Apply the latest Alembic migrations"
	@echo "  make migration \"msg\"   Create a new Alembic migration with a message"
	@echo "  make downgrade"      Downgrade the database to the previous revision"

.PHONY: detached down build restart logs migrate makemigration downgrade test help
