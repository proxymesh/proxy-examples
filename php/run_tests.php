#!/usr/bin/env php
<?php
/**
 * Run all PHP proxy examples as tests.
 *
 * Configuration via environment variables:
 *   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
 *   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
 *   PROXY_HEADER    - Header name to check in response (optional)
 *   PROXY_VALUE     - Header value to send to proxy (optional)
 *
 * Usage:
 *   php run_tests.php              # Run all examples
 *   php run_tests.php guzzle       # Run specific example
 *   php run_tests.php -l           # List available examples
 *   php run_tests.php -v           # Verbose output
 */

define('EXAMPLES', [
    'curl_proxy.php' => 'cURL',
    'guzzle_proxy.php' => 'Guzzle',
    'symfony_http_client_proxy.php' => 'Symfony HttpClient',
    'buzz_proxy.php' => 'Buzz',
    'streams_proxy.php' => 'PHP Streams',
    'amphp_proxy.php' => 'Amp HTTP',
]);

function parseArgs(array $argv): array {
    $options = [
        'verbose' => false,
        'list' => false,
        'help' => false,
        'examples' => [],
    ];

    foreach (array_slice($argv, 1) as $arg) {
        switch ($arg) {
            case '-v':
            case '--verbose':
                $options['verbose'] = true;
                break;
            case '-l':
            case '--list':
                $options['list'] = true;
                break;
            case '-h':
            case '--help':
                $options['help'] = true;
                break;
            default:
                if (!str_starts_with($arg, '-')) {
                    $options['examples'][] = $arg;
                }
        }
    }

    return $options;
}

function showHelp(): void {
    echo <<<HELP
Run all PHP proxy examples as tests.

Usage:
  php run_tests.php [options] [example1] [example2] ...

Options:
  -v, --verbose    Show full output from each example
  -l, --list       List available examples
  -h, --help       Show this help message

Environment Variables:
  PROXY_URL        Proxy URL (required), e.g., http://user:pass@proxy:8080
  TEST_URL         URL to request (default: https://api.ipify.org?format=json)
  PROXY_HEADER     Header name to check in response (optional)
  PROXY_VALUE      Header value to send to proxy (optional)

Examples:
  PROXY_URL='http://proxy:8080' php run_tests.php
  php run_tests.php guzzle symfony

HELP;
}

function listExamples(): void {
    echo "Available examples:\n";
    foreach (EXAMPLES as $file => $name) {
        $key = str_replace('_proxy.php', '', $file);
        printf("  %-25s %s\n", $key, $name);
    }
}

function maskPassword(string $url): string {
    return preg_replace('/:[^:@]+@/', ':****@', $url);
}

function runExample(string $file, bool $verbose): array {
    $scriptDir = __DIR__;
    $scriptPath = "{$scriptDir}/{$file}";

    if (!file_exists($scriptPath)) {
        return ['success' => false, 'error' => "Script not found: {$scriptPath}"];
    }

    $output = [];
    $returnCode = 0;
    exec("php {$scriptPath} 2>&1", $output, $returnCode);
    $outputStr = implode("\n", $output);

    if ($verbose) {
        echo $outputStr . "\n";
    }

    return [
        'success' => $returnCode === 0,
        'output' => $outputStr,
    ];
}

function main(array $argv): int {
    $options = parseArgs($argv);

    if ($options['help']) {
        showHelp();
        return 0;
    }

    if ($options['list']) {
        listExamples();
        return 0;
    }

    $proxyUrl = getenv('PROXY_URL') ?: getenv('HTTPS_PROXY');
    if (!$proxyUrl) {
        fwrite(STDERR, "Error: Set PROXY_URL environment variable\n");
        fwrite(STDERR, "\nExample:\n");
        fwrite(STDERR, "  export PROXY_URL='http://user:pass@proxy:8080'\n");
        return 1;
    }

    $examplesToRun = EXAMPLES;
    if (!empty($options['examples'])) {
        $examplesToRun = array_filter(EXAMPLES, function($file) use ($options) {
            foreach ($options['examples'] as $arg) {
                if (str_contains($file, $arg)) {
                    return true;
                }
            }
            return false;
        }, ARRAY_FILTER_USE_KEY);
    }

    $testUrl = getenv('TEST_URL') ?: 'https://api.ipify.org?format=json';

    echo str_repeat('=', 60) . "\n";
    echo "PHP Proxy Examples - Test Runner\n";
    echo str_repeat('=', 60) . "\n";
    echo "Proxy URL:       " . maskPassword($proxyUrl) . "\n";
    echo "Test URL:        {$testUrl}\n";
    echo "Examples:        " . count($examplesToRun) . "\n";
    echo str_repeat('=', 60) . "\n\n";

    $passed = 0;
    $failed = 0;

    foreach ($examplesToRun as $file => $name) {
        echo "Testing {$name}... ";

        $result = runExample($file, $options['verbose']);

        if ($result['success']) {
            echo "OK\n";
            $passed++;
        } else {
            echo "FAILED\n";
            if (!$options['verbose']) {
                $errorLine = explode("\n", $result['output'])[0] ?? '';
                if ($errorLine) {
                    echo "  Error: {$errorLine}\n";
                }
            }
            $failed++;
        }
    }

    echo "\n" . str_repeat('=', 60) . "\n";
    echo "Results: {$passed} passed, {$failed} failed\n";
    echo str_repeat('=', 60) . "\n";

    return $failed > 0 ? 1 : 0;
}

exit(main($argv));
