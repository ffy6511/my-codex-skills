---
name: xigai-discussion-ppt-content
description: Generate and update classroom discussion slide content for Xi Jinping Thought / ideological-political courses from changing topics. Use when users ask to produce a `content.md`-style script for a 4-8 minute presentation where normal text is slide-visible content, blockquotes are per-slide speaker notes, and each slide includes at least one directly renderable Markdown image (`![alt](url)`), with a coherent narrative line, formal wording, theory + data support, and factually correct historical statements.
---

# Xigai Discussion PPT Content

Create a `content.md` that can be used directly for class discussion slides and speaking notes.
Adapt the analysis to each topic; do not assume fixed question patterns.

## Output Contract

- Write to `content.md` in the same directory as the user's plan/source file unless the user specifies another path.
- Use Markdown only.
- Keep normal paragraphs/lists as slide-visible text.
- Put speaker notes for each slide in `>` blockquotes.
- Split slides by natural subtopics.
- Use formal written style suitable for classroom reporting; avoid colloquial wording in titles and bullets.
- Include at least one image for each slide section.
- Insert images in Markdown-renderable form only: `![alt text](image-url)`.
- Do not output plain URL-only image lines like `图片URL: ...`.

Use this shape:

```markdown
# 标题页
- 课程主题
- 小组信息（可选）
> 开场讲稿……

## 第1页：问题引入
- 要点A
- 要点B
![图示说明A](https://example.com/image-a.jpg)
> 本页讲稿……

## 第2页：核心分析
- 要点A
- 要点B
![图示说明B](https://example.com/image-b.jpg)
> 本页讲稿……
```

## Workflow

1. Analyze the topic dynamically.
2. Plan the narrative and timing.
3. Draft per-slide visible text and matching speaker notes.
4. Enrich with theory, data, and facts.
5. Run quality checks before finalizing `content.md`.

## 1) Analyze Topic Dynamically

- Extract the exact discussion topic from user input or provided files.
- Determine topic type (for example: concept interpretation, historical evolution, path justification, policy effectiveness, comparative analysis).
- Derive 1-3 key analytical questions from this specific topic.
- Build one clear narrative line that answers those questions in sequence.
- Never force a fixed "two-question" structure when the topic does not require it.

For topic-specific argument patterns, read:
- `references/slide-structures.md`

## 2) Plan Timing and Slide Count

- Target speaking duration: 4-8 minutes.
- Use this default pacing:
  - 4 minutes: 4-5 content slides
  - 5-6 minutes: 5-7 content slides
  - 7-8 minutes: 7-9 content slides
- Allocate time in this order: opening context -> core argument -> evidence -> conclusion/call to discussion.
- Keep each slide to 2-4 visible bullets; place explanatory detail in blockquote notes.

## 3) Draft Slide Content

- Start from an outline first, then expand to final copy.
- Ensure each slide has both:
  - visible text (concise, projection-friendly)
  - a matching `>` speaker-note block
- Ensure each slide has at least one image using `![alt](url)` and concise, meaningful alt text.
- Keep transitions explicit between slides so the narrative is continuous.
- Use headings like `## 第N页：<子主题>` for clarity.

## 4) Integrate Theory, Data, and Facts

- Include relevant theoretical framing from the course context.
- Support key claims with data or observable outcomes where possible.
- Use historically accurate events and timelines.
- If a data point is uncertain, prefer cautious phrasing over fabricated precision.

Fact safety checklist is in:
- `references/fact-checklist.md`

## 5) Final Quality Gate

Before writing the final output, verify all items:
- The structure responds to this specific topic, not a rigid template.
- A single main line connects all slides.
- Every slide has speaker notes in blockquote format.
- Every slide has at least one Markdown image using `![alt](url)` syntax.
- Wording is formal and non-colloquial.
- Theory and evidence are both present.
- Historical statements are internally consistent and factually plausible.
- Total speaking length fits 4-8 minutes.

## References

- `references/slide-structures.md`: Topic-to-structure mapping and narrative patterns.
- `references/fact-checklist.md`: Data/history validity rules for safe writing.
