#!/usr/bin/env python3
"""
Requests with proxy headers - Session example.

Configuration via environment variables:
    PROXY_URL    - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL     - URL to request (default: https://api.ipify.org?format=json)
    PROXY_HEADER - Header name to send to proxy (optional)
    PROXY_VALUE  - Header value to send to proxy (optional)

See: https://github.com/proxymesh/python-proxy-headers
"""
import os
import sys
from python_proxy_headers.requests_adapter import ProxySession

# Get configuration from environment
proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print("Error: Set PROXY_URL environment variable", file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
proxy_header = os.environ.get('PROXY_HEADER')
proxy_value = os.environ.get('PROXY_VALUE')

proxies = {'http': proxy_url, 'https': proxy_url}
proxy_headers = {proxy_header: proxy_value} if proxy_header and proxy_value else None

# Make requests using session
with ProxySession(proxy_headers=proxy_headers) as session:
    session.proxies = proxies
    
    response = session.get(test_url)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    print(f"X-ProxyMesh-IP: {response.headers.get('X-ProxyMesh-IP')}")
