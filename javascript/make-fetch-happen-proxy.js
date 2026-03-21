#!/usr/bin/env node
/**
 * make-fetch-happen with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Passes HttpsProxyAgent via opts.agent (handled by @npmcli/agent).
 */
import makeFetchHappen from 'make-fetch-happen';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';
const agent = new HttpsProxyAgent(proxyUrl);

const fetch = makeFetchHappen.defaults({ agent });

try {
    const response = await fetch(testUrl);
    const body = await response.text();

    console.log(`Status: ${response.status}`);
    console.log(`Body: ${body}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
