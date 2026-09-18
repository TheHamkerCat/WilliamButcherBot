# ============= BASE STAGE =============
FROM python:3.12-slim-bookworm AS base

WORKDIR /wbb

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# install required system dependencies for python packages
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    git gcc build-essential \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .

# ============= PRODUCTION STAGE =============
FROM base

ENV UV_NO_DEV=1
RUN uv sync

COPY . .

# Starting Bot
ENTRYPOINT ["uv", "run", "python", "-m", "wbb"]
