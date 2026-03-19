---
name: capture-dev-insight
description: Capture and append concise Chinese development insight notes from the current agent conversation, code explanation, modification rationale, debugging takeaway, or syntax clarification. Use when the user wants to 记一下、整理成笔记、保存启发、记录新知识/新发现, especially for explanations like why a change was made, how a mechanism works, or what a piece of syntax means.
---

# Capture Dev Insight

## Goal

Turn a worthwhile takeaway from the current conversation into a compact Markdown note that is **self-contained and understandable even when read alone later**.

## Default Target

- Default notes directory: `/Users/bytedance/Documents/Personal-record/MyTypst/Dev/daily-dev-notes`
- Default file rule: append to `YYYY-MM-DD.md` for today.
- If today's file does not exist, create it first.
- If the user explicitly names a Markdown file, append there instead of the default daily file.

## Workflow

1. Identify the exact insight worth keeping from the current discussion or code context.
2. Distill it before writing:
- Keep the new knowledge, decision rationale, mechanism, pitfall, or mental model.
- Drop conversational filler, repeated chatter, and implementation noise.
3. Add the missing background needed for standalone reading:
- State the business/code context first when the note would otherwise be hard to understand alone.
- Include the minimum necessary setup: where the code lives, what problem was being solved, and what triggers the mechanism.
4. Resolve the target file:
- If the user names a file, use that file.
- Otherwise use today's file in the default notes directory.
5. Read the target file first when it already exists:
- Preserve nearby tone and heading style.
- Avoid repeating an insight that is already recorded.
6. Decide whether to append or revise:
- If this is a new insight, append it.
- If you just wrote a note for the same insight in the current conversation and it is incomplete or poorly structured, **revise/replace that fresh section instead of appending a second competing section**.
- Prefer one canonical section per insight in the same daily file.
7. Draft a compact note section in Simplified Chinese.
8. Append with `scripts/append_note.py` when adding a new section; use direct editing when consolidating or replacing a just-written section.

## Preferred Note Shape

Use this structure unless the target file already shows a stronger local style:

~~~md
## <标题>

### 背景
<2-4 句。先交代代码/机制所在位置、触发条件、要解决的问题，让笔记脱离当前对话也能读懂>

### 核心结论
<1-3 句，先说本质>

### 为什么
- <原因 / 机制 / 设计取舍>
- <必要时补一个反例或误区>

### 例子
~~~text
<尽量短的小例子>
~~~

### 边界
- <可选：适用范围、限制、易错点>
~~~

Guidelines:

- Put **背景** before **核心结论** when context is needed.
- Keep the title concrete and short; prefer the knowledge point itself.
- Use short paragraphs and short bullet lists.
- Include a simple example when it improves understanding.
- Omit `### 边界` when there is no meaningful caveat.
- The note must still make sense to someone who only reads the note file days later.

## Writing Rules

- Write in concise, logical Simplified Chinese.
- When needed, start with context/background before the conclusion.
- Prefer one insight per section.
- Keep examples minimal but specific.
- Favor durable explanations over transient task chatter.
- If the note would confuse a future reader, add the missing background instead of assuming chat context.
- If there is no real takeaway, do not pad the note.

## Append Rules

- For the default daily file, keep one file per date.
- When appending a truly new section to a non-empty file, separate entries with `---`.
- Do not create two adjacent sections for the same insight just because the first draft was weak; replace or merge the newer one.
- Do not rewrite unrelated historical notes unless the user explicitly asks.
- If multiple same-day default files already exist, stop and ask the user which file should remain the canonical daily note.

## Script

Use `scripts/append_note.py` for the default append flow.

Examples:

```bash
python3 /Users/bytedance/.codex/skills/capture-dev-insight/scripts/append_note.py \
  --title "双令牌机制鉴权" \
  --body-file /tmp/insight.md
```

```bash
python3 /Users/bytedance/.codex/skills/capture-dev-insight/scripts/append_note.py \
  --target-file /path/to/custom.md \
  --title "为什么这里要做幂等处理" \
  --body-file /tmp/insight.md
```

Use direct editing instead of the append script when the task is to consolidate, reorder, or replace a just-added section.

## Output Contract

- Produce Markdown only for the note body you plan to write.
- Keep the result compact and readable.
- Match the existing target file style when the user points to a specific file.
- Ensure the note can be understood without reopening the original conversation.
