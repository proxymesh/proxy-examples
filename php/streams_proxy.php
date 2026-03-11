#!/usr/bin/env php
<?php
/**
 * PHP Streams with proxy example.
 *
 * Configuration via environment variables:
 *   PROXY_URL  - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *   TEST_URL   - URL to request (default: https://api.ipify.org?format=json)
 *
 * PHP Streams (file_get_contents with context) support proxies but do NOT
 * support custom CONNECT headers or reading proxy response headers.
 * This is PHP's built-in HTTP capability without extensions.
 */

$proxyUrl = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
if (!$proxyUrl) {
    fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
    exit(1);
}

$testUrl = getenv('TEST_URL') ?: 'https://api.ipify.org?format=json';

$parsedProxy = parse_url($proxyUrl);
$proxyHost = $parsedProxy['host'];
$proxyPort = $parsedProxy['port'] ?? 8080;

$contextOptions = [
    'http' => [
        'proxy' => "tcp://{$proxyHost}:{$proxyPort}",
        'request_fulluri' => true,
        'timeout' => 30,
    ],
    'ssl' => [
        'verify_peer' => true,
        'verify_peer_name' => true,
    ],
];

// Add proxy authentication if provided
if (isset($parsedProxy['user'])) {
    $auth = base64_encode($parsedProxy['user'] . ':' . ($parsedProxy['pass'] ?? ''));
    $contextOptions['http']['header'] = "Proxy-Authorization: Basic {$auth}";
}

$context = stream_context_create($contextOptions);

$response = @file_get_contents($testUrl, false, $context);

if ($response === false) {
    $error = error_get_last();
    fwrite(STDERR, "Error: " . ($error['message'] ?? 'Unknown error') . "\n");
    exit(1);
}

// Get status from response headers
$status = 'Unknown';
if (isset($http_response_header[0])) {
    preg_match('/HTTP\/\d\.\d\s+(\d+)/', $http_response_header[0], $matches);
    $status = $matches[1] ?? 'Unknown';
}

echo "Status: {$status}\n";
echo "Body: {$response}\n";
