# my-claude-code-setup

My complete Claude Code configuration, built in one session working through the [ECC shortform and longform guides](https://github.com/affaan-m/ECC) by [@affaan-m](https://github.com/affaan-m).

**Who this is for:** solo builders and founders who ship fast with Claude Code and want a setup that compounds over time. Not for teams, not for enterprise. For someone who opens a terminal, types `claude`, and builds real things.

## What's in here

| Folder | Contents |
|---|---|
| `skills/` | 14 global skills covering the execplan workflow, grill-me, e2e-testing, database-migrations, error-handling, browser-qa, canary-watch, intent-driven-development, and more |
| `agents/` | 16 specialized subagents: planner, architect, typescript-reviewer, security-reviewer, database-reviewer, silent-failure-hunter, and more |
| `rules/ecc/common/` | 10 ECC common rules: coding style, testing, security, git workflow, patterns, performance, agents, hooks, code review, development workflow |
| `rules/ecc/typescript/` | 5 TypeScript-specific rules |
| `hooks/` | Automation hooks: skill reminder, MCP tool count, project rules reminder, prettier, tsc check, console.log audit, session memory, metrics bridge |
| `contexts/` | Claude mode contexts: dev, review, research |
| `scripts/hooks/` | ECC session memory scripts (SessionStart, Stop, PreCompact) |
| `scripts/lib/` | ECC library dependencies for session hooks |

## Key features

- **Session memory** - SessionStart/Stop/PreCompact hooks persist context across sessions so you never re-explain where you left off
- **Continuous learning v2** - instinct-based pattern capture with confidence scoring, project-scoped by default
- **Skill reminder** - UserPromptSubmit hook nudges skill invocation before every task
- **MCP tool count** - session-start report of active tools vs the 80-tool context limit
- **Statusline** - model, cost, duration, lines changed, context bar with color thresholds
- **Context aliases** - `claude-dev`, `claude-review`, `claude-research` terminal shortcuts for different modes
- **ExecPlan workflow** - grill-me to execplan-create to implement-execplan to review-recent-work

## Session flows

### Starting a new project
```
/custom-rule-invoker
/brainstorming
/grill-me
/execplan-create
/implement-execplan
typescript-reviewer
/review-recent-work
security-reviewer
```

### Building a feature in an existing codebase
```
/brainstorming
/grill-me (if non-trivial)
/execplan-create
/implement-execplan
typescript-reviewer
database-reviewer (if schema changed)
security-reviewer (if touching auth or user input)
/review-recent-work
/verification-before-completion
```

## Installation

```bash
# Copy skills
cp skills/*.md ~/.claude/skills/

# Copy agents
mkdir -p ~/.claude/agents
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

Then merge `settings.json` hooks and statusLine into your `~/.claude/settings.json`.

## Credits

Built on top of [ECC by affaan-m](https://github.com/affaan-m/ECC) (MIT license). The agents, rules, and session memory scripts all come from ECC. The skills, hooks, and context files are custom. If you haven't read affaan's shortform and longform guides, start there.
