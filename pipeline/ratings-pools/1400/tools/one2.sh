#!/bin/sh
p=$1
cd "$HOME/Documents/w1400"
ok=$(python3 -c "import json,sys
try: d=json.load(open('checks/$p.json'))
except Exception: print('no'); sys.exit()
print('yes' if d.get('recipeClean') and not d.get('invalidInputs') and not d.get('oracleMismatches') and not d.get('bruteMismatches') and not d.get('extraInvalid') else 'no')")
if [ "$ok" != yes ]; then
  sleep 3
  r=$(timeout 900 python3 build.py "$p" --check-only 2>&1 | tail -1)
  echo "CHECK $r" >> check2.log
  case "$r" in "$p CLEAN"*) ;; *) echo "SKIP $p not clean" >> check2.log; exit 0;; esac
fi
timeout 300 python3 bundle.py "$p" > "gen_bundle_$p.log" 2>&1 || { echo "SKIP $p bundle failed" >> check2.log; exit 0; }
python3 gen_run.py "$p"
