#!/usr/bin/env python3
"""
Scrapy with an HTTP proxy (runspider).

Configuration via environment variables:
    PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
    RESPONSE_HEADER - Optional header name to print from the response

Uses ``meta['proxy']`` on the request. For custom headers on the proxy tunnel
(ProxyMesh-style), see the scrapy-proxy-headers package linked from the README.

Documentation: https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpproxy
"""
import os
import sys

import scrapy
from scrapy.crawler import CrawlerProcess


class ProxiedIpifySpider(scrapy.Spider):
    name = 'proxied_ipify'
    custom_settings = {
        'LOG_LEVEL': 'WARNING',
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        proxy_url = os.environ['PROXY_URL']
        test_url = os.environ.get('TEST_URL', 'https://api.ipify.org?format=json')
        yield scrapy.Request(test_url, meta={'proxy': proxy_url}, dont_filter=True)

    def parse(self, response):
        rh = os.environ.get('RESPONSE_HEADER')
        print(f'Status: {response.status}')
        print(f'Body: {response.text}')
        if rh:
            key = rh.encode('utf-8')
            raw = response.headers.get(key)
            val = raw.decode('utf-8') if raw else None
            print(f'{rh}: {val}')


def main() -> None:
    if not (os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')):
        print('Error: Set PROXY_URL environment variable', file=sys.stderr)
        sys.exit(1)
    if not os.environ.get('PROXY_URL'):
        os.environ['PROXY_URL'] = os.environ['HTTPS_PROXY']

    process = CrawlerProcess()
    process.crawl(ProxiedIpifySpider)
    process.start()


if __name__ == '__main__':
    main()
