#!/bin/bash
# usage: pipeline_run.sh PID...   (generate via build.py, then sandboxed validate)
cd /home/ubuntu/repos/cf-race
for p in "$@"; do
  out=$(python3 /home/ubuntu/Documents/w1400/build.py $p)
  echo "$out"
  case "$out" in *CLEAN*) ;; *) continue;; esac
  python3 pipeline/rated_pool.py validate --rating 1400 --target 100 --workspace ~/Documents/cf-pools --cache ~/.cache/cf-race-pool \
    --id $p --all-submissions --validator devin-1400-worker --coverage ~/Documents/w1400/coverage/coverage-$p.json 2>&1 | python3 -c "
import sys,json
t=sys.stdin.read()
try:
  d=json.loads(t); print('VAL',d['id'],d['status'],'acc',d['accepted'],'inc',d['incorrect'],'exc',d['excluded'])
except Exception: print('VALERR $p',t[-300:])
"
done
