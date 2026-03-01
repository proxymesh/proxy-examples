#!/usr/bin/env node
/**
 * Cheerio with node-fetch and proxy example.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://example.com)
 *
 * Cheerio is an HTML parser; this example shows how to combine it
 * with node-fetch for web scraping through a proxy.
 *
 * Note: The underlying HTTP client (node-fetch) does not support
 * custom proxy headers during HTTPS CONNECT.
 */
import * as cheerio from 'cheerio';
import fetch from 'node-fetch';
import { HttpsProxyAgent } from 'https-proxy-agent';

const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
if (!proxyUrl) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

const testUrl = process.env.TEST_URL || 'https://example.com';

const agent = new HttpsProxyAgent(proxyUrl);

try {
    const response = await fetch(testUrl, { agent });
    const html = await response.text();

    const $ = cheerio.load(html);
    const title = $('title').text();

    console.log(`Status: ${response.status}`);
    console.log(`Title: ${title}`);
} catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
}
