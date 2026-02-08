#!/usr/bin/env python3
"""
Basic requests with proxy example.

Configuration via environment variables:
    PROXY_URL - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL  - URL to request (default: https://api.ipify.org?format=json)
"""
import os
import sys
import requests

# Get configuration from environment
proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print("Error: Set PROXY_URL environment variable", file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')

proxies = {'http': proxy_url, 'https': proxy_url}

# Make request
response = requests.get(test_url, proxies=proxies)

# Output
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")
