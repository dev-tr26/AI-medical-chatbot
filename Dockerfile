# Use Python 3.10 slim for smaller image size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better layer caching
COPY requirements.txt .

# Install Python dependencies in one layer
# Install CPU-only PyTorch first to avoid conflicts
RUN pip install --no-cache-dir --default-timeout=200 \
    torch==2.2.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir --default-timeout=200 -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Cloud Run uses PORT environment variable
ENV PORT=8080

# Expose port (documentation purposes)
EXPOSE 8080

# Run with Gunicorn (optimized for Cloud Run)
# - 2 workers for better handling of concurrent requests
# - timeout set to 300s (5 min) to match Cloud Run default
# - preload for faster response times
CMD exec gunicorn --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 300 \
    --worker-class sync \
    --worker-tmp-dir /dev/shm \
    --preload \
    --access-logfile - \
    --error-logfile - \
    app:app