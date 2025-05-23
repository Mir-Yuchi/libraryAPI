# Dockerfile

FROM python:3.13-slim AS base

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry via pip
RUN pip install --no-cache-dir poetry

# Set working directory
WORKDIR /app

# Copy only dependency manifests to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install Python dependencies (without installing the project itself)
RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi --only main --no-root

# Copy the rest of the application code
COPY . .

# Expose the application port
EXPOSE 8000

# Run migrations then start Uvicorn
CMD ["sh", "-c", "poetry run alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
