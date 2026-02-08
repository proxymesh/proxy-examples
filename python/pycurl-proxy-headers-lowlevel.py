#!/usr/bin/env python3
"""
PycURL with proxy headers - low-level example.

This example shows how to add proxy header support to existing pycurl code
using the low-level helper functions from python-proxy-headers.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/pycurl.html
"""
import pycurl
from io import BytesIO
from python_proxy_headers.pycurl_proxy import set_proxy_headers, HeaderCapture

# Create a pycurl handle
c = pycurl.Curl()
buffer = BytesIO()

# Configure the request
c.setopt(pycurl.URL, 'https://api.ipify.org?format=json')
c.setopt(pycurl.PROXY, 'http://USERNAME:PASSWORD@PROXYHOST:PORT')
c.setopt(pycurl.WRITEDATA, buffer)

# Add custom headers to send to the proxy
set_proxy_headers(c, {'X-ProxyMesh-Country': 'US'})

# Capture response headers (installs HEADERFUNCTION callback)
capture = HeaderCapture(c)

# Perform the request
c.perform()

# Print results
print(f"Status: {c.getinfo(pycurl.RESPONSE_CODE)}")
print(f"Body: {buffer.getvalue().decode('utf-8')}")

# Access headers from the proxy's CONNECT response
print(f"Proxy headers: {capture.proxy_headers}")
print(f"Proxy IP: {capture.proxy_headers.get('X-ProxyMesh-IP')}")

# Access headers from the origin server
print(f"Origin headers: {capture.origin_headers}")

c.close()
