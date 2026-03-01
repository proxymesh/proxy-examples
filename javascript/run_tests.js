#!/usr/bin/env node
/**
 * Run all JavaScript proxy examples as tests.
 *
 * Configuration via environment variables:
 *     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *     PROXY_HEADER    - Header name to send to proxy (optional)
 *     PROXY_VALUE     - Header value to send to proxy (optional)
 *     RESPONSE_HEADER - Header name to read from response (optional)
 *
 * Usage:
 *     node run_tests.js              # Run all examples
 *     node run_tests.js axios        # Run specific example
 *     node run_tests.js -l           # List available examples
 *     node run_tests.js -v           # Verbose output
 */
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));

const EXAMPLES = [
    'axios-proxy.js',
    'node-fetch-proxy.js',
    'got-proxy.js',
    'undici-proxy.js',
    'superagent-proxy.js',
    'needle-proxy.js',
    'cheerio-proxy.js',
];

const BROWSER_EXAMPLES = [
    'puppeteer-proxy.js',
    'playwright-proxy.js',
];

function parseArgs() {
    const args = process.argv.slice(2);
    const options = {
        verbose: false,
        list: false,
        help: false,
        includeBrowser: false,
        examples: [],
    };

    for (const arg of args) {
        if (arg === '-v' || arg === '--verbose') {
            options.verbose = true;
        } else if (arg === '-l' || arg === '--list') {
            options.list = true;
        } else if (arg === '-h' || arg === '--help') {
            options.help = true;
        } else if (arg === '-b' || arg === '--browser') {
            options.includeBrowser = true;
        } else if (!arg.startsWith('-')) {
            options.examples.push(arg);
        }
    }

    return options;
}

function showHelp() {
    console.log(`
Run all JavaScript proxy examples as tests.

Usage:
    node run_tests.js [options] [example1] [example2] ...

Options:
    -v, --verbose    Show full output from each example
    -l, --list       List available examples
    -b, --browser    Include browser examples (puppeteer, playwright)
    -h, --help       Show this help message

Environment Variables:
    PROXY_URL        Proxy URL (required), e.g., http://user:pass@proxy:8080
    TEST_URL         URL to request (default: https://api.ipify.org?format=json)
    PROXY_HEADER     Header name to send to proxy (optional)
    PROXY_VALUE      Header value to send to proxy (optional)
    RESPONSE_HEADER  Header name to read from response (optional)

Examples:
    # Run all examples
    PROXY_URL='http://proxy:8080' node run_tests.js

    # Run specific examples
    node run_tests.js axios got

    # Include browser examples
    node run_tests.js -b
`);
}

function listExamples() {
    console.log('Available examples:');
    console.log('\nHTTP Libraries:');
    for (const example of EXAMPLES) {
        console.log(`  ${example.replace('.js', '')}`);
    }
    console.log('\nBrowser Automation (use -b flag):');
    for (const example of BROWSER_EXAMPLES) {
        console.log(`  ${example.replace('.js', '')}`);
    }
}

function maskPassword(url) {
    try {
        const parsed = new URL(url);
        if (parsed.password) {
            return url.replace(`:${parsed.password}@`, ':****@');
        }
        return url;
    } catch {
        return url;
    }
}

async function runExample(name, verbose) {
    const file = join(__dirname, name);

    return new Promise((resolve) => {
        const proc = spawn('node', [file], {
            env: process.env,
            stdio: verbose ? 'inherit' : 'pipe',
        });

        let stdout = '';
        let stderr = '';

        if (!verbose) {
            proc.stdout?.on('data', (data) => { stdout += data; });
            proc.stderr?.on('data', (data) => { stderr += data; });
        }

        proc.on('close', (code) => {
            resolve({
                success: code === 0,
                code,
                stdout,
                stderr,
            });
        });

        proc.on('error', (err) => {
            resolve({
                success: false,
                code: -1,
                stdout: '',
                stderr: err.message,
            });
        });
    });
}

async function main() {
    const options = parseArgs();

    if (options.help) {
        showHelp();
        process.exit(0);
    }

    if (options.list) {
        listExamples();
        process.exit(0);
    }

    const proxyUrl = process.env.PROXY_URL || process.env.HTTPS_PROXY;
    if (!proxyUrl) {
        console.error('Error: Set PROXY_URL environment variable');
        console.error('\nExample:');
        console.error("  export PROXY_URL='http://user:pass@proxy:8080'");
        process.exit(1);
    }

    let examplesToRun = [...EXAMPLES];
    if (options.includeBrowser) {
        examplesToRun = [...EXAMPLES, ...BROWSER_EXAMPLES];
    }

    if (options.examples.length > 0) {
        examplesToRun = examplesToRun.filter(e =>
            options.examples.some(arg => e.includes(arg))
        );
    }

    const testUrl = process.env.TEST_URL || 'https://api.ipify.org?format=json';
    const proxyHeader = process.env.PROXY_HEADER;
    const proxyValue = process.env.PROXY_VALUE;

    console.log('='.repeat(60));
    console.log('JavaScript Proxy Examples - Test Runner');
    console.log('='.repeat(60));
    console.log(`Proxy URL:       ${maskPassword(proxyUrl)}`);
    console.log(`Test URL:        ${testUrl}`);
    if (proxyHeader && proxyValue) {
        console.log(`Send Header:     ${proxyHeader}: ${proxyValue}`);
    }
    console.log(`Examples:        ${examplesToRun.length}`);
    console.log('='.repeat(60));
    console.log();

    let passed = 0;
    let failed = 0;

    for (const example of examplesToRun) {
        const name = example.replace('.js', '');
        process.stdout.write(`Testing ${name}... `);

        const result = await runExample(example, options.verbose);

        if (result.success) {
            console.log('OK');
            passed++;
        } else {
            console.log('FAILED');
            if (!options.verbose && result.stderr) {
                console.log(`  Error: ${result.stderr.trim().split('\n')[0]}`);
            }
            failed++;
        }
    }

    console.log();
    console.log('='.repeat(60));
    console.log(`Results: ${passed} passed, ${failed} failed`);
    console.log('='.repeat(60));

    process.exit(failed > 0 ? 1 : 0);
}

main().catch(err => {
    console.error('Unexpected error:', err);
    process.exit(1);
});
