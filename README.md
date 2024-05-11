This is a basic "Hello, World!" Flask application.

## Running the App

To run this Flask app, follow these steps:


1.  **Docker Compose**:
```bash
% docker compose up
```

## Adminer

To use Adminer (https://www.adminer.org/) for database management, Docker Compose then navigate to http://localhost:8080 in a browser.

## Making Migrations

After creating or updating models (or making a new db container), the db schema must be updated using Alembic (https://alembic.sqlalchemy.org/en/latest/index.html)

1. **Detached Docker Compose**:
```bash
% docker compose up -d
```

2. **Start an interactive shell in the app**:
```bash
% docker compose exec pump_backend sh
```

3. **Create migration version**:
```bash
\# alembic revision --autogenerate -m '<version_name>'
```

4. **Apply migration**:
```bash
\# alembic upgrade head
```
