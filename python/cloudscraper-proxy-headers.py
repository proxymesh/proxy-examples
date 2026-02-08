#!/usr/bin/env python3
"""
CloudScraper with proxy headers example.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    PROXY_HEADER    - Header name to send to proxy (optional)
    PROXY_VALUE     - Header value to send to proxy (optional)
    RESPONSE_HEADER - Header name to read from response (optional)

See: https://github.com/proxymesh/python-proxy-headers
"""
import os
import sys
from python_proxy_headers.cloudscraper_proxy import create_scraper

# Get configuration from environment
proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print("Error: Set PROXY_URL environment variable", file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
proxy_header = os.environ.get('PROXY_HEADER')
proxy_value = os.environ.get('PROXY_VALUE')
response_header = os.environ.get('RESPONSE_HEADER')

proxy_headers = {proxy_header: proxy_value} if proxy_header and proxy_value else None

# Create scraper with proxy headers
scraper = create_scraper(proxy_headers=proxy_headers, browser='chrome')
scraper.proxies = {'http': proxy_url, 'https': proxy_url}

# Make request
response = scraper.get(test_url)

# Output
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")
if response_header:
    print(f"{response_header}: {response.headers.get(response_header)}")
