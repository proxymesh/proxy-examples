#!/usr/bin/env python3
"""
urllib3 with proxy headers example.

This example shows how to send custom headers to a proxy server and
receive proxy response headers using the python-proxy-headers library.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/urllib3.html
"""
from python_proxy_headers import urllib3_proxy_manager

# Create a proxy manager with custom proxy headers
proxy = urllib3_proxy_manager.ProxyHeaderManager(
    'http://USERNAME:PASSWORD@PROXYHOST:PORT',
    proxy_headers={'X-ProxyMesh-Country': 'US'}
)

# Make a request
response = proxy.request('GET', 'https://api.ipify.org?format=json')

# Print response
print(f"Status: {response.status}")
print(f"Body: {response.data.decode('utf-8')}")

# Access proxy response headers (from CONNECT response)
proxy_ip = response.headers.get('X-ProxyMesh-IP')
print(f"Proxy IP: {proxy_ip}")
