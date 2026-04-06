#!/usr/bin/env python3
"""
AutoScraper with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - HTML page to scrape (default: https://httpbin.org/html)
    WANTED_TEXT     - Comma-separated substrings AutoScraper should learn to extract
                      (default: matches the <h1> on the default page)

AutoScraper downloads pages with ``requests`` internally (see ``AutoScraper._fetch_html``).
This script does not import ``requests`` itself: pass ``proxies`` and other ``requests``
keyword arguments only through ``request_args`` on ``build()`` and ``get_result_similar()``,
which is how you use a proxy with AutoScraper in real code.

AutoScraper targets HTML (BeautifulSoup + rules), not raw JSON APIs. For a simple proxied
``GET`` with status and headers printed, use ``requests-proxy.py``.

Documentation: https://github.com/alirezamika/autoscraper
"""
import os
import sys

from autoscraper import AutoScraper

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

# httpbin.org/html is stable test HTML; example.com is often blocked or rewritten in CI.
test_url = os.environ.get('TEST_URL', 'https://httpbin.org/html')
wanted_raw = os.environ.get('WANTED_TEXT', 'Herman Melville - Moby-Dick')
wanted_list = [s.strip() for s in wanted_raw.split(',') if s.strip()]

proxies = {'http': proxy_url, 'https': proxy_url}
request_args = {'proxies': proxies, 'timeout': 30}

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
