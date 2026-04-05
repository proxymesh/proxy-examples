#!/usr/bin/env python3
"""
AutoScraper (requests-based) with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name to print from the response

AutoScraper uses ``requests`` for downloads. Pass ``proxies`` (and other
``requests`` keyword arguments) through ``request_args`` on ``build()``,
``get_result_similar()``, and related methods.

Documentation: https://github.com/alirezamika/autoscraper
"""
import os
import sys

import requests
from autoscraper import AutoScraper

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
response_header = os.environ.get('RESPONSE_HEADER')

proxies = {'http': proxy_url, 'https': proxy_url}

response = requests.get(test_url, proxies=proxies, timeout=30)
print(f'Status: {response.status_code}')
print(f'Body: {response.text}')
if response_header:
    print(f'{response_header}: {response.headers.get(response_header)}')

# Example: scraper.build(url, wanted_list=[...], request_args={'proxies': proxies, 'timeout': 30})
AutoScraper()
