#!/usr/bin/env bash
# End-to-end smoke test: create event -> check in -> start race -> submit -> finish.
# Exercises the /api routes against a running deployment (or local `pnpm dev`).
#
# Usage:
#   ./scripts/smoke.sh                              # against http://localhost:3000
#   BASE_URL=https://your-app.vercel.app ./scripts/smoke.sh
#   PROBLEM_ID=2024A SOURCE_FILE=sol.py ./scripts/smoke.sh
#
# Defaults submit an A+B Python solution for problems/dev/aplusb, so run
# `pnpm seed --only dev/aplusb` once first (the row must exist in Supabase and
# the package must be on the judge).
set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:3000}
PROBLEM_ID=${PROBLEM_ID:-dev/aplusb}
SOURCE_FILE=${SOURCE_FILE:-}
command -v jq >/dev/null || { echo "jq is required"; exit 1; }

if [ -n "$SOURCE_FILE" ]; then
  SOURCE=$(cat "$SOURCE_FILE")
else
  SOURCE='t=int(input())
for _ in range(t):
    a,b=map(int,input().split())
    print(a+b)'
fi

say() { printf '\033[36m==>\033[0m %s\n' "$1"; }
die() { printf '\033[31mFAIL\033[0m %s\n' "$1"; exit 1; }

say "creating event at $BASE_URL"
EV=$(curl -fsS "$BASE_URL/api/events" -H 'content-type: application/json' \
  -d '{"name":"smoke test"}')
EVENT_ID=$(echo "$EV" | jq -r .id)
SECRET=$(echo "$EV" | jq -r .secret)
[ "$EVENT_ID" != null ] || die "event creation: $EV"
COOKIE="cfr_$(echo "$EVENT_ID" | tr -d -)=$SECRET"
echo "    event $EVENT_ID"

say "checking in contestant on station1"
C1=$(curl -fsS "$BASE_URL/api/checkin" -H 'content-type: application/json' -b "$COOKIE" \
  -d "{\"eventId\":\"$EVENT_ID\",\"station\":\"station1\",\"name\":\"Smoke Bot\"}")
CONTESTANT_ID=$(echo "$C1" | jq -r .contestant.id)
[ "$CONTESTANT_ID" != null ] || die "checkin: $C1"

say "starting race on problem $PROBLEM_ID"
RACE=$(curl -fsS "$BASE_URL/api/race/start" -H 'content-type: application/json' -b "$COOKIE" \
  -d "{\"eventId\":\"$EVENT_ID\",\"problemId\":\"$PROBLEM_ID\"}")
RACE_ID=$(echo "$RACE" | jq -r .race.id)
[ "$RACE_ID" != null ] || die "race start: $RACE"

say "submitting solution"
SUB=$(jq -n --arg e "$EVENT_ID" --arg r "$RACE_ID" --arg c "$CONTESTANT_ID" --arg s "$SOURCE" \
  '{eventId:$e, raceId:$r, contestantId:$c, lang:"py", source:$s}' |
  curl -fsS "$BASE_URL/api/submit" -H 'content-type: application/json' -b "$COOKIE" -d @-)
VERDICT=$(echo "$SUB" | jq -r .verdict)
echo "    verdict: $VERDICT ($(echo "$SUB" | jq -r '"\(.passedCount)/\(.totalCount) tests"'))"

say "finishing race"
curl -fsS "$BASE_URL/api/race/finish" -H 'content-type: application/json' -b "$COOKIE" \
  -d "{\"eventId\":\"$EVENT_ID\"}" > /dev/null

[ "$VERDICT" = AC ] || die "expected AC, got $VERDICT: $SUB"
printf '\033[32mPASS\033[0m smoke test OK (event %s)\n' "$EVENT_ID"
