"""
Shared helpers for proxy waterfall examples.

Pattern from:
https://dev.to/votiakov/anti-bot-without-melting-your-budget-the-proxy-waterfall-4a04

Environment:
    TEST_URL              Target URL (default: https://api.ipify.org?format=json)
    PROXY_URL             Datacenter / default proxy (also PROXY_URL_DATACENTER / HTTPS_PROXY)
    PROXY_URL_RESIDENTIAL Optional residential proxy tier
    PROXY_URL_UNLOCKER    Optional managed anti-bot / unlocker proxy tier
    EXPECT_STATUS         Required HTTP status (default: 200)
    EXPECT_MIN_BYTES      Minimum response body length (default: 0)
    EXPECT_MUST_CONTAIN   Substring that must appear in the body (optional)
    EXPECT_BLOCK_MARKERS  Extra soft-block markers, comma-separated (optional)
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple
from urllib.parse import urlparse

DEFAULT_TEST_URL = 'https://api.ipify.org?format=json'

# Soft-block / challenge substrings (content-level failure, not just status).
DEFAULT_BLOCK_MARKERS = (
    'captcha',
    'cf-challenge',
    'challenge-platform',
    'access denied',
    'attention required',
    'verify you are human',
    'just a moment',
)


@dataclass(frozen=True)
class Tier:
    name: str
    proxy_url: Optional[str]  # None = direct (no proxy)
    impersonate: Optional[str] = None  # e.g. "chrome" for curl_cffi Tier 0.5


@dataclass
class Expect:
    status: int = 200
    min_bytes: int = 0
    must_contain: Optional[str] = None
    block_markers: Tuple[str, ...] = DEFAULT_BLOCK_MARKERS


@dataclass
class AttemptResult:
    tier: Tier
    ok: bool
    reason: str
    status_code: Optional[int] = None
    body: Optional[str] = None


def mask_proxy_url(url: Optional[str]) -> str:
    """Mask password in a proxy URL for logging."""
    if not url:
        return '(direct)'
    try:
        parsed = urlparse(url)
        if parsed.password:
            return url.replace(f':{parsed.password}@', ':****@', 1)
        return url
    except Exception:
        return url


def load_expect() -> Expect:
    status = int(os.environ.get('EXPECT_STATUS', '200'))
    min_bytes = int(os.environ.get('EXPECT_MIN_BYTES', '0'))
    must_contain = os.environ.get('EXPECT_MUST_CONTAIN') or None
    extra = os.environ.get('EXPECT_BLOCK_MARKERS', '')
    markers = list(DEFAULT_BLOCK_MARKERS)
    if extra.strip():
        markers.extend(m.strip() for m in extra.split(',') if m.strip())
    return Expect(
        status=status,
        min_bytes=min_bytes,
        must_contain=must_contain,
        block_markers=tuple(markers),
    )


def get_test_url() -> str:
    return os.environ.get('TEST_URL', DEFAULT_TEST_URL)


def _datacenter_proxy() -> Optional[str]:
    return (
        os.environ.get('PROXY_URL_DATACENTER')
        or os.environ.get('PROXY_URL')
        or os.environ.get('HTTPS_PROXY')
    )


def build_tiers(*, include_tls: bool = False) -> List[Tier]:
    """
    Build the cheap-to-expensive ladder. Missing optional proxy tiers are skipped.
    """
    tiers: List[Tier] = [Tier(name='direct', proxy_url=None)]
    if include_tls:
        tiers.append(Tier(name='tls', proxy_url=None, impersonate='chrome'))

    datacenter = _datacenter_proxy()
    if datacenter:
        tiers.append(Tier(name='datacenter', proxy_url=datacenter))

    residential = os.environ.get('PROXY_URL_RESIDENTIAL')
    if residential:
        tiers.append(Tier(name='residential', proxy_url=residential))

    unlocker = os.environ.get('PROXY_URL_UNLOCKER')
    if unlocker:
        tiers.append(Tier(name='unlocker', proxy_url=unlocker))

    return tiers


def require_proxy_tier(tiers: Sequence[Tier]) -> None:
    """Fail fast when no proxy tier is configured (keep these as proxy examples)."""
    if any(t.proxy_url for t in tiers):
        return
    raise SystemExit(
        'Error: Set at least one proxy tier env var\n'
        "  PROXY_URL / PROXY_URL_DATACENTER  (datacenter)\n"
        '  PROXY_URL_RESIDENTIAL             (optional)\n'
        '  PROXY_URL_UNLOCKER                (optional)\n'
        "Example: export PROXY_URL='http://user:pass@proxy.example.com:8080'"
    )


def is_good(status_code: int, body: str, expect: Expect) -> Tuple[bool, str]:
    """Content-level validation — soft blocks fail even on HTTP 200."""
    if status_code != expect.status:
        return False, f'status {status_code} != {expect.status}'
    if len(body) < expect.min_bytes:
        return False, f'body {len(body)} bytes < min {expect.min_bytes}'
    lower = body.lower()
    for marker in expect.block_markers:
        if marker.lower() in lower:
            return False, f'soft-block marker {marker!r}'
    if expect.must_contain is not None and expect.must_contain not in body:
        return False, f'missing must_contain {expect.must_contain!r}'
    return True, 'ok'


def url_pattern(url: str) -> str:
    """Cache key: hostname (article uses URL pattern / domain)."""
    parsed = urlparse(url)
    return parsed.netloc.lower() or url


def describe_tier(tier: Tier) -> str:
    parts = [tier.name]
    if tier.impersonate:
        parts.append(f'impersonate={tier.impersonate}')
    parts.append(mask_proxy_url(tier.proxy_url))
    return ' | '.join(parts)


def print_config(tiers: Sequence[Tier], test_url: str, expect: Expect) -> None:
    print(f'Test URL:  {test_url}')
    print(f'Expect:    status={expect.status} min_bytes={expect.min_bytes}')
    if expect.must_contain:
        print(f'           must_contain={expect.must_contain!r}')
    print('Tiers:')
    for t in tiers:
        print(f'  - {describe_tier(t)}')
    print()


Fetcher = Callable[[Tier, str], Tuple[int, str]]


def run_waterfall(
    tiers: Sequence[Tier],
    url: str,
    expect: Expect,
    fetch: Fetcher,
    *,
    start_index: int = 0,
) -> AttemptResult:
    """
    Walk tiers from start_index onward. Returns the first good AttemptResult,
    or the last failure if all tiers fail.
    """
    if start_index < 0 or start_index >= len(tiers):
        start_index = 0

    last: Optional[AttemptResult] = None
    for tier in tiers[start_index:]:
        print(f'Trying tier: {describe_tier(tier)}')
        try:
            status_code, body = fetch(tier, url)
        except Exception as exc:
            last = AttemptResult(
                tier=tier,
                ok=False,
                reason=f'request error: {exc}',
            )
            print(f'  FAIL: {last.reason}')
            continue

        ok, reason = is_good(status_code, body, expect)
        last = AttemptResult(
            tier=tier,
            ok=ok,
            reason=reason,
            status_code=status_code,
            body=body,
        )
        if ok:
            print(f'  OK: {reason}')
            return last
        print(f'  FAIL: {reason} (status={status_code}, bytes={len(body)})')

    if last is None:
        return AttemptResult(
            tier=tiers[0] if tiers else Tier(name='none', proxy_url=None),
            ok=False,
            reason='no tiers to try',
        )
    return last


def print_success(result: AttemptResult) -> None:
    body = result.body or ''
    snippet = body if len(body) <= 500 else body[:500] + '...'
    print()
    print(f'Winner: {describe_tier(result.tier)}')
    print(f'Status: {result.status_code}')
    print(f'Body: {snippet}')


def tier_index_by_name(tiers: Sequence[Tier], name: str) -> Optional[int]:
    for i, t in enumerate(tiers):
        if t.name == name:
            return i
    return None
