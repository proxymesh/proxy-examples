<?php

/**
 * Shared helpers for PHP proxy examples.
 */

function normalize_proxy_url(string $value): string
{
    $trimmed = trim($value);
    if ($trimmed === '') {
        return '';
    }

    if (!preg_match('/^[a-z][a-z0-9+\-.]*:\/\//i', $trimmed)) {
        $trimmed = "http://{$trimmed}";
    }

    $parts = parse_url($trimmed);
    if (!is_array($parts) || empty($parts['host'])) {
        return '';
    }

    $scheme = $parts['scheme'] ?? 'http';
    $host = $parts['host'];
    $port = $parts['port'] ?? 31280;
    $user = $parts['user'] ?? null;
    $pass = $parts['pass'] ?? null;

    $auth = '';
    if ($user !== null) {
        $auth = rawurlencode($user);
        if ($pass !== null) {
            $auth .= ':' . rawurlencode($pass);
        }
        $auth .= '@';
    }

    return sprintf('%s://%s%s:%d', $scheme, $auth, $host, $port);
}

function get_proxy_url(): string
{
    $raw = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
    if (!$raw) {
        fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
        exit(1);
    }

    $normalized = normalize_proxy_url($raw);
    if ($normalized === '') {
        fwrite(STDERR, "Error: Invalid PROXY_URL value\n");
        exit(1);
    }

    return $normalized;
}
