#!/usr/bin/env node
/**
 * Puppeteer with proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *
 * Note: Puppeteer delegates proxy handling to the browser (Chromium).
 * Custom proxy headers during HTTPS CONNECT are not supported as the browser
 * handles the tunneling internally.
 */
import puppeteer from 'puppeteer';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';

const url = new URL(proxyUrl);
const proxyServer = `${url.protocol}//${url.hostname}:${url.port}`;
const username = url.username;
const password = url.password;

const browser = await puppeteer.launch({
    args: [`--proxy-server=${proxyServer}`],
    headless: true,
});

try {
    const page = await browser.newPage();

    if (username && password) {
        await page.authenticate({ username, password });
    }

    const response = await page.goto(testUrl, { waitUntil: 'networkidle0' });

    console.log(`Status: ${response.status()}`);
    const body = await page.evaluate(() => document.body.innerText);
    console.log(`Body: ${body}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
} finally {
    await browser.close();
}
