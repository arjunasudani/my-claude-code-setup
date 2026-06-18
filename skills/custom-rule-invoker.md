---
name: custom-rule-invoker
description: Add ECC rules to the current project. Asks which rule sets are relevant and sets them up under .claude/rules/ecc/. Use at the start of any new project before implementation begins.
---

# Custom Rule Invoker

Sets up project-level ECC rules for the current working directory.

## Available Rule Sets

Rules live in `~/.claude/rules-archive/`. Currently available:

- **python** — coding style, testing, security, hooks, patterns, performance, FastAPI
- **web** — coding style, testing, security, hooks, patterns, design quality

Already active globally (no need to add):
- **common** — always loaded globally
- **typescript** — always loaded globally

## Workflow

### Step 1: Identify what this project needs

Ask the user:

> "What's the primary stack for this project? Looking at the available rule sets:
> - **python** — add if this project has Python code, a FastAPI backend, scripts, or data pipelines
> - **web** — add if this project has significant frontend work beyond what TypeScript rules cover (CSS systems, accessibility, design quality)
>
> Which apply, and why? (Skip any that don't fit — rules load on every session and consume context.)"

Do not add rules speculatively. Only add what the user confirms is relevant.

### Step 2: Check what's already set up

```bash
ls .claude/rules/ecc/ 2>/dev/null || echo "no project rules yet"
```

### Step 3: Add confirmed rule sets

For each confirmed rule set:

```bash
mkdir -p .claude/rules/ecc
cp -r ~/.claude/rules-archive/<ruleset> .claude/rules/ecc/
```

### Step 4: Confirm

List what was added and what each set covers:

```
Added to .claude/rules/ecc/:
  python/  — 7 files: coding-style, testing, security, hooks, patterns, performance, fastapi
  web/     — 6 files: coding-style, testing, security, hooks, patterns, design-quality
```

Remind the user: these rules now load automatically in every session inside this project directory. To remove a rule set later, delete its folder from `.claude/rules/ecc/`.

## Anti-patterns

- Do not add rules "just in case" — every rule set adds context overhead
- Do not add python rules to a TypeScript-only project
- Do not add web rules if the project's frontend is already covered by global TypeScript rules
