#!/usr/bin/env python3
"""
Inject a skill reminder when the prompt looks like a task.
Fires on implementation, debugging, planning, and research keywords.
"""
import sys
import json

try:
    data = json.load(sys.stdin)
    prompt = data.get("prompt", "").lower()
except Exception:
    sys.exit(0)

TASK_KEYWORDS = [
    "implement", "build", "add", "create", "fix", "refactor", "change",
    "update", "write", "make", "edit", "remove", "delete", "move",
    "migrate", "deploy", "configure", "debug", "investigate", "research",
    "plan", "design", "review", "audit", "test", "setup", "integrate",
]

if any(kw in prompt for kw in TASK_KEYWORDS):
    print(
        "\n[SKILL CHECK] Before responding, confirm whether a skill applies:\n"
        "  /grill-me              — stress-test a plan or design\n"
        "  /brainstorming         — before building any new feature\n"
        "  /execplan-create       — turn a decision into a step-by-step plan\n"
        "  /implement-execplan    — execute an existing plan\n"
        "  /systematic-debugging  — before fixing any bug\n"
        "  /review-recent-work    — after implementing\n"
        "  /verification-before-completion — before claiming done\n"
        "Invoke with the Skill tool if one fits. Skip this check only if the task is trivial.\n"
    )

sys.exit(0)
