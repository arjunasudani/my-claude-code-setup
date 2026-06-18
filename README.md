# my-claude-code-setup

My complete Claude Code configuration — built and refined over a single session covering both the ECC shortform and longform guides.

## What's in here

| Folder | Contents |
|---|---|
| `skills/` | 19 global skills — execplan workflow, grill-me, e2e-testing, database-migrations, error-handling, browser-qa, canary-watch, intent-driven-development, and more |
| `agents/` | 16 specialized subagents — planner, architect, typescript-reviewer, security-reviewer, database-reviewer, silent-failure-hunter, and more |
| `rules/ecc/common/` | 10 ECC common rules — coding style, testing, security, git workflow, patterns, performance, agents, hooks, code review, development workflow |
| `rules/ecc/typescript/` | 5 TypeScript-specific rules |
| `hooks/` | Automation hooks — skill reminder, MCP tool count, project rules reminder, prettier, tsc check, console.log audit, session memory, metrics bridge |
| `contexts/` | Claude mode contexts — dev, review, research |
| `scripts/hooks/` | ECC session memory scripts (SessionStart, Stop, PreCompact) |
| `scripts/lib/` | ECC library dependencies for session hooks |

## Key features

- **Session memory** — SessionStart/Stop/PreCompact hooks persist context across sessions
- **Continuous learning v2** — instinct-based pattern capture with confidence scoring
- **Skill reminder** — UserPromptSubmit hook nudges skill invocation before tasks
- **MCP tool count** — session-start report of active tools vs 80-tool limit
- **Statusline** — model, cost, duration, lines changed, context bar
- **Context aliases** — `claude-dev`, `claude-review`, `claude-research` terminal shortcuts
- **ExecPlan workflow** — grill-me → execplan-create → implement-execplan → review-recent-work

## Setup flows

### New project
```
/custom-rule-invoker → /brainstorming → /grill-me → /execplan-create → /implement-execplan → typescript-reviewer → /review-recent-work → security-reviewer
```

### Existing feature
```
/brainstorming → (/grill-me if non-trivial) → /execplan-create → /implement-execplan → typescript-reviewer → database-reviewer → security-reviewer → /review-recent-work → /verification-before-completion
```

## Installation

```bash
# Copy skills
cp skills/*.md ~/.claude/skills/

# Copy agents
cp agents/*.md ~/.claude/agents/

# Copy rules
mkdir -p ~/.claude/rules/ecc
cp -r rules/ecc/common ~/.claude/rules/ecc/
cp -r rules/ecc/typescript ~/.claude/rules/ecc/

# Copy hooks
cp hooks/*.py hooks/*.js ~/.claude/hooks/

# Copy contexts
mkdir -p ~/.claude/contexts
cp contexts/*.md ~/.claude/contexts/

# Copy scripts
cp -r scripts ~/.claude/scripts

# Add context aliases to ~/.zshrc
echo 'alias claude-dev='"'"'claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'"'"'' >> ~/.zshrc
echo 'alias claude-review='"'"'claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'"'"'' >> ~/.zshrc
echo 'alias claude-research='"'"'claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'"'"'' >> ~/.zshrc
```

Then merge the `settings.json` hooks and statusLine into your `~/.claude/settings.json`.

## Credits

Rules and agents sourced from [ECC by affaan-m](https://github.com/affaan-m/ECC) (MIT license).
Session memory scripts from ECC scripts/hooks.
