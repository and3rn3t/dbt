# dbt Analytics Docker Image
FROM python:3.11-slim

# Set metadata
LABEL maintainer="and3rn3t"
LABEL description="dbt Analytics with PostgreSQL adapter"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DBT_PROFILES_DIR=/app/dbt_project

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements-datascience.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-datascience.txt

# Copy dbt project
COPY dbt_project/ /app/dbt_project/

# Copy scripts for utilities
COPY scripts/ /app/scripts/

# Create directories for data and logs
RUN mkdir -p /app/data/raw /app/data/processed /app/data/staging /app/logs && \
    chmod -R 755 /app

# Validate dbt installation
RUN dbt --version

# Set working directory to dbt project
WORKDIR /app/dbt_project

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD dbt debug || exit 1

# Default command
CMD ["dbt", "run"]
