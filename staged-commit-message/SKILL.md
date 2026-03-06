---
name: staged-commit-message
description: Generate git commit messages from the current staged changes only and write them to COMMIT.md using Conventional Commit structure (type, scope, description, body, optional footer). Use when the user asks to draft/update commit text based on staged files, asks for COMMIT.md generation, or requests commit messages that must follow a strict template and language style inferred from repository history.
---

<!-- Purpose: Define a deterministic workflow for drafting commit messages from staged git changes and writing COMMIT.md. -->

# Staged Commit Message

## Workflow

1. Inspect staged changes only.
- Run `git diff --cached --name-status`.
- Run `git diff --cached --stat`.
- Run `git diff --cached`.
- Do not use unstaged (`git diff`) or untracked files as evidence.

2. Stop early if nothing is staged.
- Check with `git diff --cached --quiet`.
- If no staged changes exist, return a short error and do not generate fake commit text.

3. Infer commit language from recent history.
- Run `git log -n 20 --no-merges --pretty=format:%s%n%b`.
- Prefer Chinese if recent commit subjects/bodies are mainly Chinese.
- Prefer English if recent commit subjects/bodies are mainly English.
- If mixed and no strong signal, follow the repository's most recent non-merge commit language.

4. Draft message with this structure.
- First line: `<type>(<scope>): <description>`
- Blank line.
- Body bullets (`- ...`), maximum 5 lines.
- Optional footer lines (for example `BREAKING CHANGE:` or `Refs:`) only when needed.

5. Choose fields using staged evidence.
- `type`: choose from `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `revert`.
- `scope`: choose the smallest meaningful module/component inferred from staged paths.
- `description`: one concise sentence in selected language, no trailing period.
- `body`: summarize staged behavior/code changes only; avoid file-by-file noise.
- `footer`: include only if there is clear staged evidence (breaking change, issue link, migration note).

6. Write output file.
- Default target is current working directory `COMMIT.md`.
- Overwrite file content instead of appending.
- If user explicitly requests another path/name, honor that override.
- Write plain text commit message only (no code fences, no extra explanation lines).

## Output Template

```text
<type>(<scope>): <description>

- <point 1>
- <point 2>
- <point 3>

<optional footer line 1>
<optional footer line 2>
```

## Quality Rules

- Keep body bullet count <= 5.
- Keep summary accurate and specific to staged diffs.
- Never invent changes not present in staged content.
- Keep wording concise and actionable.
