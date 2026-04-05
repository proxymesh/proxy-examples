#!/usr/bin/env python3
"""
Run all Python proxy examples as tests.

Configuration via environment variables:
    PROXY_URL    - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL     - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name for examples that print response headers

Usage:
    python run_tests.py              # Run all examples
    python run_tests.py requests     # Run specific example
    python run_tests.py -l           # List available examples
"""
import os
import sys
import subprocess
from pathlib import Path
from typing import List

# Examples to test (filename without .py)
EXAMPLES = [
    'requests-proxy',
    'requests-session-proxy',
    'urllib3-proxy',
    'aiohttp-proxy',
    'httpx-proxy',
    'httpx-async-proxy',
    'pycurl-proxy',
    'pycurl-proxy-lowlevel',
    'cloudscraper-proxy',
    'autoscraper-proxy',
    'scrapy-proxy',
]


def _scrapy_import_ok() -> bool:
    """Check Scrapy in a subprocess so a broken cryptography/cffi stack cannot abort this runner."""
    try:
        r = subprocess.run(
            [sys.executable, '-c', 'import scrapy'],
            capture_output=True,
            timeout=30,
        )
        return r.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def _available_examples() -> List[str]:
    """Skip examples when optional native / heavy dependencies are missing or broken."""
    try:
        import pycurl  # noqa: F401

        has_pycurl = True
    except ImportError:
        has_pycurl = False

    has_scrapy = _scrapy_import_ok()

    out: List[str] = []
    for e in EXAMPLES:
        if 'pycurl' in e and not has_pycurl:
            continue
        if e == 'scrapy-proxy' and not has_scrapy:
            continue
        out.append(e)
    return out


def run_example(name: str) -> bool:
    """Run an example script and return True if successful."""
    script_dir = Path(__file__).parent
    script_path = script_dir / f'{name}.py'

    if not script_path.exists():
        print(f'  Script not found: {script_path}')
        return False

    if name == 'scrapy-proxy':
        cmd = [sys.executable, '-m', 'scrapy', 'runspider', str(script_path)]
        timeout = 90
    else:
        cmd = [sys.executable, str(script_path)]
        timeout = 30

    try:
        result = subprocess.run(
            cmd,
            cwd=str(script_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.returncode == 0:
            return True
        print(f'  Exit code: {result.returncode}')
        if result.stderr:
            print(f'  Error: {result.stderr.strip()}')
        return False

    except subprocess.TimeoutExpired:
        print(f'  Timeout after {timeout}s')
        return False
    except Exception as e:
        print(f'  Exception: {e}')
        return False


def main():
    args = sys.argv[1:]

    if '-l' in args or '--list' in args:
        print('Available examples:')
        for name in _available_examples():
            print(f'  {name}')
        sys.exit(0)

    if '-h' in args or '--help' in args:
        print(__doc__)
        sys.exit(0)

    if not os.environ.get('PROXY_URL') and not os.environ.get('HTTPS_PROXY'):
        print('Error: Set PROXY_URL environment variable', file=sys.stderr)
        print('\nExample:', file=sys.stderr)
        print("  export PROXY_URL='http://user:pass@proxy:8080'", file=sys.stderr)
        sys.exit(1)

    available = _available_examples()
    if args:
        examples = [e for e in available if any(a in e for a in args)]
        if not examples:
            print('No matching examples.', file=sys.stderr)
            sys.exit(1)
    else:
        examples = available

    print(f"\n{'=' * 50}")
    print('Running Python Proxy Examples')
    print(f"{'=' * 50}\n")

    passed = 0
    failed = 0

    for name in examples:
        print(f'[TEST] {name}... ', end='', flush=True)
        if run_example(name):
            print('PASS')
            passed += 1
        else:
            print('FAIL')
            failed += 1

    print(f"\n{'=' * 50}")
    print(f'Results: {passed} passed, {failed} failed')
    print(f"{'=' * 50}\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
