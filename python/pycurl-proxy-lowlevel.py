#!/usr/bin/env python3
"""
pycurl with an HTTP proxy (explicit setopt calls).

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)

Same behavior as ``pycurl-proxy.py`` but with each option set separately, which
matches how lower-level libcurl integrations are often structured.

Documentation: https://pycurl.io/docs/latest/curlobject.html
"""
import os
import sys
from io import BytesIO

import pycurl

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')

buffer = BytesIO()
handle = pycurl.Curl()

handle.setopt(pycurl.URL, test_url)
handle.setopt(pycurl.PROXY, proxy_url)
handle.setopt(pycurl.WRITEDATA, buffer)
handle.setopt(pycurl.FOLLOWLOCATION, 1)
handle.setopt(pycurl.TIMEOUT, 30)
handle.setopt(pycurl.SSL_VERIFYPEER, 1)

try:
    handle.perform()
    status = handle.getinfo(pycurl.RESPONSE_CODE)
except pycurl.error as exc:
    _errno, msg = exc.args
    print(f'Error: {msg}', file=sys.stderr)
    sys.exit(1)
finally:
    handle.close()

print(f'Status: {status}')
print(f'Body: {buffer.getvalue().decode("utf-8", errors="replace")}')
