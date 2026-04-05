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
from urllib.parse import urlparse, urlunparse

import urllib3

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
response_header = os.environ.get('RESPONSE_HEADER')

parsed = urlparse(proxy_url)
pool_kw = {'retries': False}
if parsed.username is not None:
    # Some stacks omit CONNECT credentials unless they are sent as Proxy-Authorization.
    user = parsed.username
    password = parsed.password or ''
    pool_kw['proxy_headers'] = urllib3.util.make_headers(
        proxy_basic_auth=f'{user}:{password}'
    )
    host = parsed.hostname or ''
    if parsed.port:
        host = f'{host}:{parsed.port}'
    proxy_for_pool = urlunparse((parsed.scheme, host, '', '', '', ''))
else:
    proxy_for_pool = proxy_url

http = urllib3.ProxyManager(proxy_for_pool, **pool_kw)
response = http.request('GET', test_url, timeout=urllib3.Timeout(30))

body = response.data.decode('utf-8', errors='replace')
print(f'Status: {response.status}')
print(f'Body: {body}')
if response_header:
    print(f'{response_header}: {response.headers.get(response_header)}')
