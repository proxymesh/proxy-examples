#!/usr/bin/env python3
"""
httpx (sync) with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name to print from the response

Documentation: https://www.python-httpx.org/advanced/proxies/
"""
import os
import sys

import httpx

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
response_header = os.environ.get('RESPONSE_HEADER')

with httpx.Client(proxy=proxy_url, timeout=30.0) as client:
    response = client.get(test_url)

print(f'Status: {response.status_code}')
print(f'Body: {response.text}')
if response_header:
    print(f'{response_header}: {response.headers.get(response_header)}')
