#!/usr/bin/env python3
import json, sys, subprocess, os

try:
    data = json.load(sys.stdin)
    path = data.get('tool_input', {}).get('file_path', '')
    if not path or not any(path.endswith(e) for e in ['.ts', '.tsx']):
        sys.exit(0)
    if not os.path.exists('tsconfig.json'):
        sys.exit(0)
    result = subprocess.run(
        ['npx', 'tsc', '--noEmit'],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0 and result.stdout.strip():
        print('⚠️  TypeScript errors:')
        print(result.stdout[:2000])
except Exception:
    pass
