---
name: intern-daily-report
description: Incrementally update internship daily reports in Markdown using user-specified source documents (for example, updating byteDance-landing/日报.md). Use when the user asks to write/append/refresh 日报, 实习日报, or daily progress logs with concise factual Chinese wording, clear outcomes, issues, and next improvements, while keeping the entry short (at most 5 bullets, optional one-line summary).
---

# Intern Daily Report

## Goal

Produce concise, factual daily report updates in Chinese and append them incrementally to the target Markdown file.

## Workflow

1. Confirm the target report file and source documents from the user request.
2. Read the current report file first to preserve structure and avoid rewriting past entries.
3. Read only the specified source documents and extract facts:
- Completed work and concrete outputs.
- Problems or risks encountered.
- Planned improvements or next actions.
4. Convert facts into a short markdown entry:
- Optional 1-line summary.
- Total list items <= 5.
- Each bullet should include clear action/result; when relevant, include issue + improvement direction in the same bullet.
5. Append or update only the intended date section incrementally. Do not alter unrelated historical content.
6. If key facts are missing, ask for the minimum missing details before writing.

## Writing Rules

- Use scientific, concise, factual language.
- Prefer concrete verbs and outcomes over vague statements.
- Avoid subjective filler and repetitive wording.
- Keep each bullet focused on one fact cluster (work, issue, or improvement).

## Bullet Patterns

Use compact templates like:

- `完成：<任务/学习内容>，产出：<可验证结果>。`
- `问题：<具体问题>，影响：<范围/后果>，改进：<下一步措施>。`
- `推进：<今日动作>，结论：<当前状态>，下一步：<明确动作>。`

## Output Contract

When writing the daily report content:

- Return Markdown only.
- Keep entries short.
- Use no more than 5 bullets total (summary line optional).
