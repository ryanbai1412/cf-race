#!/bin/bash
set -e

SANDBOX="${JUDGE_SANDBOX:-isolate}"
case "$SANDBOX" in
  isolate)
    if [ ! -d /sys/fs/cgroup/memory ]; then
      echo "error: JUDGE_SANDBOX=isolate requires the cgroup v1 memory controller; refusing to start" >&2
      exit 1
    fi
    ;;
  none|isolate-nocg)
    if [ "${ALLOW_UNSAFE_SANDBOX:-}" != "1" ]; then
      echo "error: JUDGE_SANDBOX=$SANDBOX is unsafe; set ALLOW_UNSAFE_SANDBOX=1 for an explicit opt-in" >&2
      exit 1
    fi
    ;;
  *)
    echo "error: unsupported JUDGE_SANDBOX=$SANDBOX" >&2
    exit 1
    ;;
esac

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
  mount -t tmpfs -o size=8g tmpfs "${CACHE_DIR:-/data/cache}" 2>/dev/null || true
fi
if ! mountpoint -q /tmp 2>/dev/null; then
  mount -t tmpfs -o size=1g tmpfs /tmp 2>/dev/null || true
fi

# Problem sync happens inside the server (immediately on boot, then every
# PROBLEM_SYNC_INTERVAL_SEC) so startup isn't blocked and the health check
# passes while existing packages on the volume keep serving.

# Warm the compiler and Python so first runs are fast.
(
  cd /tmp
  printf '#include <bits/stdc++.h>\nint main(){return 0;}\n' > warm.cpp
  g++ -O1 -g -fsanitize=address,undefined -std=c++20 -I /opt/pch/debug -o /dev/null warm.cpp || true
  g++ -O2 -std=c++20 -I /opt/pch/submit -o /dev/null warm.cpp || true
  python3 -c 'pass' || true
) &

exec node dist/server.js
