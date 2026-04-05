#!/usr/bin/env python3
"""
urllib3 with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name to print from the response

urllib3's :class:`urllib3.ProxyManager` routes traffic through the proxy. It does
not support sending custom headers on the HTTPS CONNECT request or reading proxy
CONNECT response headers (see python-proxy-headers for that).

Default urllib3 retries repeat HTTPS CONNECT through the proxy; some providers
return errors such as ``407 too many failures`` when that happens, so retries
are disabled here.

Documentation: https://urllib3.readthedocs.io/en/stable/reference/urllib3.poolmanager.html
"""
import os
import sys

import urllib3

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
response_header = os.environ.get('RESPONSE_HEADER')

http = urllib3.ProxyManager(proxy_url, retries=False)
response = http.request('GET', test_url, timeout=urllib3.Timeout(30))

body = response.data.decode('utf-8', errors='replace')
print(f'Status: {response.status}')
print(f'Body: {body}')
if response_header:
    print(f'{response_header}: {response.headers.get(response_header)}')
