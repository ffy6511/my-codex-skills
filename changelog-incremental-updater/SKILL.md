---
name: changelog-incremental-updater
description: Update changelog-style Markdown files with incremental run-based records in Simplified Chinese by default. Use when users ask to append/update progress logs (for example `specs/changelog.md`, 变更日志, 增量日志, 运行记录), especially when the update must compare against recent commit messages and file diffs instead of rewriting historical entries.
---

# Incremental Changelog Updater

## Goal
Produce concise, append-only changelog records that are easy to scan by date and by run.

## Workflow

### 1. Confirm target and date
- Resolve target document path from user input (default: `specs/changelog.md`).
- Read existing content and check whether today's date heading exists in `## YYYY-MM-DD` format.
- If today is a new day for the document, create a new date heading before appending a run record.

### 2. Gather evidence from Git and workspace
- Read the latest entries in the target document to avoid duplication.
- Review recent commit context:
  - `git log --oneline -n 5`
  - `git show --name-only --pretty=medium <commit>` when details are needed
- Review current modifications relevant to the run:
  - `git diff --stat`
  - `git diff --cached --stat`
  - File-level diff for key modules
- Use these sources as the basis of the new run block; do not infer unsupported changes.

### 3. Append incrementally (never mix with old records)
- Append one new run block under today's date heading.
- Always prepend a Markdown separator:
  - `---`
- Then write concise bullets for this run only.
- Do not rewrite previous run blocks or merge this run into old bullets.

### 4. Keep readability high
- Keep the entry short; prefer concrete bullets with changed scope and paths.
- Use a small subheading inside the run block only if the run has many independent parts.
- Write entries in Simplified Chinese unless the user explicitly asks for another language.
- Include architecture notes only when needed:
  - Data flow/control flow changes
  - Minimal pseudocode-level explanation for non-obvious behavior

## Output Template
Use this structure when appending:

```md
## YYYY-MM-DD

---
### <可选：本次运行标题>
- 变更 1（做了什么 + 在哪里）
- 变更 2（做了什么 + 在哪里）
- 变更 3（影响或行为变化）
```

## Guardrails
- Do not fabricate changes that are not visible in commit/diff evidence.
- Do not produce long historical summaries when user asked for incremental logging.
- Do not remove existing sections unless user explicitly asks for cleanup/refactor.
- Keep wording concise and factual; avoid noisy prose.

## Quick Checklist
- Date heading for today exists or is created.
- New run is appended with `---` separator.
- Content reflects only this run (incremental).
- Statements are supported by recent commits/diffs.
