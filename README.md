This is a basic "Hello, World!" Flask application.

## Running the App

To run this Flask app, follow these steps:


1.  **Docker Compose**:
```bash
% docker compose up
```

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
