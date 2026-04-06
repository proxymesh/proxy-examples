#!/usr/bin/env node
/**
 * typed-rest-client with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Uses RestClient requestOptions.proxy (tunnel-based HTTPS CONNECT).
 *
 * typed-rest-client only applies proxy auth when proxyUsername / proxyPassword
 * are set; credentials embedded in proxyUrl are ignored (tunnel gets no
 * Proxy-Authorization), which yields 407 on authenticated proxies.
 */
import { URL } from 'url';
import { RestClient } from 'typed-rest-client';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

function proxyOptionsFromUrl(urlString) {
    const u = new URL(urlString);
    const base = `${u.protocol}//${u.hostname}${u.port ? `:${u.port}` : ''}`;
    const proxy = { proxyUrl: base };
    if (u.username !== '' || u.password !== '') {
        proxy.proxyUsername = decodeURIComponent(u.username);
        proxy.proxyPassword = decodeURIComponent(u.password);
    }
    return proxy;
}

const client = new RestClient('proxy-examples-javascript', null, null, {
    proxy: proxyOptionsFromUrl(proxyUrl),
});

try {
    const result = await client.get(testUrl);

    console.log(`Status: ${result.statusCode}`);
    console.log(`Body: ${JSON.stringify(result.result)}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
