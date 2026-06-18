#!/usr/bin/env node
/**
 * PostToolUse hook — maintains a session metrics bridge file.
 * Tracks tool count, modified file count, and session start time.
 * Written atomically so the statusline script can read it safely.
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const BRIDGE_DIR = path.join(os.tmpdir(), "claude-metrics");

function bridgeFile(sessionId) {
  return path.join(BRIDGE_DIR, `${sessionId}.json`);
}

function run() {
  let input = "";
  process.stdin.on("data", (chunk) => (input += chunk));
  process.stdin.on("end", () => {
    try {
      const data = JSON.parse(input || "{}");
      const sessionId = data.session_id || "default";

      fs.mkdirSync(BRIDGE_DIR, { recursive: true });

      const file = bridgeFile(sessionId);
      let metrics = {};
      try {
        metrics = JSON.parse(fs.readFileSync(file, "utf8"));
      } catch {}

      metrics.startTime = metrics.startTime || Date.now();
      metrics.toolCount = (metrics.toolCount || 0) + 1;

      // Track unique modified files
      const toolName = data.tool_name || "";
      const toolInput = data.tool_input || {};
      if (
        ["Edit", "Write", "MultiEdit"].includes(toolName) &&
        toolInput.file_path
      ) {
        metrics.fileSet = metrics.fileSet || [];
        if (!metrics.fileSet.includes(toolInput.file_path)) {
          metrics.fileSet.push(toolInput.file_path);
        }
      }
      metrics.fileCount = (metrics.fileSet || []).length;

      // Atomic write
      const tmp = file + ".tmp." + process.pid;
      fs.writeFileSync(tmp, JSON.stringify(metrics));
      fs.renameSync(tmp, file);
    } catch {}
    process.exit(0);
  });
}

run();
