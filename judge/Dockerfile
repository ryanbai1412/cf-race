# Judge service: Node.js + g++ + python3 + isolate sandbox.
FROM ubuntu:24.04 AS isolate-build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git libcap-dev libsystemd-dev pkg-config ca-certificates \
    && rm -rf /var/lib/apt/lists/*
# v1.10.1: classic isolate (cgroup v1 / rlimits). v2.0's mountpoint scan
# breaks on Fly.io's kernel, and Fly machines only expose cgroup v1 anyway.
RUN git clone --depth 1 --branch v1.10.1 https://github.com/ioi/isolate.git /isolate \
    && make -C /isolate isolate

FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ python3 libcap2 libsystemd0 ca-certificates curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY --from=isolate-build /isolate/isolate /usr/local/bin/isolate
COPY --from=isolate-build /isolate/default.cf /usr/local/etc/isolate
RUN chmod u+s /usr/local/bin/isolate \
    && mkdir -p /var/local/lib/isolate /data/problems

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY tsconfig.json ./
COPY src ./src
COPY scripts ./scripts
RUN npm run build

# Dev problems baked into the image so the judge works before any sync.
COPY problems-dev /data/problems/dev

ENV PROBLEMS_DIR=/data/problems \
    CACHE_DIR=/data/cache \
    JUDGE_SANDBOX=isolate \
    PORT=8080

EXPOSE 8080
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
