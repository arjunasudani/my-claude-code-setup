#!/usr/bin/env node
/**
 * Claude Code statusLine script.
 *
 * Input JSON fields used:
 *   model.display_name          — model name
 *   workspace.current_dir       — working directory
 *   context_window.used_percentage — context %
 *   cost.total_cost_usd         — session cost
 *   cost.total_duration_ms      — session duration
 *   cost.total_lines_added      — lines added
 *   cost.total_lines_removed    — lines removed
 *   workspace.repo.name         — git repo name (if in a repo)
 *
 * Output: Model | $cost Xm +A-R | dir ████████░░ 68%
 */
const fs = require("fs");
const path = require("path");
const os = require("os");

const RESET = "\x1b[0m";
const GREEN = "\x1b[32m";
const YELLOW = "\x1b[33m";
const ORANGE = "\x1b[38;5;208m";
const RED = "\x1b[31m";
const DIM = "\x1b[2m";
const BOLD = "\x1b[1m";

function contextColor(pct) {
  if (pct >= 80) return RED;
  if (pct >= 65) return ORANGE;
  if (pct >= 50) return YELLOW;
  return GREEN;
}

function contextBar(pct) {
  const total = 10;
  const filled = Math.round((pct / 100) * total);
  const bar = "█".repeat(filled) + "░".repeat(total - filled);
  return `${contextColor(pct)}${bar}${RESET}`;
}

function run() {
  let input = "";
  const timer = setTimeout(() => {
    process.stdout.write("claude\n");
    process.exit(0);
  }, 3000);

  process.stdin.on("data", (chunk) => (input += chunk));
  process.stdin.on("end", () => {
    clearTimeout(timer);
    try {
      const d = JSON.parse(input || "{}");

      const model = (d.model && d.model.display_name) || "Claude";
      const dir = path.basename(
        (d.workspace && d.workspace.current_dir) || process.cwd(),
      );
      const pct = Math.round(
        d.context_window && d.context_window.used_percentage != null
          ? d.context_window.used_percentage
          : 0,
      );

      const cost =
        d.cost && d.cost.total_cost_usd != null
          ? `$${d.cost.total_cost_usd.toFixed(3)}`
          : null;

      const durationMin =
        d.cost && d.cost.total_duration_ms
          ? Math.round(d.cost.total_duration_ms / 60000)
          : 0;
      const duration = durationMin > 0 ? `${durationMin}m` : null;

      const linesAdded = d.cost && d.cost.total_lines_added;
      const linesRemoved = d.cost && d.cost.total_lines_removed;
      const lines =
        linesAdded || linesRemoved
          ? `${linesAdded ? `+${linesAdded}` : ""}${linesRemoved ? `-${linesRemoved}` : ""}`
          : null;

      const bar = contextBar(pct);
      const pctStr = `${contextColor(pct)}${pct}%${RESET}`;

      const metricsParts = [cost, duration, lines].filter(Boolean).join(" ");

      const segments = [
        `${DIM}${model}${RESET}`,
        metricsParts || null,
        `${DIM}${dir}${RESET} ${bar} ${pctStr}`,
      ].filter(Boolean);

      process.stdout.write(segments.join(` ${DIM}|${RESET} `) + "\n");
    } catch {
      process.stdout.write("claude\n");
    }
    process.exit(0);
  });
}

run();
