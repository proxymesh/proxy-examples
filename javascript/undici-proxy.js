#!/usr/bin/env node
/**
 * Undici with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Undici is Node.js's recommended HTTP client (powers native fetch in Node 18+).
 * It has built-in ProxyAgent support with some customization options.
 *
 * Note: Undici's ProxyAgent supports custom request headers but the proxy
 * CONNECT response headers are not easily accessible.
 */
import { ProxyAgent, request } from 'undici';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

const proxyAgent = new ProxyAgent(proxyUrl);

try {
    const { statusCode, body } = await request(testUrl, {
        dispatcher: proxyAgent,
    });

    const data = await body.text();
    console.log(`Status: ${statusCode}`);
    console.log(`Body: ${data}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
} finally {
    await proxyAgent.close();
}
