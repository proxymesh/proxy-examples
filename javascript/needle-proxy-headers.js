#!/usr/bin/env node
/**
 * needle with javascript-proxy-headers (custom CONNECT headers).
 *
 * This complements needle-proxy.js (HttpsProxyAgent). Here, ProxyHeadersAgent is used
 * so you can send/receive custom proxy headers during CONNECT.
 *
 * Configuration via environment variables:
 *     PROXY_URL         - Proxy URL (required)
 *     TEST_URL          - URL to request (default: https://api.ipify.org?format=json)
 *     PROXY_HEADER      - Header name to send on CONNECT (optional)
 *     PROXY_VALUE       - Header value to send on CONNECT (optional)
 *     RESPONSE_HEADER   - Header name to read (optional; merged into res.headers)
 *
 * See: https://github.com/proxymesh/javascript-proxy-headers
 */
import { proxyNeedleGet } from 'javascript-proxy-headers/needle';

function headerFromObject(headers, name) {
    if (!headers || !name) return undefined;
    const lower = name.toLowerCase();
    for (const [k, v] of Object.entries(headers)) {
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
    const res = await proxyNeedleGet(testUrl, {
        proxy: proxyUrl,
        proxyHeaders,
    });

    console.log(`Status: ${res.statusCode}`);
    console.log(`Body: ${JSON.stringify(res.body)}`);

    if (responseHeader) {
        console.log(`${responseHeader}: ${headerFromObject(res.headers, responseHeader) ?? ''}`);
    }

    if (res.statusCode < 200 || res.statusCode >= 300) {
        process.exit(1);
    }
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
