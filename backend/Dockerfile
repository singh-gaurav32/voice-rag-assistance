# Single-stage Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock /app/

# Install uv package manager and dependencies
RUN pip install --no-cache-dir uv && uv sync

# Copy the rest of the app code
COPY . /app

# Install uvicorn (ensure it's in PATH)
RUN pip install --no-cache-dir uvicorn

# Expose FastAPI port
EXPOSE 8080

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
