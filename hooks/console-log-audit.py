#!/usr/bin/env python3
import sys, os, glob, subprocess

if os.getcwd() == os.path.expanduser("~"):
    sys.exit(0)

try:
    files = (
        glob.glob('**/*.ts', recursive=True) +
        glob.glob('**/*.tsx', recursive=True) +
        glob.glob('**/*.js', recursive=True) +
        glob.glob('**/*.jsx', recursive=True)
    )
    files = [f for f in files if 'node_modules' not in f and 'dist' not in f and '.next' not in f]

    found = []
    for f in files:
        result = subprocess.run(['grep', '-n', r'console\.log', f], capture_output=True, text=True)
        if result.stdout:
            found.append(f'{f}:\n{result.stdout.strip()}')

    if found:
        print('⚠️  SESSION AUDIT: console.log statements found:')
        print('\n\n'.join(found))
except Exception:
    pass
