# Single-stage Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv package manager and dependencies
RUN pip install --no-cache-dir uv

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock /app/

ENV UV_PROJECT=/app

# Install dependencies
RUN uv sync

# Copy the rest of the app code
COPY . /app

# Expose FastAPI port
EXPOSE 8080

# Run app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
