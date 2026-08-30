# Multi-stage build for FastAPI service
FROM python:3.12-slim AS builder

WORKDIR /build

# Install poetry
RUN pip install poetry==1.7.1

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Configure poetry: no interactive, no venv (we'll use system python)
RUN poetry config virtualenvs.create false

# Install dependencies (no dev dependencies for production)
RUN poetry install --no-interaction --no-ansi --only main --no-root

# Copy application code
COPY app ./app
COPY scripts ./scripts

# Runtime
FROM python:3.12-slim

LABEL maintainer="MDM Team <mdm-team@bankxyz.co.id>"
LABEL version="1.0.0"
LABEL description="MDM {{SERVICE_NAME}}"

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tini \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN usergroupadd -g 1001 mdm && useradd -u 1001 -g mdm -s /bin/bash mdm

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY --from=builder /build/app ./app
COPY --from=builder /build/scripts ./scripts

USER mdm
EXPOSE {{SERVER_PORT}}

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:{{SERVER_PORT}}/api/v1/health/ || exit 1

# Production-grade uvicorn
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    WORKERS=2 \
    WORKER_CLASS=uvicorn.workers.UvicornWorker \
    HOST=0.0.0.0 \
    PORT={{SERVER_PORT}}

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers ${WORKERS} --proxy-headers --forwarded-allow-ips='*' --access-log"]
