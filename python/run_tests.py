#!/usr/bin/env python3
"""
Run all Python proxy header examples as tests.

Configuration via environment variables:
    PROXY_URL    - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL     - URL to request (default: https://api.ipify.org?format=json)
    PROXY_HEADER - Header name to send to proxy (optional)
    PROXY_VALUE  - Header value to send to proxy (optional)

Usage:
    python run_tests.py              # Run all examples
    python run_tests.py requests     # Run specific example
    python run_tests.py -l           # List available examples
"""
import os
import sys
import subprocess
from pathlib import Path

# Examples to test (filename without .py)
EXAMPLES = [
    'requests-proxy-headers',
    'requests-proxy-headers-session',
    'urllib3-proxy-headers',
    'aiohttp-proxy-headers',
    'httpx-proxy-headers',
    'httpx-async-proxy-headers',
    'pycurl-proxy-headers',
    'pycurl-proxy-headers-lowlevel',
    'cloudscraper-proxy-headers',
    'autoscraper-proxy-headers',
]


def run_example(name: str) -> bool:
    """Run an example script and return True if successful."""
    script_dir = Path(__file__).parent
    script_path = script_dir / f"{name}.py"
    
    if not script_path.exists():
        print(f"  Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return True
        else:
            print(f"  Exit code: {result.returncode}")
            if result.stderr:
                print(f"  Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print("  Timeout after 30s")
        return False
    except Exception as e:
        print(f"  Exception: {e}")
        return False


def main():
    args = sys.argv[1:]
    
    # Handle -l/--list
    if '-l' in args or '--list' in args:
        print("Available examples:")
        for name in EXAMPLES:
            print(f"  {name}")
        sys.exit(0)
    
    # Handle -h/--help
    if '-h' in args or '--help' in args:
        print(__doc__)
        sys.exit(0)
    
    # Check for PROXY_URL
    if not os.environ.get('PROXY_URL') and not os.environ.get('HTTPS_PROXY'):
        print("Error: Set PROXY_URL environment variable", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print("  export PROXY_URL='http://user:pass@proxy:8080'", file=sys.stderr)
        sys.exit(1)
    
    # Determine which examples to run
    if args:
        examples = args
    else:
        examples = EXAMPLES
    
    print(f"\n{'='*50}")
    print("Running Python Proxy Header Examples")
    print(f"{'='*50}\n")
    
    passed = 0
    failed = 0
    
    for name in examples:
        print(f"[TEST] {name}...", end=" ", flush=True)
        if run_example(name):
            print("PASS")
            passed += 1
        else:
            print("FAIL")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}\n")
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
