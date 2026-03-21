#!/usr/bin/env node
/**
 * typed-rest-client with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Uses RestClient requestOptions.proxy (tunnel-based HTTPS CONNECT).
 */
import { RestClient } from 'typed-rest-client';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

const client = new RestClient('proxy-examples-javascript', null, null, {
    proxy: { proxyUrl: proxyUrl },
});

try {
    const result = await client.get(testUrl);

    console.log(`Status: ${result.statusCode}`);
    console.log(`Body: ${JSON.stringify(result.result)}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
