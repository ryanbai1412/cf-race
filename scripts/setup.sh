#!/usr/bin/env bash
# One-shot dev setup: checks prerequisites, creates .env.local, installs deps.
# Usage: ./scripts/setup.sh   (or: make setup)
set -euo pipefail
cd "$(dirname "$0")/.."

ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }
fail() { printf '  \033[31m✗\033[0m %s\n' "$1"; FAILED=1; }
FAILED=0

echo "Checking prerequisites..."

if command -v node >/dev/null; then
  NODE_MAJOR=$(node -v | sed 's/^v\([0-9]*\).*/\1/')
  if [ "$NODE_MAJOR" -ge 20 ]; then ok "node $(node -v)"; else fail "node >= 20 required (found $(node -v))"; fi
else
  fail "node not found — install Node.js 20+ (https://nodejs.org)"
fi

if command -v pnpm >/dev/null; then
  ok "pnpm $(pnpm -v)"
else
  warn "pnpm not found — enabling via corepack"
  corepack enable 2>/dev/null || sudo corepack enable
  # Older corepack builds fail signature checks on new pnpm releases:
  COREPACK_INTEGRITY_KEYS=0 corepack prepare pnpm@10.18.3 --activate
  ok "pnpm $(pnpm -v)"
fi

command -v docker >/dev/null && ok "docker $(docker --version | awk '{print $3}' | tr -d ,) (optional, for local judge container)" \
  || warn "docker not found (optional — only needed for 'make judge-docker')"
command -v fly >/dev/null && ok "flyctl (optional, for judge deploys)" \
  || warn "flyctl not found (optional — only needed for 'make judge-deploy')"

if [ "$FAILED" = 1 ]; then echo; echo "Fix the ✗ items above and re-run."; exit 1; fi

echo
if [ ! -f .env.local ]; then
  cp .env.example .env.local
  warn "created .env.local from .env.example — fill in the values below"
else
  ok ".env.local exists"
fi

echo
echo "Required env vars (in .env.local — see .env.example and README.md):"
cat <<'EOF'
  NEXT_PUBLIC_SUPABASE_URL       Supabase project URL (Dashboard -> Settings -> API)
  NEXT_PUBLIC_SUPABASE_ANON_KEY  Supabase anon key
  SUPABASE_SERVICE_ROLE_KEY      Supabase service-role key (server-side only)
  NEXT_PUBLIC_LIVEKIT_URL        LiveKit server wss:// URL
  LIVEKIT_API_KEY                LiveKit API key
  LIVEKIT_API_SECRET             LiveKit API secret
  JUDGE_URL                      Judge base URL (http://localhost:8080 for local judge)
  JUDGE_TOKEN                    Judge bearer token ("dev" for local judge)
EOF

MISSING=$(grep -E '^[A-Z_]+=\s*$' .env.local | cut -d= -f1 || true)
echo
if [ -n "$MISSING" ]; then
  warn "still empty in .env.local: $(echo "$MISSING" | tr '\n' ' ')"
else
  ok "all env vars in .env.local are set"
fi

echo
echo "Installing dependencies..."
pnpm install
(cd judge && pnpm install)

echo
echo "Done. Next steps:"
echo "  pnpm dev          # web app on http://localhost:3000"
echo "  make judge-dev    # local judge on http://localhost:8080 (no sandbox)"
echo "  pnpm seed         # upload problems/ to Supabase (needs service-role key)"
echo "  make smoke        # end-to-end smoke test against BASE_URL"
