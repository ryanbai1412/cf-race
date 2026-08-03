#!/bin/bash
set -e

# isolate v2 needs a delegated cgroup v2 subtree; normally isolate-cg-keeper
# (systemd) provides it. Without systemd, set it up by hand: move all processes
# out of the cgroup root, enable controllers, and point /run/isolate/cgroup at
# a dedicated subtree.
if [ "${JUDGE_SANDBOX:-isolate}" = "isolate" ] && ! grep -q memory /sys/fs/cgroup/cgroup.controllers 2>/dev/null; then
  echo "cgroup v2 controllers unavailable; falling back to JUDGE_SANDBOX=isolate-nocg"
  export JUDGE_SANDBOX=isolate-nocg
fi

if [ -f /sys/fs/cgroup/cgroup.controllers ]; then
  mkdir -p /sys/fs/cgroup/init /sys/fs/cgroup/isolate /run/isolate
  for pid in $(cat /sys/fs/cgroup/cgroup.procs 2>/dev/null); do
    echo "$pid" > /sys/fs/cgroup/init/cgroup.procs 2>/dev/null || true
  done
  for ctrl in cpuset memory cpu; do
    echo "+$ctrl" > /sys/fs/cgroup/cgroup.subtree_control 2>/dev/null || true
    echo "+$ctrl" > /sys/fs/cgroup/isolate/cgroup.subtree_control 2>/dev/null || true
  done
  echo /sys/fs/cgroup/isolate > /run/isolate/cgroup
fi

mkdir -p "${CACHE_DIR:-/data/cache}" "${PROBLEMS_DIR:-/data/problems}"

# Optional: sync problems from Supabase Storage on boot if creds are present.
if [ -n "$SUPABASE_URL" ] && [ -n "$SUPABASE_SERVICE_ROLE_KEY" ]; then
  echo "syncing problems from Supabase..."
  npx tsx scripts/sync-problems.ts || echo "problem sync failed (continuing with local problems)"
fi

# Pre-mount isolate's tmpfs so concurrent first-inits don't race.
isolate -b 0 --init >/dev/null 2>&1 && isolate -b 0 --cleanup >/dev/null 2>&1 || true

# Warm the compiler and Python so first runs are fast.
(
  cd /tmp
  echo 'int main(){return 0;}' > warm.cpp
  g++ -O1 -g -fsanitize=address,undefined -std=c++20 -o /dev/null warm.cpp || true
  g++ -O2 -std=c++20 -o /dev/null warm.cpp || true
  python3 -c 'pass' || true
) &

exec node dist/server.js
