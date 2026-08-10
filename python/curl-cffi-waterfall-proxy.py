#!/usr/bin/env python3
"""
Proxy waterfall with a free TLS-fingerprint tier (article Tier 0.5).

Same ladder and content validation as requests-waterfall-proxy.py, but inserts
a direct request that impersonates Chrome via curl_cffi before spending on
proxy IPs. Requires: pip install curl_cffi

Tiers (skip missing optional proxies):
  1. direct              — curl_cffi, no impersonation, no proxy
  2. tls                 — curl_cffi impersonate=chrome, no proxy
  3. datacenter          — PROXY_URL / PROXY_URL_DATACENTER / HTTPS_PROXY
  4. residential         — PROXY_URL_RESIDENTIAL
  5. unlocker            — PROXY_URL_UNLOCKER

Example:
    pip install 'curl_cffi>=0.6.0'
    export PROXY_URL='http://user:pass@us-ca.proxymesh.com:31280'
    python python/curl-cffi-waterfall-proxy.py

Article:
https://dev.to/votiakov/anti-bot-without-melting-your-budget-the-proxy-waterfall-4a04
"""
import sys

from waterfall_common import (
    build_tiers,
    get_test_url,
    load_expect,
    print_config,
    print_success,
    require_proxy_tier,
    run_waterfall,
)

try:
    from curl_cffi import requests as curl_requests
except ImportError:
    print(
        'Error: curl_cffi is required for this example\n'
        "  pip install 'curl_cffi>=0.6.0'",
        file=sys.stderr,
    )
    sys.exit(1)


def fetch(tier, url):
    kwargs = {'timeout': 30}
    if tier.proxy_url:
        kwargs['proxies'] = {'http': tier.proxy_url, 'https': tier.proxy_url}
    if tier.impersonate:
        kwargs['impersonate'] = tier.impersonate
    response = curl_requests.get(url, **kwargs)
    return response.status_code, response.text


def main() -> int:
    tiers = build_tiers(include_tls=True)
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
