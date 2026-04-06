#!/usr/bin/env python3
"""
AutoScraper with an HTTP proxy.

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - HTML page to scrape (default: https://httpbin.org/html)
    WANTED_TEXT     - Optional comma-separated substrings for ``wanted_list``. If unset,
                      the script reads the page once and derives a target from the first
                      ``<h1>`` (then ``<title>``, then first ``<p>``) so the string always
                      matches what AutoScraper actually receives (hard-coded defaults fail in
                      CI when proxies change whitespace or encoding).

AutoScraper downloads with ``requests`` via ``AutoScraper._fetch_html``; ``build()`` and
``get_result_similar()`` use ``request_args`` for the proxy.

Documentation: https://github.com/alirezamika/autoscraper
"""
import os
import sys
from typing import List

from autoscraper import AutoScraper
from bs4 import BeautifulSoup

proxy_url = os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
if not proxy_url:
    print('Error: Set PROXY_URL environment variable', file=sys.stderr)
    sys.exit(1)

test_url = os.environ.get('TEST_URL', 'https://httpbin.org/html')
wanted_raw = os.environ.get('WANTED_TEXT')

proxies = {'http': proxy_url, 'https': proxy_url}
request_args = {'proxies': proxies, 'timeout': 30}


def wanted_list_from_html(html: str) -> List[str]:
    """Pick a substring that definitely exists in this HTML for AutoScraper to learn."""
    soup = BeautifulSoup(html, 'lxml')
    for tag_name in ('h1', 'h2', 'title'):
        tag = soup.find(tag_name)
        if tag:
            text = tag.get_text(strip=True)
            if text:
                return [text]
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if len(text) >= 12:
            return [text[:240]]
    stripped = soup.get_text(strip=True)
    if len(stripped) >= 8:
        return [stripped[:240]]
    return []


html = AutoScraper._fetch_html(test_url, request_args=request_args)
if not html or not html.strip():
    print('Error: Empty response body from proxy fetch', file=sys.stderr)
    sys.exit(1)

if wanted_raw:
    wanted_list = [s.strip() for s in wanted_raw.split(',') if s.strip()]
else:
    wanted_list = wanted_list_from_html(html)
    if not wanted_list:
        print(
            'Error: Could not derive WANTED_TEXT from HTML (no headings or text).',
            file=sys.stderr,
        )
        sys.exit(1)

scraper = AutoScraper()
learned = scraper.build(html=html, url=test_url, wanted_list=wanted_list)
print(f'AutoScraper wanted_list: {wanted_list}')
print(f'AutoScraper build (values used to learn rules): {learned}')

similar = scraper.get_result_similar(test_url, request_args=request_args)
print(f'AutoScraper get_result_similar: {similar}')

if not learned and not similar:
    print(
        'Note: No matches. Set WANTED_TEXT to substrings that appear in the page, '
        'or use an HTML TEST_URL.',
        file=sys.stderr,
    )
    sys.exit(1)
