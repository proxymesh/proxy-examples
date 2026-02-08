#!/usr/bin/env python3
"""
Requests with proxy headers - Session example.

This example shows how to use ProxySession for connection pooling
and making multiple requests with the same proxy header configuration.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/requests.html
"""
from python_proxy_headers.requests_adapter import ProxySession

proxies = {
    'http': 'http://USERNAME:PASSWORD@PROXYHOST:PORT',
    'https': 'http://USERNAME:PASSWORD@PROXYHOST:PORT'
}

# Create a session with proxy header support
with ProxySession(proxy_headers={'X-ProxyMesh-Country': 'US'}) as session:
    session.proxies = proxies
    
    # Make multiple requests with the same session
    r1 = session.get('https://api.ipify.org?format=json')
    print(f"Request 1 - IP: {r1.json()['ip']}, Proxy IP: {r1.headers.get('X-ProxyMesh-IP')}")
    
    r2 = session.get('https://httpbin.org/headers')
    print(f"Request 2 - Status: {r2.status_code}")
