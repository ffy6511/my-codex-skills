---
name: pytest-test-maintainer
description: Build and maintain pytest+mock tests with pytest-cov, pytest-xdist, and pytest-html. Use when users ask to generate test scripts, add regression tests, update test coverage scope, or run quick/cov/report/changed test modes. For requests like “更新测试脚本的覆盖范围”, inspect recent git messages, staged/unstaged diffs, and changelog.md (if present) before deciding what to test.
---

# Pytest Test Maintainer

## Goal
Generate or update Python tests with `pytest + mock` and keep execution repeatable via one shell runner.

## Workflow

### 1. Collect change evidence first
Use this order when planning or updating coverage:
- `git log --oneline -n 5`
- `git diff --cached --name-only` and `git diff --name-only`
- `changelog.md` or `specs/changelog.md` when present

For the explicit request `更新测试脚本的覆盖范围`, always gather all three evidence sources before editing tests.

### 2. Map change scope to test types
Read [references/testing-strategy.md](references/testing-strategy.md) and pick targeted test logic:
- Unit tests for pure/utility logic
- Integration tests for component boundaries (adapter/client/tool wiring)
- API tests for request/response and error mapping
- Regression tests for bugfix paths and previous failures

### 3. Implement or update tests
- Prefer deterministic assertions and explicit fixtures.
- Use `unittest.mock` or `pytest-mock` style patching for I/O and network boundaries.
- Keep test setup local to module-level fixtures unless sharing is clearly beneficial.

### 4. Run standardized script modes
Use [scripts/run_tests.sh](scripts/run_tests.sh):
- `./scripts/run_tests.sh quick` for fast smoke runs
- `./scripts/run_tests.sh cov` for coverage + `htmlcov/`
- `./scripts/run_tests.sh report` for `pytest-html` report
- `./scripts/run_tests.sh changed` for change-focused runs

Pass extra pytest args after mode, for example:
- `./scripts/run_tests.sh cov -k sandbox -q`

## Guardrails
- Do not expand to full-suite rewrites when the request is scope-limited.
- Do not claim coverage increases without running or clearly stating it was not executed.
- Keep model-facing summaries concise; avoid dumping full raw logs.
