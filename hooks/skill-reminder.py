#!/usr/bin/env python3
"""
PreToolUse hook — shows a visible skill reminder on the first tool call of each session.
Fires once per session, visible to the user as a ⎿ notification.
"""
import sys
import json
import os
import tempfile

MARKER_DIR = os.path.join(tempfile.gettempdir(), "claude-session-markers")

try:
    data = json.load(sys.stdin)
    session_id = data.get("session_id", "unknown")
except Exception:
    sys.exit(0)

# Only fire once per session
os.makedirs(MARKER_DIR, exist_ok=True)
marker = os.path.join(MARKER_DIR, f"{session_id}.skill-reminded")
if os.path.exists(marker):
    sys.exit(0)
open(marker, "w").close()

print(
    "\n[SKILL CHECK] Before I start — have you invoked the right skill?\n"
    "  /grill-me              — stress-test a plan or design\n"
    "  /brainstorming         — before building any new feature\n"
    "  /execplan-create       — turn a decision into a step-by-step plan\n"
    "  /implement-execplan    — execute an existing plan\n"
    "  /systematic-debugging  — before fixing any bug\n"
    "  /review-recent-work    — after implementing\n"
    "  /verification-before-completion — before claiming done\n"
    "If one fits, stop me now and invoke it first.\n",
    file=sys.stderr
)

sys.exit(0)
