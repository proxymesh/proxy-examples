#!/usr/bin/env python3
"""
urllib3 with proxy headers example.

Configuration via environment variables:
    PROXY_URL    - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL     - URL to request (default: https://api.ipify.org?format=json)
    PROXY_HEADER - Header name to send to proxy (optional)
    PROXY_VALUE  - Header value to send to proxy (optional)

See: https://github.com/proxymesh/python-proxy-headers
"""
import os
import sys
from python_proxy_headers import urllib3_proxy_manager

# Get configuration from environment
proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print("Error: Set PROXY_URL environment variable", file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
proxy_header = os.environ.get('PROXY_HEADER')
proxy_value = os.environ.get('PROXY_VALUE')

proxy_headers = {proxy_header: proxy_value} if proxy_header and proxy_value else None

# Create proxy manager and make request
proxy = urllib3_proxy_manager.ProxyHeaderManager(proxy_url, proxy_headers=proxy_headers)
response = proxy.request('GET', test_url)

# Output
print(f"Status: {response.status}")
print(f"Body: {response.data.decode('utf-8')}")
print(f"X-ProxyMesh-IP: {response.headers.get('X-ProxyMesh-IP')}")
