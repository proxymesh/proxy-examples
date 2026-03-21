#!/usr/bin/env node
/**
 * ky with javascript-proxy-headers (custom CONNECT headers + proxy response headers).
 *
 * Configuration via environment variables:
 *     PROXY_URL         - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL          - URL to request (default: https://api.ipify.org?format=json)
 *     PROXY_HEADER      - Header name to send on CONNECT (optional)
 *     PROXY_VALUE       - Header value to send on CONNECT (optional)
 *     RESPONSE_HEADER   - Proxy response header to print (optional), e.g. X-ProxyMesh-IP
 *
 * See: https://github.com/proxymesh/javascript-proxy-headers
 */
import { createProxyKy } from 'javascript-proxy-headers/ky';

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
    const api = await createProxyKy({
        proxy: proxyUrl,
        proxyHeaders,
    });

    const response = await api(testUrl);
    const body = await response.text();

    console.log(`Status: ${response.status}`);
    console.log(`Body: ${body}`);

    if (responseHeader) {
        const fromProxy = mapGetInsensitive(response.proxyHeaders, responseHeader);
        const fromOrigin = response.headers.get(responseHeader);
        console.log(`${responseHeader}: ${fromProxy ?? fromOrigin ?? ''}`);
    }

    if (response.status < 200 || response.status >= 300) {
        process.exit(1);
    }
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
