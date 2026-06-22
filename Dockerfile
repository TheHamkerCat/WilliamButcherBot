# ============= BASE STAGE =============
FROM python:3.12-slim-bullseye AS base

WORKDIR /wbb

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    gcc \
    build-essential \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .

# ============= PRODUCTION STAGE =============
FROM base AS production

ENV UV_NO_DEV=1

# Install dependencies without dev packages
RUN uv sync --no-dev

# Copy application code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import asyncio; from wbb import log; log.info('Health check passed')" || exit 1

# Start bot
ENTRYPOINT ["uv", "run", "python", "-m", "wbb"]
