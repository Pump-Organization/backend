## Running the App

1. **Create local .env config**

After cloning the repo create an .env file in the root `Pump-Backend` directory and populate it with the following metadata:

```bash
touch .env

echo "POSTGRES_HOST=pump-db-host:5432
POSTGRES_DB=pump_db
POSTGRES_USER=jennings_and_siq
POSTGRES_PASSWORD=bobcancode955
JWT_SECRET=supersecret" >> .env
```

2. **Install Docker Desktop**

If you already have Docker Desktop installed, you can skip this step.

If you do not already have Docker Desktop installed, go to the Docker website (https://www.docker.com/products/docker-desktop/) to install Docker Desktop for your OS.

If you are trying to run Docker on Apple Silicon (M1), you may run into a CPU compatibility issue, in which case you should install from this updated DMG: https://docs.docker.com/docker-for-mac/apple-m1/.

3.  **Docker Compose**:

Ensure the Docker Desktop application is running in the background. Sometimes you need to open it manually by clicking on the Application icon. The home UI should say “Your running containers show up here.”

From within the root directory `Pump-Backend`, aggregate the Docker service:

```bash
docker compose up
```

If your docker is complaining that you need the Postgres credentials to complete this step, go into your `docker-compose.yml` file and replace the following env variables with whatever you want. The values don't matter because this is a local instance spun up in your own Docker container. For instance:

```
POSTGRES_USER: postgres_user
POSTGRES_PASSWORD: postgres_password
POSTGRES_DB: postgres_db
```

Once the debugger is active, you're up and running. Hit `V` in the terminal to view your instance in Docker Desktop. You should see 3 packages running.

## Adminer

To use Adminer (https://www.adminer.org/) for database visualization, Docker Compose then navigate to http://localhost:8080 in a browser.

## Making Migrations

After pulling model changes, the db must be upgraded to the new migrations using Alembic (https://alembic.sqlalchemy.org/en/latest/index.html). This is only necessary when the db schema is changed.

For now, we can nuke our db then rebuild with the new migrations. After we deploy, we'll meet to apply migrations.

1. **Delete local Pump containers and volumes**:

```bash
make down
```

2. **Detached Docker Compose**:

```bash
make detached
```

3. **Apply migration**:

```bash
make migrate
```

You should see your local DB spun up in `migrations/versions/`. If you are having trouble, run `docker compose down` to kill the running Docker instance, remove all files inside `migrations/versions/`, before recomposing `docker compose up` and trying the migration again.

## Postman

You may want to use the Postman interface to populate your local DB with object instances and test end-to-end functionality.

1. **Download Postman (https://www.postman.com/downloads/) desktop application.**

2. **Import the following APIs**

Request the Postman APIs from us.

File > Import > [Copy + Paste the file we send you]
