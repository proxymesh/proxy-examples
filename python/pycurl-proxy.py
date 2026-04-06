#!/usr/bin/env python3
"""
pycurl (libcurl) with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)

Requires libcurl development headers to install the ``pycurl`` package. Options are
set with :meth:`pycurl.Curl.setopt` like any libcurl binding.

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
c = pycurl.Curl()
try:
    c.setopt(pycurl.URL, test_url)
    c.setopt(pycurl.PROXY, proxy_url)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.TIMEOUT, 30)
    c.setopt(pycurl.SSL_VERIFYPEER, 1)
    c.setopt(pycurl.WRITEDATA, buffer)
    c.perform()
    status = c.getinfo(pycurl.RESPONSE_CODE)
except pycurl.error as exc:
    errno, msg = exc.args
    print(f'Error: {msg}', file=sys.stderr)
    sys.exit(1)
finally:
    c.close()

print(f'Status: {status}')
print(f'Body: {buffer.getvalue().decode("utf-8", errors="replace")}')
