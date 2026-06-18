#!/usr/bin/env python3
import json, sys, subprocess

try:
    data = json.load(sys.stdin)
    path = data.get('tool_input', {}).get('file_path', '')
    if path and any(path.endswith(e) for e in ['.ts', '.tsx', '.js', '.jsx']):
        subprocess.run(
            ['npx', 'prettier', '--write', path],
            capture_output=True, timeout=30
        )
except Exception:
    pass
