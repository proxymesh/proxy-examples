#!/usr/bin/env python3
"""
aiohttp with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name to print from the response

Documentation: https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support
"""
import asyncio
import os
import sys

import aiohttp

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
response_header = os.environ.get('RESPONSE_HEADER')


async def main() -> None:
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(test_url, proxy=proxy_url) as response:
            body = await response.text()
            print(f'Status: {response.status}')
            print(f'Body: {body}')
            if response_header:
                print(f'{response_header}: {response.headers.get(response_header)}')


if __name__ == '__main__':
    asyncio.run(main())
