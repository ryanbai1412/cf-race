.PHONY: setup dev lint typecheck build check seed judge-dev judge-test judge-docker judge-deploy smoke

setup: ## check prerequisites, create .env.local, install deps
	./scripts/setup.sh

dev: ## run the web app (http://localhost:3000)
	pnpm dev

lint:
	pnpm lint

typecheck:
	pnpm typecheck

build:
	pnpm build

check: ## lint + typecheck + build (run before pushing)
	pnpm lint && pnpm typecheck && pnpm build

seed: ## upload problems/ packages to Supabase Storage + upsert problems table
	pnpm seed

judge-dev: ## local judge, no sandbox (unsafe, dev only) on http://localhost:8080
	cd judge && JUDGE_TOKEN=dev JUDGE_SANDBOX=none PROBLEMS_DIR=../problems pnpm run dev

judge-test:
	cd judge && pnpm test

judge-docker: ## local judge in Docker with the real isolate sandbox
	rm -rf judge/problems-dev && cp -R problems/dev judge/problems-dev
	docker compose up --build judge

judge-deploy: ## deploy the judge to Fly.io (app cf-race-judge)
	rm -rf judge/problems-dev && cp -R problems/dev judge/problems-dev
	cd judge && fly deploy -a cf-race-judge

smoke: ## end-to-end smoke test (BASE_URL=... PROBLEM_ID=...)
	./scripts/smoke.sh
