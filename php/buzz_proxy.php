#!/usr/bin/env php
<?php
/**
 * Buzz with proxy example.
 *
 * Configuration via environment variables:
 *   PROXY_URL  - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *   TEST_URL   - URL to request (default: https://api.ipify.org?format=json)
 *
 * Buzz is a simple PSR-18 HTTP client. It supports proxies but does NOT
 * support custom CONNECT headers or reading proxy response headers.
 */

require_once __DIR__ . '/vendor/autoload.php';

use Buzz\Browser;
use Buzz\Client\Curl;
use Nyholm\Psr7\Factory\Psr17Factory;

$proxyUrl = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
if (!$proxyUrl) {
    fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
    exit(1);
}

$testUrl = getenv('TEST_URL') ?: 'https://api.ipify.org?format=json';

try {
    $psr17Factory = new Psr17Factory();
    
    $client = new Curl($psr17Factory, [
        'proxy' => $proxyUrl,
        'timeout' => 30,
    ]);
    
    $browser = new Browser($client, $psr17Factory);
    $response = $browser->get($testUrl);

    echo "Status: " . $response->getStatusCode() . "\n";
    echo "Body: " . $response->getBody() . "\n";
} catch (Exception $e) {
    fwrite(STDERR, "Error: " . $e->getMessage() . "\n");
    exit(1);
}
