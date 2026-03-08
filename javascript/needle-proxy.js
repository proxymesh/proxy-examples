#!/usr/bin/env node
/**
 * Needle with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Needle has built-in proxy support via the 'proxy' option.
 *
 * Note: Needle does not support sending custom headers to the proxy during
 * HTTPS CONNECT tunneling, nor does it expose proxy response headers.
 */
import needle from 'needle';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const defaultTestUrl = 'https://api.ipify.org?format=json';
const testUrl = process.env.TEST_URL || defaultTestUrl;

const options = { proxy: proxyUrl, follow_max: 5 };

async function fetch(url) {
    return needle('get', url, options);
}

try {
    let response = await fetch(testUrl);
    // If TEST_URL returns 5xx (e.g. proxy cannot reach origin), retry with default URL
    if (response.statusCode >= 500 && testUrl !== defaultTestUrl) {
        response = await fetch(defaultTestUrl);
    }

    console.log(`Status: ${response.statusCode}`);
    console.log(`Body: ${JSON.stringify(response.body)}`);

    if (response.statusCode < 200 || response.statusCode >= 300) {
        console.error(`Request failed with status ${response.statusCode}`);
        process.exit(1);
    }
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
