# my-claude-code-setup

My complete Claude Code configuration, built in one session working through the [ECC shortform and longform guides](https://github.com/affaan-m/ECC) by [@affaan-m](https://github.com/affaan-m).

**Who this is for:** solo builders and founders who ship fast with Claude Code and want a setup that compounds over time. Not for teams, not for enterprise. For someone who opens a terminal, types `claude`, and builds real things. Specifically tuned for TypeScript/Next.js/Supabase stacks but the core workflow applies to anything.

---

## Table of Contents

- [Philosophy](#philosophy)
- [What's in here](#whats-in-here)
- [Skills](#skills)
- [Agents](#agents)
- [Rules](#rules)
- [Hooks](#hooks)
- [Session Memory](#session-memory)
- [Continuous Learning v2](#continuous-learning-v2)
- [Statusline](#statusline)
- [Context Aliases](#context-aliases)
- [ExecPlan Workflow](#execplan-workflow)
- [Session Flows](#session-flows)
- [MCP Discipline](#mcp-discipline)
- [Installation](#installation)
- [Credits](#credits)

---

## Philosophy

Most Claude Code setups are configured once and forgotten. This one is designed to compound. Every session teaches it something. Every project gets the right rules. Every task gets nudged toward the right workflow.

The core ideas:

- **Skills over prompts.** Reusable workflow definitions beat one-off prompts every time. Write the prompt once, invoke it everywhere.
- **Agents for delegation.** The main context is for orchestration. Specialist work goes to specialist agents.
- **Rules for consistency.** Always-loaded guidelines mean you never have to remind Claude about coding style, testing, or security.
- **Hooks for automation.** Formatting, type checking, context memory, skill reminders — all fire automatically so you never forget.
- **Memory that persists.** Session summaries mean Claude knows where you left off every single time you open a project.

---

## What's in here

```
my-claude-code-setup/
├── skills/          # 14 global workflow skills
├── agents/          # 16 specialized subagents
├── rules/
│   └── ecc/
│       ├── common/  # 10 always-loaded rules
│       └── typescript/ # 5 TypeScript-specific rules
├── hooks/           # 11 automation hook scripts
├── contexts/        # 3 Claude mode context files
├── scripts/
│   ├── hooks/       # Session memory scripts
│   └── lib/         # Library dependencies
├── CLAUDE.md        # Global behavioral guidelines
├── settings.json    # Annotated settings template
└── mcp-tool-counts.json  # MCP server tool count cache
```

---

## Skills

Skills are the primary workflow surface. They live in `~/.claude/skills/` and get invoked with the Skill tool or via slash commands. Each one is a scoped workflow definition with clear trigger conditions and step-by-step instructions.

### Workflow skills (the core loop)

**`grill-me`** — Stress-tests a plan or design before you commit to it. Asks the hard questions: what are the failure modes, what are the hidden dependencies, what did you assume that might be wrong. Use before any non-trivial architectural decision.

**`brainstorming`** — Forces exploration before implementation. Surfaces requirements, edge cases, and design options before a single line of code is written. Use before building any new feature, no matter how small it seems.

**`execplan-create`** — Turns a locked decision into a self-contained execution plan. Reads the codebase, names exact files and functions, defines milestones, writes acceptance criteria. A novice should be able to follow the plan cold.

**`execplan-improve`** — Deep-reads every file an existing plan references and rewrites the plan with code-grounded improvements. Catches wrong file paths, missing dependencies, and vague acceptance criteria before you start building.

**`implement-execplan`** — Executes an ExecPlan milestone by milestone. Updates Progress, Surprises, and Decision Log as it goes. Stops cleanly when blocked rather than guessing.

**`review-recent-work`** — Fresh-eyes code review pass after implementation. Reads the git diff, cross-references the original plan, fixes obvious issues immediately, reruns verification. Ends with a usefulness score.

**`intent-driven-development`** — Turns ambiguous requests into observable acceptance criteria before implementation. Critical for anything touching security, data, migrations, or external APIs.

### Diagnostic skills

**`error-handling`** — TypeScript error hierarchy patterns, Result pattern, API error envelopes, retry with backoff, React error boundaries. Reference when designing error handling for a new module.

**`database-migrations`** — Safe migration patterns for Postgres: concurrent indexes, expand-contract, batch backfills, zero-downtime column renames. ORM-specific guidance for Prisma, Drizzle, and Kysely.

**`e2e-testing`** — Playwright patterns: Page Object Model, stable locators, anti-flakiness strategies, CI config, artifact management. Reference when writing or reviewing E2E tests.

**`browser-qa`** — Post-deploy QA checklist: smoke test, interaction test, visual regression, accessibility. Outputs SHIP / SHIP WITH FIXES / DO NOT SHIP verdict.

**`canary-watch`** — Post-deploy monitoring: HTTP status, console errors, Core Web Vitals, SSE streams, static assets. Use after every production deploy.

### Utility skills

**`custom-rule-invoker`** — Adds project-level ECC rules when you're in a new git repo. Asks which rule sets are relevant before adding anything. Prevents context bloat from irrelevant rules.

**`help-me-parallelize`** — Confirms whether you actually need multiple Claude instances, sets up the right pattern (two terminals vs git worktrees), and gives you the exact commands and briefs for each instance.

**`instinct-status`** — Shows learned instincts from continuous-learning-v2 and resets the 14-day reminder. Run every two weeks to review what patterns have been captured and promote strong ones to skills.

---

## Agents

Agents are specialized subprocesses Claude can delegate to. They live in `~/.claude/agents/` and get invoked via the Agent tool. Each has scoped tool permissions and a specific model assignment (Haiku for cheap tasks, Sonnet for most work, Opus for deep reasoning).

### Planning and architecture

**`planner`** (Opus, read-only) — Feature implementation planning. Breaks work into milestones, identifies risks, writes implementation blueprints. Read-only tools so it can't accidentally modify anything.

**`architect`** (Opus, read-only) — System design and technical decision-making. Use for anything that spans multiple modules or has long-term architectural implications.

### Code quality

**`typescript-reviewer`** (Sonnet) — TypeScript/JavaScript code review focused on type safety, async correctness, Node/web security, and idiomatic patterns. Use after every significant TypeScript change.

**`code-reviewer`** (Sonnet) — General code quality, security, and maintainability review. Broader than typescript-reviewer, less language-specific.

**`security-reviewer`** (Sonnet) — OWASP Top 10, secrets detection, SSRF, injection, unsafe crypto. Use after anything touching auth, user input, or API endpoints.

**`silent-failure-hunter`** (Sonnet) — Finds swallowed errors, bad fallbacks, and missing error propagation. Particularly useful in async TypeScript codebases where errors disappear silently.

**`database-reviewer`** (Sonnet) — PostgreSQL query optimization, schema design, RLS policy review, migration safety. Use after any schema change or complex query.

### Testing

**`tdd-guide`** (Sonnet) — Enforces write-tests-first methodology. Drives RED-GREEN-IMPROVE cycle. Use when writing any new feature or fixing a bug.

**`e2e-runner`** (Sonnet) — Playwright specialist. Generates, maintains, and runs E2E tests. Manages test journeys, quarantines flaky tests, uploads artifacts.

### Maintenance

**`build-error-resolver`** (Sonnet) — Fixes build and TypeScript errors with minimal diffs. No architectural edits. Gets the build green quickly.

**`refactor-cleaner`** (Sonnet) — Dead code removal using knip, depcheck, ts-prune. Safely removes unused exports, imports, and files.

**`performance-optimizer`** (Sonnet) — Bottleneck analysis, bundle size reduction, render optimization, memory leak detection.

### Open source

**`opensource-forker`** — Copies files, strips secrets and credentials (20+ patterns), replaces internal references with placeholders.

**`opensource-sanitizer`** — Verifies a fork is clean before release. Scans for leaked secrets, PII, and internal references. Generates PASS/FAIL report.

**`opensource-packager`** — Generates complete OSS packaging: CLAUDE.md, setup.sh, README, LICENSE, CONTRIBUTING.md, GitHub issue templates.

### Other

**`seo-specialist`** — Technical SEO audits, meta tags, structured data, Core Web Vitals, sitemap issues.

---

## Rules

Rules are always-loaded guidelines that apply to every session. They live in `~/.claude/rules/` and fire automatically without being invoked. Unlike skills, you never call them — they're persistent constraints.

### Global rules (`rules/ecc/common/`)

These load in every session regardless of project:

- **`coding-style.md`** — Immutability as a hard requirement, KISS/DRY/YAGNI, file size limits (200-400 lines typical, 800 max), naming conventions, error handling standards
- **`testing.md`** — TDD workflow (RED-GREEN-IMPROVE), 80% minimum coverage, Arrange-Act-Assert pattern, descriptive test names
- **`security.md`** — Pre-commit security checklist: no hardcoded secrets, SQL injection prevention, XSS protection, CSRF, rate limiting, error message safety
- **`git-workflow.md`** — Conventional commits format (feat/fix/refactor/docs/test/chore), PR workflow, branch naming
- **`performance.md`** — Model selection guide (Haiku/Sonnet/Opus by task type), context window management, extended thinking usage
- **`agents.md`** — When to delegate to subagents, parallel execution patterns, multi-perspective analysis
- **`patterns.md`** — Repository pattern, API response envelope format, skeleton project approach
- **`hooks.md`** — Hook architecture documentation, TodoWrite usage, permission management
- **`code-review.md`** — Code review priorities, what to look for, how to report findings
- **`development-workflow.md`** — Research-first workflow, planning with agents, TDD cycle, code review, git operations

### TypeScript rules (`rules/ecc/typescript/`)

These load in TypeScript/JavaScript projects based on file path matching:

- **`coding-style.md`** — Explicit types on public APIs, interface vs type alias usage, no `any`, Zod for validation, immutable patterns with spread operators
- **`testing.md`** — Playwright for E2E, e2e-runner agent
- **`patterns.md`** — ApiResponse type, custom hooks pattern, Repository interface
- **`security.md`** — Never hardcode API keys, always validate env vars on startup
- **`hooks.md`** — PostToolUse hooks for prettier, tsc, console.log detection

### Archived rules

Python and web rules are stored in `~/.claude/rules-archive/` and only added to specific projects via `/custom-rule-invoker`. This prevents irrelevant rules from loading in every session and burning context.

---

## Hooks

Hooks are trigger-based automations that fire on specific Claude Code lifecycle events. They're configured in `~/.claude/settings.json`.

### UserPromptSubmit hooks (fires on every prompt)

**`skill-reminder.py`** — Detects task keywords (implement, build, fix, add, refactor, etc.) and injects a skill checklist into context before Claude responds. Forces the question "should I invoke a skill here?" on every meaningful task.

**`mcp-tool-count.py`** — Fires once per session on the first prompt. Reports active MCP servers and tool counts vs the 80-tool limit. Also checks if you're in a git repo without project rules and prompts `/custom-rule-invoker`. Also shows the 14-day learning reminder when it's time to run `/instinct-status`.

### PreToolUse hooks

**`tmux-reminder.py`** — Reminds you to use tmux before long-running bash commands so you can detach and reattach without losing the process.

**`git-push-review.py`** — Opens a review prompt before git push to catch anything worth double-checking.

**`block-md-files.py`** — Blocks Claude from creating new `.md` files unless they're README or CLAUDE.md. Prevents documentation sprawl.

**`observe.sh pre`** (continuous-learning-v2) — Captures every PreToolUse event to the project observations log.

### PostToolUse hooks

**`prettier-format.py`** — Runs Prettier after every file edit to `.ts`, `.tsx`, `.js`, `.jsx` files.

**`tsc-check.py`** — Runs TypeScript type check after edits to `.ts`/`.tsx` files.

**`console-log-warn.py`** — Warns when console.log appears in edited files.

**`ecc-metrics-bridge.js`** — Tracks tool count, modified file count, and session start time in a temp file for the statusline to read.

**`observe.sh post`** (continuous-learning-v2) — Captures every PostToolUse event to the project observations log.

### Stop hooks

**`console-log-audit.py`** — Checks all modified files for console.log before session ends.

**`session-end.js`** — Reads the session transcript, extracts tasks, tools used, and files modified, writes a session summary to `~/.claude/session-data/`. Loaded on next session start.

### PreCompact hook

**`pre-compact.js`** — Logs compaction events and marks the active session file before context compression. Prevents important context from being silently lost.

### SessionStart hook

**`session-start.js`** — Loads the most recent session summary matching the current project directory into context. Also loads learned instincts above the confidence threshold. Means Claude starts every session knowing where you left off.

---

## Session Memory

Three hooks work together to give Claude persistent memory across sessions:

**How it works:**

1. You work in a project
2. Every response, `session-end.js` updates a session file in `~/.claude/session-data/` with what was worked on, which files were touched, and what tools were used
3. Before context compaction, `pre-compact.js` marks the event in the session file
4. Next time you open Claude in the same project, `session-start.js` finds the matching session file and injects it as context

**Session files are project-matched.** A session in `~/discovery-tool` only loads in future `~/discovery-tool` sessions. Home directory sessions don't mix with project sessions.

**What gets saved:**
- Last 10 user messages (what you asked for)
- Files modified in the session
- Tools used
- Timestamps for tracking progress rate

---

## Continuous Learning v2

An instinct-based learning system that captures patterns from your work and compounds them over time.

**The problem it solves:** You hit a bug, figure it out, move on. Two weeks later in a different project you hit the same bug and spend 20 minutes re-diagnosing it. Continuous learning captures the fix as an instinct the first time, so the second time Claude already knows.

**How it works:**

Every tool call fires `observe.sh` via PreToolUse and PostToolUse hooks. Each observation gets written to `~/.local/share/ecc-homunculus/projects/<hash>/observations.jsonl`. The project hash comes from your git remote URL so the same repo gets the same ID across machines.

Over time, patterns emerge in the observations. When you run `/instinct-status`, the system shows what it has learned. When you run `/evolve`, it clusters related instincts and suggests promoting them to full skills.

**Instinct example:**
```yaml
trigger: "when using Supabase Realtime"
action: "always add a polling fallback — Realtime drops silently"
confidence: 0.7
scope: discovery-tool (project)
```

**Scope rules:**
- Language/framework conventions, file structure, code style → project-scoped
- Security practices, general best practices, tool workflow → global

**Auto-promotion:** When the same instinct appears in 2+ projects with confidence >= 0.8, it promotes to global automatically.

**The 14-day reminder:** The session-start hook tracks when you last ran `/instinct-status` and reminds you when it's been two weeks.

**Background observer is off by default.** Observations accumulate silently. You control when patterns get extracted.

---

## Statusline

A terminal statusline showing live session metrics. Configured via `statusLine` in `settings.json`.

**Format:**
```
Sonnet 4.6 | $0.042 3m +47-12 | discovery-tool ████████░░ 72%
```

**What each segment means:**
- Model name
- Session cost in USD
- Duration in minutes
- Lines added and removed
- Current working directory
- Context window usage bar with color thresholds (green < 50%, yellow < 65%, orange < 65%, red >= 80%)

The statusline updates after every assistant response. It runs locally and does not consume API tokens.

---

## Context Aliases

Three terminal aliases for starting Claude in a specific mode:

```bash
alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'
alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'
alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'
```

**`claude-dev`** — Default building mode. Stay in execution mode, run validation after changes, commit validated batches, follow the project CLAUDE.md strictly.

**`claude-review`** — Critic mode. Be skeptical, find bugs before they hit production, check for security issues, look for edge cases. Prioritizes finding problems over building features.

**`claude-research`** — Exploration mode. No code changes. Produce a recommendation document with current state, options, tradeoffs, and a single clear recommendation. Use when figuring out how to approach something new before committing to an approach.

**Switching modes mid-session:** You can't switch the system prompt mid-session. The options are: open a second terminal in the new mode, use `/fork` and instruct it verbally, or just ask Claude directly to switch mindset.

---

## ExecPlan Workflow

A structured planning and execution system that ensures every non-trivial task has a self-contained plan before implementation begins.

**The workflow:**

```
grill-me → execplan-create → execplan-improve → implement-execplan → review-recent-work
```

**Plans live in `.agent/work/<slug>/`** within each project:
- `meta.json` — stage, state, timestamps
- `decision.md` (optional) — why this approach was chosen, what was rejected
- `execplan.md` — the actual plan

**The key requirement:** Every ExecPlan must be fully self-contained. A novice with only the plan and the codebase should be able to implement it end-to-end without prior context. This means defining jargon, naming exact files, showing exact commands, and describing observable acceptance criteria.

**`grill-me` replaces `decision.md`** for most cases. If you've stress-tested the approach with grill-me, that session is your decision artifact.

---

## Session Flows

### Starting a new project

```
1. Open Claude in the new project directory
   (hook fires: MCP count + project rules check)

2. /custom-rule-invoker
   Add relevant rules for this stack

3. /brainstorming
   Figure out what you're actually building before touching code

4. /grill-me
   Stress-test the approach before committing

5. /execplan-create
   Turn the decision into a step-by-step plan

6. /implement-execplan
   Execute milestone by milestone

7. "Have the typescript-reviewer check this"
   After each meaningful chunk of code

8. /review-recent-work
   Fresh-eyes pass on what was just built

9. "Run the security-reviewer on anything touching auth or user input"
   Before shipping anything public-facing
```

### Building a feature in an existing codebase

```
1. Open Claude in the project directory
   (hook fires: session memory loads, MCP count shows)

2. /brainstorming
   Even for small features — 5 minutes here saves an hour later

3. /grill-me (if non-trivial)
   Skip for obvious tasks, use for anything architectural

4. /execplan-create
   Skip only for truly trivial changes (one-liners, typos)

5. /implement-execplan
   Execute milestone by milestone

6. "Have the typescript-reviewer check this"
   After writing code

7. "Have the database-reviewer check this migration"
   After any schema change

8. "Run the security-reviewer"
   After anything touching auth, user input, or API endpoints

9. /review-recent-work
   Before committing

10. /verification-before-completion
    Before claiming it's done
```

---

## MCP Discipline

Claude Code's context window degrades significantly with too many active MCP servers. The rule: keep active tools under 80.

**The session-start hook reports your current count** every time you open Claude. If you're over 80, run `/mcp` to disable unused servers.

**The `mcp-tool-counts.json` file** tracks exact tool counts per server. Update it when you add or remove servers. The hook uses it to calculate your real total rather than estimating.

**The 80-tool rule applies to active servers only.** You can have 20 servers configured and only 5 enabled. Configure generously, enable surgically.

---

## Installation

### Prerequisites

- Claude Code CLI v2.1+
- Node.js 18+
- Python 3.x

### Step 1: Clone and copy files

```bash
git clone https://github.com/arjunasudani/my-claude-code-setup.git
cd my-claude-code-setup

# Skills
mkdir -p ~/.claude/skills
cp skills/*.md ~/.claude/skills/

# Agents
mkdir -p ~/.claude/agents
cp agents/*.md ~/.claude/agents/

# Rules
mkdir -p ~/.claude/rules/ecc
cp -r rules/ecc/common ~/.claude/rules/ecc/
cp -r rules/ecc/typescript ~/.claude/rules/ecc/

# Hooks
mkdir -p ~/.claude/hooks
cp hooks/*.py hooks/*.js ~/.claude/hooks/

# Contexts
mkdir -p ~/.claude/contexts
cp contexts/*.md ~/.claude/contexts/

# Scripts (session memory)
cp -r scripts ~/.claude/scripts
```

### Step 2: Wire up settings.json

Merge the hooks, statusLine, and env sections from `settings.json` into your `~/.claude/settings.json`. Don't overwrite your existing settings — add the new hook entries to your existing hook arrays.

### Step 3: Add context aliases

```bash
echo 'alias claude-dev='"'"'claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'"'"'' >> ~/.zshrc
echo 'alias claude-review='"'"'claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'"'"'' >> ~/.zshrc
echo 'alias claude-research='"'"'claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'"'"'' >> ~/.zshrc
source ~/.zshrc
```

### Step 4: Set up continuous learning v2

```bash
# Copy the skill
cp -r ~/.claude/skills/continuous-learning-v2 ~/.claude/skills/

# Create directory structure
mkdir -p "${HOME}/.local/share/ecc-homunculus"/{instincts/{personal,inherited},evolved/{agents,skills,commands},projects}

# Make hook executable
chmod +x ~/.claude/skills/continuous-learning-v2/hooks/observe.sh
```

Then add the PreToolUse and PostToolUse observation hooks to your `settings.json` pointing to `observe.sh pre` and `observe.sh post`.

### Step 5: Install LSP plugins and mgrep

In a Claude Code session:

```
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin marketplace add https://github.com/mixedbread-ai/mgrep
/plugin install mgrep@Mixedbread-Grep
```

---

## Credits

Built on top of [ECC by affaan-m](https://github.com/affaan-m/ECC) (MIT license). The agents, rules, session memory scripts, and continuous learning system all come from ECC. The skills, hooks, context files, and session flows are custom. If you haven't read affaan's shortform and longform guides, start there — this repo is an implementation of those guides, not a replacement for reading them.
