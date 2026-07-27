#!/usr/bin/env python3
"""
Proxy waterfall with a TTL decision cache.

Same ladder and content validation as requests-waterfall-proxy.py, plus
remembering which tier worked for a host so later requests start there
instead of re-walking cheaper tiers every time.

Cache:
    WATERFALL_CACHE_TTL   Seconds to remember a winning tier (default: 86400)
    WATERFALL_CACHE_PATH  Optional JSON file path for persistence across runs

On a cache hit, start at the cached tier. If that tier fails, invalidate the
entry and continue down the remaining ladder. On success, refresh the cache.

Example:
    export PROXY_URL='http://user:pass@us-ca.proxymesh.com:31280'
    export PROXY_URL_RESIDENTIAL='http://user:pass@residential.example:8080'
    export WATERFALL_CACHE_PATH=/tmp/waterfall-cache.json
    python python/requests-waterfall-cache-proxy.py

Article:
https://dev.to/votiakov/anti-bot-without-melting-your-budget-the-proxy-waterfall-4a04
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from waterfall_common import (
    build_tiers,
    get_test_url,
    load_expect,
    print_config,
    print_success,
    require_proxy_tier,
    run_waterfall,
    tier_index_by_name,
    url_pattern,
)


def fetch(tier, url):
    proxies = None
    if tier.proxy_url:
        proxies = {'http': tier.proxy_url, 'https': tier.proxy_url}
    response = requests.get(url, proxies=proxies, timeout=30)
    return response.status_code, response.text


def _cache_ttl() -> int:
    return int(os.environ.get('WATERFALL_CACHE_TTL', '86400'))


def _cache_path() -> Optional[Path]:
    raw = os.environ.get('WATERFALL_CACHE_PATH')
    return Path(raw) if raw else None


def load_cache() -> Dict[str, Any]:
    path = _cache_path()
    if not path or not path.is_file():
        return {}
    try:
        with path.open() as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError) as exc:
        print(f'Warning: could not read cache {path}: {exc}', file=sys.stderr)
        return {}


def save_cache(cache: Dict[str, Any]) -> None:
    path = _cache_path()
    if not path:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as f:
            json.dump(cache, f, indent=2, sort_keys=True)
            f.write('\n')
    except OSError as exc:
        print(f'Warning: could not write cache {path}: {exc}', file=sys.stderr)


def get_cached_tier(cache: Dict[str, Any], key: str) -> Optional[str]:
    entry = cache.get(key)
    if not isinstance(entry, dict):
        return None
    expires_at = entry.get('expires_at')
    tier_name = entry.get('tier')
    if not isinstance(expires_at, (int, float)) or not isinstance(tier_name, str):
        return None
    if time.time() >= expires_at:
        return None
    return tier_name


def set_cached_tier(cache: Dict[str, Any], key: str, tier_name: str) -> None:
    cache[key] = {
        'tier': tier_name,
        'expires_at': time.time() + _cache_ttl(),
    }


def invalidate(cache: Dict[str, Any], key: str) -> None:
    cache.pop(key, None)


def main() -> int:
    tiers = build_tiers(include_tls=False)
    require_proxy_tier(tiers)
    test_url = get_test_url()
    expect = load_expect()
    print_config(tiers, test_url, expect)

    key = url_pattern(test_url)
    cache = load_cache()
    cached_name = get_cached_tier(cache, key)
    start_index = 0

    if cached_name:
        idx = tier_index_by_name(tiers, cached_name)
        if idx is not None:
            start_index = idx
            print(f'Cache HIT for {key!r}: start at tier {cached_name!r} (index {idx})')
        else:
            print(
                f'Cache HIT for {key!r}: tier {cached_name!r} not in current ladder; '
                'starting from cheapest'
            )
            invalidate(cache, key)
    else:
        print(f'Cache MISS for {key!r}: start at cheapest tier')
    print()

    result = run_waterfall(
        tiers, test_url, expect, fetch, start_index=start_index
    )

    if result.ok:
        set_cached_tier(cache, key, result.tier.name)
        save_cache(cache)
        print(f'Cached winner {result.tier.name!r} for {key!r} (ttl={_cache_ttl()}s)')
        print_success(result)
        return 0

    # Cached start failed and remaining ladder failed — drop stale entry.
    if cached_name:
        invalidate(cache, key)
        save_cache(cache)
        print(f'Invalidated cache for {key!r}')

    print('\nAll tiers failed.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
