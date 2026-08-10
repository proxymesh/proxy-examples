#!/usr/bin/env python3
"""
Basic proxy waterfall: try cheap tiers first, escalate only on failure.

Uses content-level validation (status, min body size, soft-block markers,
optional must_contain) so a soft block (HTTP 200 captcha page) escalates.

Tiers (skip missing optional proxies):
  1. direct              — no proxy
  2. datacenter          — PROXY_URL / PROXY_URL_DATACENTER / HTTPS_PROXY
  3. residential         — PROXY_URL_RESIDENTIAL
  4. unlocker            — PROXY_URL_UNLOCKER

Configuration via environment variables (see waterfall_common.py).

Example:
    export PROXY_URL='http://user:pass@us-ca.proxymesh.com:31280'
    export PROXY_URL_RESIDENTIAL='http://user:pass@residential.example:8080'
    python python/requests-waterfall-proxy.py

Article:
https://dev.to/votiakov/anti-bot-without-melting-your-budget-the-proxy-waterfall-4a04
"""
import sys

import requests

from waterfall_common import (
    build_tiers,
    get_test_url,
    load_expect,
    print_config,
    print_success,
    require_proxy_tier,
    run_waterfall,
)


def fetch(tier, url):
    proxies = None
    if tier.proxy_url:
        proxies = {'http': tier.proxy_url, 'https': tier.proxy_url}
    response = requests.get(url, proxies=proxies, timeout=30)
    return response.status_code, response.text


def main() -> int:
    tiers = build_tiers(include_tls=False)
    require_proxy_tier(tiers)
    test_url = get_test_url()
    expect = load_expect()
    print_config(tiers, test_url, expect)

    result = run_waterfall(tiers, test_url, expect, fetch)
    if result.ok:
        print_success(result)
        return 0

    print('\nAll tiers failed.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
