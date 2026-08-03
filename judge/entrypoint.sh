#!/bin/bash
set -e

# isolate v1 --cg needs cgroup v1 controllers (memory + cpuset). If they are
# not available (e.g. cgroup v2-only hosts without v1 mounts), fall back to
# rlimit-only sandboxing.
if [ "${JUDGE_SANDBOX:-isolate}" = "isolate" ] && [ ! -d /sys/fs/cgroup/memory ]; then
  echo "cgroup v1 memory controller unavailable; falling back to JUDGE_SANDBOX=isolate-nocg"
  export JUDGE_SANDBOX=isolate-nocg
fi

# isolate's box-tree walk requires a uniform st_dev, which overlayfs (the
# container rootfs) does not guarantee — put the box root on a tmpfs.
if ! mountpoint -q /var/local/lib/isolate 2>/dev/null; then
  mount -t tmpfs -o size=1g,mode=700 tmpfs /var/local/lib/isolate 2>/dev/null || true
fi

# Some hosts co-mount cpu,cpuacct; isolate expects a plain cpuacct path.
if [ ! -e /sys/fs/cgroup/cpuacct ] && [ -d /sys/fs/cgroup/cpu,cpuacct ]; then
  ln -s cpu,cpuacct /sys/fs/cgroup/cpuacct 2>/dev/null || true
fi

mkdir -p "${CACHE_DIR:-/data/cache}" "${PROBLEMS_DIR:-/data/problems}"

# Keep the compile cache and scratch space in RAM (box dirs already are).
if ! mountpoint -q "${CACHE_DIR:-/data/cache}" 2>/dev/null; then
  mount -t tmpfs -o size=2g tmpfs "${CACHE_DIR:-/data/cache}" 2>/dev/null || true
fi
if ! mountpoint -q /tmp 2>/dev/null; then
  mount -t tmpfs -o size=1g tmpfs /tmp 2>/dev/null || true
fi

# Optional: sync problems from Supabase Storage on boot if creds are present.
if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_SERVICE_ROLE_KEY" ]; then
  echo "syncing problems from Supabase..."
  npx tsx scripts/sync-problems.ts || echo "problem sync failed (continuing with local problems)"
fi

# Warm the compiler and Python so first runs are fast.
(
  cd /tmp
  printf '#include <bits/stdc++.h>\nint main(){return 0;}\n' > warm.cpp
  g++ -O1 -g -fsanitize=address,undefined -std=c++20 -I /opt/pch/debug -o /dev/null warm.cpp || true
  g++ -O2 -std=c++20 -I /opt/pch/submit -o /dev/null warm.cpp || true
  python3 -c 'pass' || true
) &

exec node dist/server.js
