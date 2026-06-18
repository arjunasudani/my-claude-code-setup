#!/usr/bin/env python3
import json, sys, subprocess

try:
    data = json.load(sys.stdin)
    path = data.get('tool_input', {}).get('file_path', '')
    if path and any(path.endswith(e) for e in ['.ts', '.tsx', '.js', '.jsx']):
        result = subprocess.run(
            ['grep', '-n', r'console\.log', path],
            capture_output=True, text=True
        )
        if result.stdout:
            print(f'⚠️  console.log in {path}:')
            print(result.stdout.strip())
except Exception:
    pass
