#!/usr/bin/env php
<?php
/**
 * Symfony HttpClient with proxy example.
 *
 * Configuration via environment variables:
 *   PROXY_URL  - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *   TEST_URL   - URL to request (default: https://api.ipify.org?format=json)
 *
 * Symfony HttpClient is a modern, PSR-18 compatible HTTP client.
 * It supports proxies but does NOT support custom CONNECT headers or
 * reading proxy response headers.
 */

require_once __DIR__ . '/vendor/autoload.php';

use Symfony\Component\HttpClient\HttpClient;

$proxyUrl = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
if (!$proxyUrl) {
    fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
    exit(1);
}

$testUrl = getenv('TEST_URL') ?: 'https://api.ipify.org?format=json';

try {
    $client = HttpClient::create([
        'proxy' => $proxyUrl,
        'timeout' => 30,
    ]);

    $response = $client->request('GET', $testUrl);

    echo "Status: " . $response->getStatusCode() . "\n";
    echo "Body: " . $response->getContent() . "\n";
} catch (Exception $e) {
    fwrite(STDERR, "Error: " . $e->getMessage() . "\n");
    exit(1);
}
