## Running the App

To run this Flask app, follow these steps:

1. **Install Docker Desktop**

If you already have Docker Desktop installed, you can skip this step.

If you do not already have Docker Desktop installed, go to the Docker website (https://www.docker.com/products/docker-desktop/) to install Docker Desktop for your OS.

If you are trying to run Docker on Apple Silicon (M1), you may run into a CPU compatibility issue, in which case you should install from this updated DMG: https://docs.docker.com/docker-for-mac/apple-m1/.

2.  **Docker Compose**:

From within the root directory `Pump-Backend/`, run the following command:
```bash
docker compose up
```

If your docker is complaining that you need the Postgres credentials to complete this step, go into your `docker-compose.yml` file and replace the following env variables with whatever you want. The values don't matter because this is a local instance spun up in your own Docker container. For instance:
```
POSTGRES_USER: postgres_user
POSTGRES_PASSWORD: postgres_password
POSTGRES_DB: postgres_db
```

Once you're running, hit `V` in the terminal to view your instance in Docker Desktop!

## Adminer

To use Adminer (https://www.adminer.org/) for database management, Docker Compose then navigate to http://localhost:8080 in a browser.

## Making Migrations

After creating or updating models (or making a new db container), the db schema must be updated using Alembic (https://alembic.sqlalchemy.org/en/latest/index.html)

1. **Detached Docker Compose**:
```bash
make detached
```

2. **If required, create the migration version**:
```bash
make makemigration MESSAGE="<message>"
```

3. **Apply migration**:
```bash
make migrate
```
