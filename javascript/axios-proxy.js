#!/usr/bin/env node
/**
 * Axios with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Note: Axios does not support sending custom headers to the proxy during
 * HTTPS CONNECT tunneling, nor does it expose proxy response headers.
 * See: https://github.com/axios/axios/issues/3459
 */
import axios from 'axios';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

const agent = new HttpsProxyAgent(proxyUrl);

try {
    const response = await axios.get(testUrl, {
        httpsAgent: agent,
        httpAgent: agent,
    });

    console.log(`Status: ${response.status}`);
    console.log(`Body: ${JSON.stringify(response.data)}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
