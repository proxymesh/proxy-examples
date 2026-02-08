#!/usr/bin/env python3
"""
Requests with proxy headers example.

This example shows how to send custom headers to a proxy server and
receive proxy response headers using the python-proxy-headers library.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/requests.html
"""
from python_proxy_headers import requests_adapter

proxies = {
    # USERNAME:PASSWORD is optional if you have IP authentication
    'http': 'http://USERNAME:PASSWORD@PROXYHOST:PORT',
    'https': 'http://USERNAME:PASSWORD@PROXYHOST:PORT'
}

# Make a request with custom proxy headers
response = requests_adapter.get(
    'https://api.ipify.org?format=json',
    proxies=proxies,
    proxy_headers={'X-ProxyMesh-Country': 'US'}
)

# Print response
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

# Access proxy response headers (from CONNECT response)
proxy_ip = response.headers.get('X-ProxyMesh-IP')
print(f"Proxy IP: {proxy_ip}")
