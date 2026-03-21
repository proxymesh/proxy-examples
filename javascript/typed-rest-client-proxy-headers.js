#!/usr/bin/env node
/**
 * typed-rest-client with javascript-proxy-headers (HTTPS via ProxyHeadersAgent).
 *
 * Configuration via environment variables:
 *     PROXY_URL         - Proxy URL (required)
 *     TEST_URL          - URL to request (default: https://api.ipify.org?format=json)
 *     PROXY_HEADER      - Header name to send on CONNECT (optional)
 *     PROXY_VALUE       - Header value to send on CONNECT (optional)
 *     RESPONSE_HEADER   - Proxy CONNECT response header to print (optional)
 *
 * See: https://github.com/proxymesh/javascript-proxy-headers
 */
import { createProxyRestClient } from 'javascript-proxy-headers/typed-rest-client';

function mapGetInsensitive(map, name) {
    if (!map || !name) return undefined;
    const lower = name.toLowerCase();
    for (const [k, v] of map) {
        if (k.toLowerCase() === lower) return v;
    }
    return undefined;
}

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';
const proxyHeader = process.env.PROXY_HEADER;
const proxyValue = process.env.PROXY_VALUE;
const responseHeader = process.env.RESPONSE_HEADER;

const proxyHeaders = proxyHeader && proxyValue ? { [proxyHeader]: proxyValue } : {};

try {
    const client = createProxyRestClient({
        userAgent: 'proxy-examples-javascript',
        proxy: proxyUrl,
        proxyHeaders,
    });

    const result = await client.get(testUrl);

    console.log(`Status: ${result.statusCode}`);
    console.log(`Body: ${JSON.stringify(result.result)}`);

    if (responseHeader) {
        const ph = client.proxyAgent.lastProxyHeaders;
        console.log(`${responseHeader}: ${mapGetInsensitive(ph, responseHeader) ?? ''}`);
    }

    if (result.statusCode < 200 || result.statusCode >= 300) {
        process.exit(1);
    }
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
