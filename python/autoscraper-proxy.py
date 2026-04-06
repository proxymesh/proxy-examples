#!/usr/bin/env python3
"""
AutoScraper with a proxy (how to pass ``request_args``).

The AutoScraper project tests ``build`` / ``get_result_similar`` with **inline HTML**
only — see ``tests/unit/test_build.py`` and ``tests/integration/`` in
https://github.com/alirezamika/autoscraper — not with live URLs. That keeps tests
deterministic. This script does the same for the integration runner.

**Using a proxy with a real URL** matches the library README::

    scraper.build(url, wanted_list, request_args={'proxies': proxies, 'timeout': 30})
    scraper.get_result_similar(url, request_args={'proxies': proxies, 'timeout': 30})

``PROXY_URL`` is required here so this example fits the same env as the other scripts;
this demo does not open a network connection — it only exercises AutoScraper on
embedded HTML.

Configuration via environment variables:
    PROXY_URL  - Required by the test runner (same as other examples), e.g.
                 http://user:pass@proxy:8080

Documentation: https://github.com/alirezamika/autoscraper
"""
import os
import sys

from autoscraper import AutoScraper

# Same idea as upstream tests/unit/test_build.py — fixed HTML, no HTTP.
SAMPLE_HTML = """<!DOCTYPE html>
<html><head><title>Proxy example</title></head>
<body>
  <h1>AutoScraper proxy example</h1>
  <p>Paragraph one.</p>
</body></html>
"""
PLACEHOLDER_URL = 'https://example.invalid/autoscraper-proxy-demo'


def main() -> None:
    scraper = AutoScraper()
    wanted_list = ['AutoScraper proxy example']
    learned = scraper.build(
        html=SAMPLE_HTML,
        url=PLACEHOLDER_URL,
        wanted_list=wanted_list,
    )
    similar = scraper.get_result_similar(html=SAMPLE_HTML, url=PLACEHOLDER_URL)
    print(f'AutoScraper build: {learned}')
    print(f'AutoScraper get_result_similar: {similar}')
    if not learned:
        sys.exit(1)


if __name__ == '__main__':
    if not (os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')):
        print('Error: Set PROXY_URL environment variable', file=sys.stderr)
        sys.exit(1)
    main()
