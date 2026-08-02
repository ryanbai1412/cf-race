# Code vs Racing (cf-race)

Head-to-head competitive programming races for live events: two contestants solve the
same Codeforces problem side by side while racing a replay of tourist solving it.

- `src/` — Next.js app (stations, monitors, admin) — deployed on Vercel
- `judge/` — sandboxed code execution service (Fly.io)
- `pipeline/` — problem scraping / test generation pipeline
- `problems/` — problem packages (see docs/JUDGE_API.md for format)
- `docs/` — PRD, architecture, flow PRDs, contracts

## Dev
```
npm install
npm run dev     # needs env vars, see .env.example
npm run lint && npx tsc --noEmit && npm run build
```
