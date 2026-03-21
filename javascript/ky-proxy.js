#!/usr/bin/env node
/**
 * ky with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * ky is given a fetch implementation backed by node-fetch + HttpsProxyAgent.
 */
import ky from 'ky';
import fetch from 'node-fetch';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';
const agent = new HttpsProxyAgent(proxyUrl);

function boundFetch(input, init = {}) {
    if (typeof Request !== 'undefined' && input instanceof Request) {
        const merged = new Request(input, init);
        return fetch(merged.url, {
            method: merged.method,
            headers: merged.headers,
            body: merged.body,
            redirect: merged.redirect,
            agent,
        });
    }
    return fetch(input, { ...init, agent });
}

try {
    const api = ky.create({ fetch: boundFetch });
    const response = await api(testUrl);
    const body = await response.text();

    console.log(`Status: ${response.status}`);
    console.log(`Body: ${body}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
