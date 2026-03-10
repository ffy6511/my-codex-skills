---
name: intern-daily-report
description: Incrementally update internship daily reports or same-day progress sections in Markdown using user-specified source documents (for example, updating byteDance-landing/日报.md or a 今日成果 section). Use when the user asks to write/append/refresh 日报, 实习日报, or daily progress logs in concise Chinese and expects the wording, format, and section structure to stay close to nearby examples.
---

# Intern Daily Report

## Goal

Produce concise, factual daily report updates in Chinese and append them incrementally to the target Markdown file or date section, while staying close to the surrounding note style.

## Workflow

1. Confirm the target report file and source documents from the user request.
2. Read the current report file or target section first to preserve structure, tone, and formatting before writing.
3. Read only the specified source documents and extract facts:
- Completed work and concrete outputs.
- Problems or risks encountered.
- Planned improvements or next actions.
4. Infer the expected format from nearby entries and any explicit user example.
5. Convert facts into a short markdown entry:
- If the user provides a concrete example, follow that structure first.
- Otherwise, prefer a sectioned format with `####` headings that summarize the day, then bullets that expand on each part.
- Typical headings are `#### 流程推进情况`、`#### 知识整理`、`#### 其他进展`, but adapt to the target file when needed.
- Keep the whole entry compact. Do not pad with filler; use only the bullets needed to cover the day clearly.
- Each bullet should describe a concrete action, understanding, issue, or next step, not just a label.
6. Append or update only the intended date section incrementally. Do not alter unrelated historical content.
7. If key facts are missing, ask for the minimum missing details before writing.

## Writing Rules

- Use concise, factual Chinese, but keep the tone close to real daily notes rather than generic templates.
- Mirror nearby wording before inventing a new style. Match the local voice of the target document.
- Prefer natural progression language such as `先`、`然后`、`最后` when summarizing a day's flow if that matches the example.
- Avoid mechanical labels like `完成：`、`推进：`、`问题：` unless the target file already uses that style or the user explicitly asks for it.
- Prefer concrete actions, outputs, and current understanding over vague summary words.
- Keep each bullet focused on one fact cluster, but allow one bullet to contain action + result or issue + follow-up when that reads more naturally.

## Preferred Format

When there is no stronger existing local style, prefer:

```md
#### 流程推进情况
<一句总起，概括今天主要推进方向>
- <先做了什么，结合什么材料或代码，得到什么进展>;
- <然后做了什么，重点看了什么内容，理清了什么关系>;
- <如果有协助排障/任务推进，写清楚当前结论>;

#### 知识整理
- <整理了哪些知识点，理解加深到什么程度>;
- <补了哪些基础知识，和当前任务有什么关系>;

#### 其他进展
- <周会、沟通、方向判断或整体认识上的补充进展>
```

Notes:

- Use `####` headings as the top-level structure inside the day section when following this preferred format.
- Start each subsection with a brief summary sentence when it helps the reading flow.
- The writing should feel like a concise personal work log, not a status dashboard or ticket system.
- Stay compact; usually 2-3 subsections are enough.

## Output Contract

When writing the daily report content:

- Return Markdown only.
- Keep entries short and incremental.
- Preserve surrounding headings and historical content.
- Prioritize matching the user's example and the target file's local style over any default template in this skill.
