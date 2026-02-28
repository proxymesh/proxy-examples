#!/usr/bin/env node
/**
 * Test runner for JavaScript proxy examples.
 *
 * Usage:
 *     export PROXY_URL='http://user:pass@proxy:8080'
 *     node run_tests.js              # Run all tests
 *     node run_tests.js axios got    # Run specific tests
 */
import { spawn } from 'child_process';
import { readdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const examples = [
    'axios-proxy.js',
    'node-fetch-proxy.js',
    'got-proxy.js',
    'undici-proxy.js',
    'superagent-proxy.js',
    'needle-proxy.js',
    'cheerio-proxy.js',
    // Browser examples require more setup, skip by default
    // 'puppeteer-proxy.js',
    // 'playwright-proxy.js',
];

const args = process.argv.slice(2);
const toRun = args.length > 0
    ? examples.filter(e => args.some(a => e.includes(a)))
    : examples;

if (!process.env.PROXY_URL && !process.env.HTTPS_PROXY) {
    console.error('Error: Set PROXY_URL environment variable');
    process.exit(1);
}

console.log(`Running ${toRun.length} example(s)...\n`);

let passed = 0;
let failed = 0;

for (const example of toRun) {
    const file = join(__dirname, example);
    console.log(`--- ${example} ---`);

    try {
        await new Promise((resolve, reject) => {
            const proc = spawn('node', [file], {
                stdio: 'inherit',
                env: process.env,
            });
            proc.on('close', code => {
                if (code === 0) resolve();
                else reject(new Error(`Exit code: ${code}`));
            });
            proc.on('error', reject);
        });
        console.log(`✓ PASSED\n`);
        passed++;
    } catch (error) {
        console.log(`✗ FAILED: ${error.message}\n`);
        failed++;
    }
}

console.log(`\nResults: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
