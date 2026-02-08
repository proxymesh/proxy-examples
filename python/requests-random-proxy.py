#!/usr/bin/env python3
"""
Random proxy rotation example.

Configuration via environment variables:
    PROXY_URLS - Comma-separated list of proxy URLs (required)
                 e.g., http://proxy1:8080,http://proxy2:8080
    TEST_URL   - URL to request (default: https://api.ipify.org?format=json)
"""
import os
import sys
import random
import requests

# Get configuration from environment
proxy_urls = os.environ.get('PROXY_URLS')
if not proxy_urls:
    print("Error: Set PROXY_URLS environment variable (comma-separated)", file=sys.stderr)
    print("Example: export PROXY_URLS='http://proxy1:8080,http://proxy2:8080'", file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')

# Parse proxy list and select random one
proxy_list = [p.strip() for p in proxy_urls.split(',')]
proxy_url = random.choice(proxy_list)

print(f"Using proxy: {proxy_url}")

proxies = {'http': proxy_url, 'https': proxy_url}

# Make request
response = requests.get(test_url, proxies=proxies)

# Output
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")
