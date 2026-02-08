#!/usr/bin/env python3
"""
httpx async with proxy headers example.

This example shows how to send custom headers to a proxy server and
receive proxy response headers using httpx's async client.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/httpx.html
"""
import asyncio
import httpx
from python_proxy_headers.httpx_proxy import AsyncHTTPProxyTransport


async def main():
    # Create a proxy with custom headers
    proxy = httpx.Proxy(
        'http://USERNAME:PASSWORD@PROXYHOST:PORT',
        headers={'X-ProxyMesh-Country': 'US'}
    )
    
    # Create async transport with proxy header support
    transport = AsyncHTTPProxyTransport(proxy=proxy)
    
    async with httpx.AsyncClient(mounts={'http://': transport, 'https://': transport}) as client:
        response = await client.get('https://api.ipify.org?format=json')
        
        # Print response
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")
        
        # Access proxy response headers (from CONNECT response)
        proxy_ip = response.headers.get('X-ProxyMesh-IP')
        print(f"Proxy IP: {proxy_ip}")


if __name__ == '__main__':
    asyncio.run(main())
