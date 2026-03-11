#!/usr/bin/env php
<?php
/**
 * cURL with proxy example.
 *
 * Configuration via environment variables:
 *   PROXY_URL  - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *   TEST_URL   - URL to request (default: https://api.ipify.org?format=json)
 *
 * cURL is PHP's built-in HTTP client. It supports proxies and has the BEST
 * potential for custom proxy headers via CURLOPT_PROXYHEADER (PHP 7.0.7+).
 * However, reading proxy CONNECT response headers is still limited.
 */

$proxyUrl = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
if (!$proxyUrl) {
    fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
    exit(1);
}

$testUrl = getenv('TEST_URL') ?: 'https://api.ipify.org?format=json';

$ch = curl_init();

curl_setopt_array($ch, [
    CURLOPT_URL => $testUrl,
    CURLOPT_PROXY => $proxyUrl,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_SSL_VERIFYPEER => true,
    CURLOPT_TIMEOUT => 30,
]);

$response = curl_exec($ch);

if (curl_errno($ch)) {
    fwrite(STDERR, "Error: " . curl_error($ch) . "\n");
    curl_close($ch);
    exit(1);
}

$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

echo "Status: {$httpCode}\n";
echo "Body: {$response}\n";
