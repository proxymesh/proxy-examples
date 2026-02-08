#!/usr/bin/env python3
"""
aiohttp with proxy headers example.

This example shows how to send custom headers to a proxy server and
receive proxy response headers using the python-proxy-headers library
with async/await.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/aiohttp.html
"""
import asyncio
from python_proxy_headers import aiohttp_proxy


async def main():
    async with aiohttp_proxy.ProxyClientSession() as session:
        async with session.get(
            'https://api.ipify.org?format=json',
            proxy='http://USERNAME:PASSWORD@PROXYHOST:PORT',
            proxy_headers={'X-ProxyMesh-Country': 'US'}
        ) as response:
            # Print response
            print(f"Status: {response.status}")
            body = await response.text()
            print(f"Body: {body}")
            
            # Access proxy response headers (from CONNECT response)
            proxy_ip = response.headers.get('X-ProxyMesh-IP')
            print(f"Proxy IP: {proxy_ip}")


if __name__ == '__main__':
    asyncio.run(main())
