FROM python:3.11.9-alpine3.19

# Install PostgreSQL development files
RUN apk update && apk add --no-cache postgresql-dev gcc musl-dev libffi-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py"]
