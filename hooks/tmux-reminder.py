#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
cmd = data.get('tool_input', {}).get('command', '')

triggers = [
    'pnpm dev', 'npm dev', 'npm start', 'pnpm start',
    'yarn dev', 'yarn start', 'npm run dev', 'pnpm run dev',
    'cargo run', 'pytest', 'npm test', 'pnpm test', 'yarn test'
]

if any(t in cmd for t in triggers):
    print('⚠️  TMUX REMINDER: Long-running command detected.')
    print('Consider: tmux new -s dev  (then Ctrl+b d to detach without killing it)')
