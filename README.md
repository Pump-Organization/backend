This is a basic "Hello, World!" Flask application.

## Running the App

To run this Flask app, follow these steps:


1.  **Build Docker Image**:
```bash
docker build -t pump_backend .
```

2.  **Run Docker image with port mapping**:
```bash
docker run -p 8080:8080 pump_backend
```
