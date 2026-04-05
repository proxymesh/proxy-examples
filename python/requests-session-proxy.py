#!/usr/bin/env python3
"""
Requests Session with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name to print from the response

Uses a :class:`requests.Session` for connection pooling. Same proxy options as
``requests.get(..., proxies=...)``.

Documentation: https://docs.python-requests.org/en/latest/user/advanced/#proxies
"""
import os
import sys

import requests

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
response_header = os.environ.get('RESPONSE_HEADER')

proxies = {'http': proxy_url, 'https': proxy_url}

with requests.Session() as session:
    session.proxies.update(proxies)
    response = session.get(test_url, timeout=30)

print(f'Status: {response.status_code}')
print(f'Body: {response.text}')
if response_header:
    print(f'{response_header}: {response.headers.get(response_header)}')
