# Use Python 3.11 as base image (compatible with the project)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=webapp.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements-docker.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copy the entire project
COPY . .

# Create necessary directories
RUN mkdir -p logs data/models config

# Make setup script executable
RUN chmod +x setup.sh

# Initialize database and run migrations
RUN cd webapp && python manage.py migrate --run-syncdb

# Expose port
EXPOSE 8000

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash fairagent
RUN chown -R fairagent:fairagent /app
USER fairagent

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["python", "main.py", "--mode", "web"]