#!/usr/bin/env python3
"""
AutoScraper with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - HTML page to scrape (default: https://example.com/)
    WANTED_TEXT     - Comma-separated substrings AutoScraper should learn to extract
                      (default: Example Domain, matching the default TEST_URL)
    RESPONSE_HEADER - Optional header name to print from the first response

AutoScraper is built for HTML pages (BeautifulSoup + rules), not raw JSON APIs.
Pass ``proxies`` through ``request_args`` on ``build()`` and ``get_result_similar()``.

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

test_url = os.environ.get('TEST_URL', 'https://example.com/')
response_header = os.environ.get('RESPONSE_HEADER')
wanted_raw = os.environ.get('WANTED_TEXT', 'Example Domain')
wanted_list = [s.strip() for s in wanted_raw.split(',') if s.strip()]

proxies = {'http': proxy_url, 'https': proxy_url}
request_args = {'proxies': proxies, 'timeout': 30}

# Same pattern as other examples: show status from requests.
probe = requests.get(test_url, **request_args)
print(f'Status: {probe.status_code}')
if response_header:
    print(f'{response_header}: {probe.headers.get(response_header)}')

scraper = AutoScraper()
learned = scraper.build(test_url, wanted_list=wanted_list, request_args=request_args)
print(f'AutoScraper build (values used to learn rules): {learned}')

similar = scraper.get_result_similar(test_url, request_args=request_args)
print(f'AutoScraper get_result_similar: {similar}')

if not learned and not similar:
    print(
        'Note: No matches. Use an HTML TEST_URL and set WANTED_TEXT to text that '
        'appears on that page.',
        file=sys.stderr,
    )
    sys.exit(1)
