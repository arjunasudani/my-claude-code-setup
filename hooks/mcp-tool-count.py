#!/usr/bin/env python3
"""
UserPromptSubmit hook — fires once per session on the first prompt.
Reports exact MCP tool counts and warns if over the 80-tool limit.

Tool counts come from ~/.claude/mcp-tool-counts.json (manually maintained).
Active servers are read from ~/.claude.json (manual MCPs) and
~/.claude/settings.json (enabled plugins).
"""
import json
import sys
import os
import tempfile
import time

MARKER_DIR = os.path.join(tempfile.gettempdir(), "claude-session-markers")
HOME = os.path.expanduser("~")
COUNTS_FILE = os.path.join(HOME, ".claude", "mcp-tool-counts.json")
CLAUDE_JSON = os.path.join(HOME, ".claude.json")
SETTINGS_JSON = os.path.join(HOME, ".claude", "settings.json")

# Map plugin names to their MCP server keys in the counts file
PLUGIN_TO_SERVER = {
    "chrome-devtools-mcp@claude-plugins-official": "chrome-devtools-mcp",
    "playwright@claude-plugins-official": "playwright",
    "context7@claude-plugins-official": "context7",
    "supabase@claude-plugins-official": "supabase",
    "vercel@claude-plugins-official": "vercel",
}

def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    session_id = data.get("session_id", "unknown")

    # Only fire once per session
    os.makedirs(MARKER_DIR, exist_ok=True)
    marker = os.path.join(MARKER_DIR, f"{session_id}.mcp-checked")
    if os.path.exists(marker):
        sys.exit(0)
    open(marker, "w").close()

    # Load tool counts cache
    try:
        with open(COUNTS_FILE) as f:
            counts_data = json.load(f)
        counts = counts_data.get("servers", {})
        limit = counts_data.get("_total_limit", 80)
    except Exception:
        print("[MCP CHECK] Could not read ~/.claude/mcp-tool-counts.json")
        sys.exit(0)

    # Get manually configured MCP servers from ~/.claude.json
    active_servers = {}
    try:
        with open(CLAUDE_JSON) as f:
            claude = json.load(f)
        for name in claude.get("mcpServers", {}).keys():
            tool_count = counts.get(name, "?")
            active_servers[name] = tool_count
        # claude.ai connected MCPs
        for name in claude.get("claudeAiMcpEverConnected", []):
            tool_count = counts.get(name, "?")
            active_servers[name] = tool_count
    except Exception:
        pass

    # Get plugin-provided MCP servers from settings.json
    try:
        with open(SETTINGS_JSON) as f:
            settings = json.load(f)
        enabled = settings.get("enabledPlugins", {})
        for plugin_id, is_enabled in enabled.items():
            if is_enabled and plugin_id in PLUGIN_TO_SERVER:
                server_key = PLUGIN_TO_SERVER[plugin_id]
                active_servers[server_key] = counts.get(server_key, "?")
    except Exception:
        pass

    # Calculate totals
    known_total = sum(v for v in active_servers.values() if isinstance(v, int))
    unknown_count = sum(1 for v in active_servers.values() if v == "?")

    over_limit = known_total > limit
    warn = "⚠️ " if over_limit else "✓ "

    lines = ["", f"[MCP TOOL CHECK — session start]"]

    # Sort by tool count descending
    sorted_servers = sorted(
        active_servers.items(),
        key=lambda x: x[1] if isinstance(x[1], int) else 0,
        reverse=True
    )

    for name, count in sorted_servers:
        count_str = str(count) if isinstance(count, int) else "?"
        lines.append(f"  {count_str:>4} tools  {name}")

    lines.append(f"  {'─'*30}")
    lines.append(f"  {warn}{known_total} total tools (limit: {limit})")

    if over_limit:
        excess = known_total - limit
        lines.append(f"  → {excess} tools over limit. Run /mcp to disable unused servers.")
    else:
        lines.append(f"  → Within limit. {limit - known_total} tools of headroom remaining.")

    if unknown_count:
        lines.append(f"  → {unknown_count} servers with unknown counts (update ~/.claude/mcp-tool-counts.json)")

    lines.append("")

    # Check if this is a project directory without rules set up
    cwd = data.get("cwd", os.getcwd())
    is_git_repo = os.path.exists(os.path.join(cwd, ".git"))
    has_project_rules = os.path.exists(os.path.join(cwd, ".claude", "rules", "ecc"))
    is_home = os.path.abspath(cwd) == os.path.expanduser("~")

    if is_git_repo and not has_project_rules and not is_home:
        lines.append(f"[PROJECT RULES] No project-level rules found in {os.path.basename(cwd)}/")
        lines.append(f"  → Run /custom-rule-invoker to add relevant rules for this project.")
        lines.append("")

    # Check when /instinct-status was last run (tracked via a timestamp file)
    INSTINCT_REMINDER_DAYS = 14
    instinct_ts_file = os.path.join(HOME, ".claude", "instinct-last-run.txt")
    should_remind = False
    days_since = None

    if not os.path.exists(instinct_ts_file):
        should_remind = True
    else:
        try:
            with open(instinct_ts_file) as f:
                last_run = float(f.read().strip())
            days_since = (time.time() - last_run) / 86400
            if days_since >= INSTINCT_REMINDER_DAYS:
                should_remind = True
        except Exception:
            should_remind = True

    if should_remind:
        if days_since is not None:
            lines.append(f"[LEARNING REMINDER] Last ran /instinct-status {int(days_since)} days ago.")
        else:
            lines.append(f"[LEARNING REMINDER] /instinct-status has never been run.")
        lines.append(f"  → Run /instinct-status and /evolve to extract learned patterns.")
        lines.append("")

    print("\n".join(lines))
    sys.exit(0)

main()
