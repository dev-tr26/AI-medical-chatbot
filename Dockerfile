FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8080

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libsndfile1 \
    ca-certificates \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

#  Install dependencies AS ROOT
RUN pip install --no-cache-dir --default-timeout=200 \
    torch==2.2.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir --default-timeout=200 -r requirements.txt

# Create non-root user AFTER install
RUN useradd --system --uid 1000 appuser \
 && chown -R appuser:appuser /app

USER appuser

# Copy app
COPY --chown=appuser:appuser . .

EXPOSE 8080

CMD ["gunicorn", "app:app","--bind", "0.0.0.0:8080","--workers", "1","--threads", "8","--timeout", "300","--worker-class", "sync","--worker-tmp-dir", "/dev/shm","--access-logfile", "-","--error-logfile", "-"]

