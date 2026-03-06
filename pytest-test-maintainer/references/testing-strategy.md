<!-- Purpose: Define repeatable pytest test-design strategies by feature type, with evidence-driven rules for coverage updates. -->

# Testing Strategy Reference

## Evidence priority for coverage updates
When user asks to update coverage scope:
1. Read recent commit intent (`git log --oneline -n 5`).
2. Read staged and unstaged file diffs (`git diff --cached`, `git diff`).
3. Read changelog context (`changelog.md` or `specs/changelog.md`) if available.

If these sources conflict, prefer actual diffs over message wording.

## Test logic by feature type
- Pure logic/helpers:
  - Focus: branch/edge conditions and invalid inputs.
  - Style: parameterized unit tests.
- API handlers:
  - Focus: status code, schema mapping, validation, and error propagation.
  - Style: request/response tests with boundary mocks.
- Adapters/clients:
  - Focus: retry/timeout/error translation and payload correctness.
  - Style: mock upstream calls; assert call arguments and fallback behavior.
- Middleware/hooks:
  - Focus: order, side effects, and failure handling.
  - Style: integration-like tests around lifecycle execution.
- Bugfix/regression:
  - Focus: one failing scenario fixed by change + one nearby guard case.
  - Style: minimal repro test plus stability assertion.

## Plugin usage baseline
- Coverage: `pytest --cov=<target> --cov-report=html`
- Parallel: `pytest -n auto` (or `-n 4`)
- HTML report: `pytest --html=report.html --self-contained-html`
