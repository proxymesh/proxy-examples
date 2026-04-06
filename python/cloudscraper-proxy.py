#!/usr/bin/env python3
"""
cloudscraper with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name to print from the response

cloudscraper builds on requests; set ``proxies`` on the scraper like a Session.

Documentation: https://github.com/VeNoMouS/cloudscraper
"""
import os
import sys

import cloudscraper

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
response_header = os.environ.get('RESPONSE_HEADER')

proxies = {'http': proxy_url, 'https': proxy_url}
scraper = cloudscraper.create_scraper(browser='chrome')
scraper.proxies = proxies

response = scraper.get(test_url, timeout=30)

print(f'Status: {response.status_code}')
print(f'Body: {response.text}')
if response_header:
    print(f'{response_header}: {response.headers.get(response_header)}')
