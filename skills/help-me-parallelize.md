---
name: help-me-parallelize
description: Help the user decide whether to parallelize work across multiple Claude instances, and set it up if they do. Use when the user invokes /help-me-parallelize or asks about running multiple Claude instances.
---

# Help Me Parallelize

## Step 1: Do you actually need this?

Ask the user to describe what they want to do. Then check:

**Don't parallelize if:**
- The tasks are sequential (Task B depends on Task A finishing first)
- It's one focused feature that one Claude can handle in a single session
- You're mid-session with a lot of context — spinning up a second Claude won't have that context

**Do parallelize if:**
- Two genuinely independent workstreams exist right now
- One task is long-running (30+ min) and something else can't wait
- You want a dedicated "questions" Claude so your coding Claude stays focused

If parallelization isn't needed, say so directly and stop here.

## Step 2: Set it up

Once parallelization is confirmed, do the setup without asking — then give the user instructions at the end.

**Pattern A — Two terminals, same directory (most common)**

When the two Claudes will work on different files:

1. Run `/rename coding` in the current session to name this one
2. Then tell the user exactly:

> "Open a new terminal window, run these commands:
> ```
> cd <current project path>
> claude
> /rename <second task name>
> ```
> Then come back here and tell me when it's open — I'll give you the brief for each window."

**Pattern B — Git worktrees (overlapping files)**

When both Claudes might edit the same files:

1. Create the worktree:
```bash
git worktree add ../<project>-<task> <new-branch-name>
```

2. Then tell the user exactly:

> "Open a new terminal window, run these commands:
> ```
> cd ../<project>-<task>
> claude
> /rename <task name>
> ```
> When it's open, come back here. I'll give you the exact brief to paste into each window."

3. Write a one-sentence brief for each Claude instance covering: what it owns, what to produce, where to save output.

When the worktree task is done:
```bash
git worktree remove ../<project>-<task>
```

## Step 3: The cascade rule

- Max 3-4 active Claude instances at once
- Open new tasks to the right
- Sweep left to right, oldest to newest
- Close finished terminals before opening new ones

## Anti-patterns

- Don't parallelize just because you can — two focused sequential sessions often beat two confused parallel ones
- Don't let parallel Claudes edit the same file without worktrees
- Don't run parallel sessions without naming them — you'll lose track
- Don't start parallel work without a clear plan for each instance
