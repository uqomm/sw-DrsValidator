# DRS Validation Tool - Docker Container
FROM python:3.14-slim

# Set maintainer info
LABEL maintainer="DRS Monitoring Team"
LABEL description="DRS Device Validation Tool for Technicians"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    iputils-ping \
    telnet \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt ./requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

# Create necessary directories
RUN mkdir -p /app/logs /app/results /app/temp

# Expose the port
EXPOSE 8089

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8089/health || exit 1

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_ENV=production
ENV LOG_LEVEL=INFO

# Run the validation service
CMD ["python", "-m", "uvicorn", "validation_app:app", "--host", "0.0.0.0", "--port", "8089", "--log-level", "info"]
