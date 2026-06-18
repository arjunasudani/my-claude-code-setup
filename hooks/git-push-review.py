#!/usr/bin/env python3
import json, sys

data = json.load(sys.stdin)
cmd = data.get('tool_input', {}).get('command', '')

if 'git push' in cmd:
    print('⚠️  GIT PUSH: Stop and ask the user to confirm before pushing.')
    print(f'Command: {cmd}')
