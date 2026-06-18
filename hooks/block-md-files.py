#!/usr/bin/env python3
import json, sys, os

data = json.load(sys.stdin)
path = data.get('tool_input', {}).get('file_path', '')

if path.endswith('.md'):
    basename = os.path.basename(path)
    if basename not in ['README.md', 'CLAUDE.md']:
        print(f'BLOCKED: Creating "{basename}" is not allowed.')
        print('Only README.md and CLAUDE.md are permitted. Skip this step.')
        sys.exit(1)
