#!/usr/bin/env python3
"""
httpx with proxy headers example.

This example shows how to send custom headers to a proxy server and
receive proxy response headers using the python-proxy-headers library.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/httpx.html
"""
import httpx
from python_proxy_headers import httpx_proxy

# Create a proxy with custom headers
proxy = httpx.Proxy(
    'http://USERNAME:PASSWORD@PROXYHOST:PORT',
    headers={'X-ProxyMesh-Country': 'US'}
)

# Make a request using the helper function
response = httpx_proxy.get('https://api.ipify.org?format=json', proxy=proxy)

# Print response
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

# Access proxy response headers (from CONNECT response)
proxy_ip = response.headers.get('X-ProxyMesh-IP')
print(f"Proxy IP: {proxy_ip}")
