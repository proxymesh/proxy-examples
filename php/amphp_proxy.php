#!/usr/bin/env php
<?php
/**
 * Amp HTTP Client with proxy example.
 *
 * Configuration via environment variables:
 *   PROXY_URL  - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *   TEST_URL   - URL to request (default: https://api.ipify.org?format=json)
 *
 * Amp HTTP Client is an async HTTP client for PHP. It supports proxies
 * but does NOT support custom CONNECT headers or reading proxy response headers.
 */

require_once __DIR__ . '/vendor/autoload.php';

use Amp\Http\Client\HttpClientBuilder;
use Amp\Http\Client\Request;
use Amp\Http\Tunnel\Http1TunnelConnector;
use Amp\Socket\SocketAddress;

$proxyUrl = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
if (!$proxyUrl) {
    fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
    exit(1);
}

$testUrl = getenv('TEST_URL') ?: 'https://api.ipify.org?format=json';

$parsedProxy = parse_url($proxyUrl);
$proxyHost = $parsedProxy['host'];
$proxyPort = $parsedProxy['port'] ?? 8080;

try {
    $connector = new Http1TunnelConnector(
        new SocketAddress($proxyHost, $proxyPort)
    );

    $client = (new HttpClientBuilder())
        ->usingPool($connector)
        ->build();

    $request = new Request($testUrl);
    $response = $client->request($request);

    echo "Status: " . $response->getStatus() . "\n";
    echo "Body: " . $response->getBody()->buffer() . "\n";
} catch (Exception $e) {
    fwrite(STDERR, "Error: " . $e->getMessage() . "\n");
    exit(1);
}
