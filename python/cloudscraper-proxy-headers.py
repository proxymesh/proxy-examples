#!/usr/bin/env python3
"""
CloudScraper with proxy headers example.

This example shows how to use CloudScraper with custom proxy headers.
CloudScraper bypasses Cloudflare protection while python-proxy-headers
enables sending/receiving custom proxy headers.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/cloudscraper.html
"""
from python_proxy_headers.cloudscraper_proxy import create_scraper

# Create a CloudScraper with proxy header support
scraper = create_scraper(
    proxy_headers={'X-ProxyMesh-Country': 'US'},
    browser='chrome'
)

# Set proxy
scraper.proxies = {
    'http': 'http://USERNAME:PASSWORD@PROXYHOST:PORT',
    'https': 'http://USERNAME:PASSWORD@PROXYHOST:PORT'
}

# Make request - Cloudflare bypass + proxy headers work together
response = scraper.get('https://api.ipify.org?format=json')

# Print response
print(f"Status: {response.status_code}")
print(f"Body: {response.text}")

# Access proxy response headers
proxy_ip = response.headers.get('X-ProxyMesh-IP')
print(f"Proxy IP: {proxy_ip}")
