#!/usr/bin/env python3
"""
PycURL with proxy headers - low-level example.

Configuration via environment variables:
    PROXY_URL    - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL     - URL to request (default: https://api.ipify.org?format=json)
    PROXY_HEADER - Header name to send to proxy (optional)
    PROXY_VALUE  - Header value to send to proxy (optional)

See: https://github.com/proxymesh/python-proxy-headers
"""
import os
import sys
import pycurl
from io import BytesIO
from python_proxy_headers.pycurl_proxy import set_proxy_headers, HeaderCapture

# Get configuration from environment
proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print("Error: Set PROXY_URL environment variable", file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
proxy_header = os.environ.get('PROXY_HEADER')
proxy_value = os.environ.get('PROXY_VALUE')

proxy_headers = {proxy_header: proxy_value} if proxy_header and proxy_value else None

# Create pycurl handle
c = pycurl.Curl()
buffer = BytesIO()

c.setopt(pycurl.URL, test_url)
c.setopt(pycurl.PROXY, proxy_url)
c.setopt(pycurl.WRITEDATA, buffer)

# Add proxy headers if configured
if proxy_headers:
    set_proxy_headers(c, proxy_headers)

# Capture response headers
capture = HeaderCapture(c)

# Perform request
c.perform()

# Output
print(f"Status: {c.getinfo(pycurl.RESPONSE_CODE)}")
print(f"Body: {buffer.getvalue().decode('utf-8')}")
print(f"X-ProxyMesh-IP: {capture.proxy_headers.get('X-ProxyMesh-IP')}")

c.close()
