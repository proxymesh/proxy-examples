#!/usr/bin/env node
/**
 * Playwright with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Note: Playwright delegates proxy handling to the browser.
 * Custom proxy headers during HTTPS CONNECT are not supported as the browser
 * handles the tunneling internally.
 */
import { chromium } from 'playwright';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

const url = new URL(proxyUrl);

const browser = await chromium.launch({
    proxy: {
        server: `${url.protocol}//${url.hostname}:${url.port}`,
        username: url.username || undefined,
        password: url.password || undefined,
    },
});

try {
    const page = await browser.newPage();
    const response = await page.goto(testUrl);

    console.log(`Status: ${response.status()}`);
    const body = await page.textContent('body');
    console.log(`Body: ${body}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
} finally {
    await browser.close();
}
