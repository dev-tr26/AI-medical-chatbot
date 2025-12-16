FROM python:3.10-slim

# ================= Environment =================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8080 \
    HF_HOME=/tmp/huggingface \
    TRANSFORMERS_CACHE=/tmp/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/tmp/huggingface \
    HF_HUB_DISABLE_XET=1

WORKDIR /app

# ================= System dependencies =================
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libsndfile1 \
    ca-certificates \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ================= Python dependencies =================
COPY requirements.txt .

# Install Torch CPU FIRST
RUN pip install --no-cache-dir --default-timeout=200 \
    torch==2.2.0+cpu \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining deps (torch must NOT be in requirements.txt)
RUN pip install --no-cache-dir --default-timeout=200 -r requirements.txt

# ================= Non-root user =================
RUN useradd --system --uid 1000 appuser \
 && mkdir -p /tmp/huggingface \
 && chown -R appuser:appuser /app /tmp/huggingface

USER appuser

# ================= App code =================
COPY --chown=appuser:appuser . .

EXPOSE 8080

CMD ["gunicorn", "app:app","--bind", "0.0.0.0:8080","--workers", "1","--threads", "8","--timeout", "300","--worker-class", "sync","--worker-tmp-dir", "/dev/shm","--access-logfile", "-","--error-logfile", "-"]
