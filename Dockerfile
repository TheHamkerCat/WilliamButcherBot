# ============= BUILD STAGE =============
FROM python:3.12-slim-bookworm AS build

WORKDIR /wbb

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl ca-certificates \
    git gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"
ENV UV_NO_DEV=1

COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
RUN uv sync

# MongoDB tools need the krb5 runtime libraries.
ARG TARGETARCH
ARG MONGO_TOOLS_VERSION=100.20.1
RUN case "${TARGETARCH:-$(uname -m)}" in \
        amd64|x86_64) tools_url="https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian12-x86_64-${MONGO_TOOLS_VERSION}.deb" ;; \
        arm64|aarch64) tools_url="https://fastdl.mongodb.org/tools/db/mongodb-database-tools-ubuntu2204-arm64-${MONGO_TOOLS_VERSION}.deb" ;; \
        *) echo "Unsupported architecture: ${TARGETARCH:-$(uname -m)}" >&2; exit 1 ;; \
    esac \
    && curl -fsSL "$tools_url" -o /tmp/mongodb-tools.deb \
    && dpkg-deb -x /tmp/mongodb-tools.deb /tmp/mongodb-tools \
    && install -m 0755 /tmp/mongodb-tools/usr/bin/mongodump /usr/local/bin/mongodump \
    && install -m 0755 /tmp/mongodb-tools/usr/bin/mongorestore /usr/local/bin/mongorestore \
    && rm -rf /tmp/mongodb-tools.deb /tmp/mongodb-tools

# ============= RUNTIME STAGE =============
FROM python:3.12-slim-bookworm AS runtime

WORKDIR /wbb

ENV PYTHONUNBUFFERED=1
ENV HOME=/home/appuser
ENV XDG_CACHE_HOME=/tmp/.cache

RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates iputils-ping gosu zip \
    libgssapi-krb5-2 libkrb5-3 libk5crypto3 libcom-err2 libkrb5support0 libkeyutils1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /wbb/.venv /wbb/.venv
COPY --from=build /usr/local/bin/mongodump /usr/local/bin/mongodump
COPY --from=build /usr/local/bin/mongorestore /usr/local/bin/mongorestore
COPY . .
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod 755 /usr/local/bin/docker-entrypoint.sh \
    && mongodump --version \
    && mongorestore --version

RUN useradd --create-home --uid 1000 --shell /usr/sbin/nologin appuser \
    && mkdir -p /data /wbb/sessions \
    && chown -R appuser:appuser /data /wbb/sessions \
    && if [ -f /wbb/config.env ]; then chown appuser:appuser /wbb/config.env; fi

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
