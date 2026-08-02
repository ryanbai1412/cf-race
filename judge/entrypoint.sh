#!/bin/bash
set -e

# isolate needs cgroup v2 delegation; Fly machines run with cgroup2 mounted.
if [ -f /sys/fs/cgroup/cgroup.controllers ]; then
  mkdir -p /sys/fs/cgroup/isolate 2>/dev/null || true
  echo "+cpuset +memory" > /sys/fs/cgroup/cgroup.subtree_control 2>/dev/null || true
fi

mkdir -p "${CACHE_DIR:-/data/cache}" "${PROBLEMS_DIR:-/data/problems}"

# Optional: sync problems from Supabase Storage on boot if creds are present.
if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_SERVICE_ROLE_KEY" ]; then
  echo "syncing problems from Supabase..."
  npx tsx scripts/sync-problems.ts || echo "problem sync failed (continuing with local problems)"
fi

# Warm the compiler and Python so first runs are fast.
(
  cd /tmp
  echo 'int main(){return 0;}' > warm.cpp
  g++ -O1 -g -fsanitize=address,undefined -std=c++20 -o /dev/null warm.cpp || true
  g++ -O2 -std=c++20 -o /dev/null warm.cpp || true
  python3 -c 'pass' || true
) &

exec node dist/server.js
