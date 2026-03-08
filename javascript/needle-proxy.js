#!/usr/bin/env node
/**
 * Needle with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Uses HttpsProxyAgent for CONNECT tunneling so HTTPS works reliably through
 * the proxy (Needle's built-in proxy option can fail with 503 on some proxies).
 * See: https://www.npmjs.com/package/needle#more-advanced-proxy-support
 */
import needle from 'needle';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

const agent = new HttpsProxyAgent(proxyUrl);

try {
    const response = await needle('get', testUrl, {
        agent,
    });

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
