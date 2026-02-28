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

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

try {
    const response = await needle('get', testUrl, {
        proxy: proxyUrl,
    });

    console.log(`Status: ${response.statusCode}`);
    console.log(`Body: ${JSON.stringify(response.body)}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
