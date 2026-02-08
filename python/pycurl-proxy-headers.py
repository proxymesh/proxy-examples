#!/usr/bin/env python3
"""
PycURL with proxy headers example.

This example shows how to send custom headers to a proxy server and
receive proxy response headers using the python-proxy-headers library.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/pycurl.html
"""
from python_proxy_headers.pycurl_proxy import get

# Make a request through the proxy with custom headers
response = get(
    'https://api.ipify.org?format=json',
    proxy='http://USERNAME:PASSWORD@PROXYHOST:PORT',
    proxy_headers={'X-ProxyMesh-Country': 'US'}
)

# Print response
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

# Access proxy response headers (from CONNECT response)
proxy_ip = response.proxy_headers.get('X-ProxyMesh-IP')
print(f"Proxy IP: {proxy_ip}")
