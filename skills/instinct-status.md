---
name: instinct-status
description: Show learned instincts from continuous-learning-v2 and record that you ran it (resets the 14-day reminder). Use every 2 weeks to review what patterns have been captured and decide what to evolve into skills.
---

# Instinct Status

## Step 1: Record that this was run

Write the current timestamp to `~/.claude/instinct-last-run.txt` so the session-start reminder resets:

```bash
date +%s > ~/.claude/instinct-last-run.txt
```

## Step 2: Show learned instincts

Run the instinct CLI:

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py status
```

This shows all captured instincts grouped by project and global scope, with confidence scores.

## Step 3: Decide what to evolve

If any instincts have confidence ≥ 0.7 and you've seen them repeatedly, run:

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py evolve
```

This clusters related instincts and suggests promoting them to full skills.

## Step 4: Promote strong global patterns

If any project instincts appear across multiple projects at high confidence:

```bash
python3 ~/.claude/skills/continuous-learning-v2/scripts/instinct-cli.py promote
```
