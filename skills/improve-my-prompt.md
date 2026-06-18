---
name: improve-my-prompt
description: Review and rewrite a draft prompt applying Anthropic's prompt engineering best practices for Claude's latest models. Use when about to send a complex or important request and want to make sure it's well-structured before sending it.
---

# Improve My Prompt

Takes a draft prompt and rewrites it to be clearer, more specific, and more likely to produce the right result first time.

## How to use

Give me your draft prompt (rough is fine) and I'll apply the principles below to rewrite it. Then you send the improved version as your actual request.

## The golden rule test

Before sending any prompt, ask: "If I showed this to a colleague with minimal context on the task, could they follow it?" If they'd be confused, I will be too. If it would leave room for interpretation, I'll interpret it wrong.

## Core principles (Claude-specific)

### 1. Actions over suggestions

The single most impactful change. If you want something done, say so directly.

| Weak (produces suggestions) | Strong (produces action) |
|---|---|
| "Can you suggest some changes to X?" | "Change X to do Y." |
| "What would you do to improve this?" | "Improve this function by doing X." |
| "How should I handle this?" | "Handle this by doing X." |

Use direct action verbs: Write, Analyze, Generate, Create, Change, Fix, Remove, Add.

### 2. Explain the why

Don't just give a rule — give the reason. Claude generalizes from reasoning and makes better decisions on related choices.

| Weak | Strong |
|---|---|
| "NEVER use bullet points" | "Write in flowing prose because this output gets read aloud by a text-to-speech engine that can't handle lists." |
| "Keep responses short" | "Keep responses under 3 sentences because they appear in a mobile notification." |

### 3. Be specific about output quality

If you want above-and-beyond output, ask for it explicitly. Don't assume I'll infer it.

| Weak | Strong |
|---|---|
| "Create an analytics dashboard" | "Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation." |

### 4. Format: tell me what TO do

| Weak | Strong |
|---|---|
| "Don't use markdown" | "Write in flowing prose paragraphs without headers or bullets." |
| "Don't be verbose" | "Respond in 2-3 sentences maximum." |

### 5. XML tags for complex prompts

When a prompt mixes instructions, context, examples, and variable inputs, wrap each type in XML tags to prevent misinterpretation.

```xml
<instructions>
Analyze the customer feedback and identify the top 3 issues.
</instructions>

<context>
This feedback is from enterprise customers, not consumers. Tone matters.
</context>

<feedback>
{{CUSTOMER_FEEDBACK}}
</feedback>
```

### 6. Long documents: top placement

When including documents or large amounts of data, put them at the TOP of the prompt, above your query. Query at the end can improve response quality by up to 30%.

```
[Documents here — above everything else]

[Instructions]

[Your query at the bottom]
```

### 7. Examples (3-5, with tags)

For specific formats or tones, show rather than tell. Wrap examples in `<example>` tags.

```xml
<examples>
<example>
Input: Q3 revenue fell 12% YoY
Output: Revenue declined 12% year-over-year in Q3.
</example>
<example>
Input: Customer churn increased significantly in enterprise segment
Output: Enterprise churn increased materially, warranting investigation.
</example>
</examples>

Now process this: {{INPUT}}
```

### 8. Permission to express uncertainty

For factual tasks: "If you're not certain, say so rather than guessing."

### 9. Parallel tool calls

When asking me to do multiple independent things, say so: "Do these in parallel, not sequentially."

## What I'll do

1. Read the draft
2. Apply the golden rule test — would a colleague be confused?
3. Flag what's vague, question-form, or under-specified
4. Rewrite applying the principles above
5. Note what changed and why
6. Present the improved version ready to use

## Examples

**Draft:** "Can you help me think about the auth system?"

**Issues:** Question form (produces discussion, not analysis). No scope. No output format.

**Improved:**
```
Analyze the authentication system in this codebase. Identify security gaps, missing edge
cases, and routes that should be protected but aren't. Focus on session management and
token handling. Order findings by severity. If any finding requires more information to
assess accurately, say so rather than speculating.
```

---

**Draft:** "Make the dashboard better"

**Issues:** Vague scope, no quality bar, no output format.

**Improved:**
```
Improve the dashboard. Add as many relevant features and interactions as possible — go
beyond the basics. Include real-time data updates, filtering, sorting, and drill-down
views. Make it production-ready, not a prototype.
```
