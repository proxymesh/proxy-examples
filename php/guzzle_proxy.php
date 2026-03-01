#!/usr/bin/env php
<?php
/**
 * Guzzle with proxy example.
 *
 * Configuration via environment variables:
 *   PROXY_URL  - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *   TEST_URL   - URL to request (default: https://api.ipify.org?format=json)
 *
 * Guzzle is the most popular PHP HTTP client. It supports proxies but does NOT
 * support sending custom headers during HTTPS CONNECT or reading proxy response headers.
 */

require_once __DIR__ . '/vendor/autoload.php';

use GuzzleHttp\Client;

$proxyUrl = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
if (!$proxyUrl) {
    fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
    exit(1);
}

$testUrl = getenv('TEST_URL') ?: 'https://api.ipify.org?format=json';

try {
    $client = new Client([
        'proxy' => $proxyUrl,
        'timeout' => 30,
    ]);

    $response = $client->get($testUrl);

    echo "Status: " . $response->getStatusCode() . "\n";
    echo "Body: " . $response->getBody() . "\n";
} catch (Exception $e) {
    fwrite(STDERR, "Error: " . $e->getMessage() . "\n");
    exit(1);
}
