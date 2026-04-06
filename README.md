# Proxy Examples

Example code for using proxy servers in different programming languages. Currently we have examples for these languages:

* Python
* JavaScript / Node.js
* Ruby
* PHP

## Python Proxy Examples

**Installation:**

```bash
pip install -r python/requirements.txt
```

`pycurl` needs libcurl and `curl-config` (for example Debian/Ubuntu: `libcurl4-openssl-dev`). The test runner skips `pycurl-*` examples when `pycurl` is not installed, and skips `scrapy-proxy` when `import scrapy` fails (for example a broken `cryptography` / `cffi` install).

**Running Examples:**

```bash
# Required: Set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Optional: Target URL (default: https://api.ipify.org?format=json)
export TEST_URL='https://httpbin.org/ip'

# Optional: Print one response header
export RESPONSE_HEADER='X-ProxyMesh-IP'

# Single example
python python/requests-proxy.py

# All examples as tests
python python/run_tests.py

# Specific examples (substring match, like the JS runner)
python python/run_tests.py requests httpx
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [requests](https://docs.python-requests.org/) | [requests-proxy.py](python/requests-proxy.py) | Basic `GET` with `proxies=` |
| [requests](https://docs.python-requests.org/) | [requests-session-proxy.py](python/requests-session-proxy.py) | Session with pooled connections |
| [urllib3](https://urllib3.readthedocs.io/) | [urllib3-proxy.py](python/urllib3-proxy.py) | `ProxyManager` |
| [aiohttp](https://docs.aiohttp.org/) | [aiohttp-proxy.py](python/aiohttp-proxy.py) | Async client, `proxy=` on the request |
| [httpx](https://www.python-httpx.org/) | [httpx-proxy.py](python/httpx-proxy.py) | Sync client, `proxy=` on the client |
| [httpx](https://www.python-httpx.org/) | [httpx-async-proxy.py](python/httpx-async-proxy.py) | Async client |
| [pycurl](http://pycurl.io/) | [pycurl-proxy.py](python/pycurl-proxy.py) | libcurl via `setopt` (`PROXY`, `WRITEDATA`, etc.) |
| [cloudscraper](https://github.com/VeNoMouS/cloudscraper) | [cloudscraper-proxy.py](python/cloudscraper-proxy.py) | Requests-based scraper with `proxies` |
| [autoscraper](https://github.com/alirezamika/autoscraper) | [autoscraper-proxy.py](python/autoscraper-proxy.py) | Proxied fetch, then `build`/`get_result_similar` on same HTML (`normalize`/`unescape` must match AutoScraper) |
| [Scrapy](https://scrapy.org/) | [scrapy-proxy.py](python/scrapy-proxy.py) | `scrapy runspider` with `meta['proxy']` |

### Other Python scripts

* [requests-random-proxy.py](python/requests-random-proxy.py) - Random proxy rotation

> **Note:** Like the Ruby, JavaScript, and PHP examples here, these scripts use each library's normal proxy options only. Most of them do not send custom headers on the HTTPS `CONNECT` tunnel or surface proxy `CONNECT` response headers. For that, see [python-proxy-headers](https://github.com/proxymesh/python-proxy-headers) or [scrapy-proxy-headers](https://github.com/proxymesh/scrapy-proxy-headers).

## JavaScript / Node.js Proxy Examples

**Installation:**

```bash
cd javascript
npm install
```

**Running Examples:**

```bash
# Required: Set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Run a single example
node javascript/axios-proxy.js

# Run all examples as tests
node javascript/run_tests.js

# Run specific examples
node javascript/run_tests.js axios got
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [axios](https://axios-http.com/) | [axios-proxy.js](javascript/axios-proxy.js) | Popular promise-based HTTP client |
| [node-fetch](https://github.com/node-fetch/node-fetch) | [node-fetch-proxy.js](javascript/node-fetch-proxy.js) | Fetch API for Node.js |
| [got](https://github.com/sindresorhus/got) | [got-proxy.js](javascript/got-proxy.js) | Human-friendly HTTP client |
| [undici](https://undici.nodejs.org/) | [undici-proxy.js](javascript/undici-proxy.js) | Fast HTTP client (powers Node.js fetch) |
| [superagent](https://github.com/ladjs/superagent) | [superagent-proxy.js](javascript/superagent-proxy.js) | Flexible HTTP client |
| [needle](https://github.com/tomas/needle) | [needle-proxy.js](javascript/needle-proxy.js) | Lean HTTP client |
| [puppeteer](https://pptr.dev/) | [puppeteer-proxy.js](javascript/puppeteer-proxy.js) | Headless Chrome automation |
| [playwright](https://playwright.dev/) | [playwright-proxy.js](javascript/playwright-proxy.js) | Browser automation |
| [cheerio](https://cheerio.js.org/) | [cheerio-proxy.js](javascript/cheerio-proxy.js) | HTML parsing with node-fetch |
| [ky](https://github.com/sindresorhus/ky) | [ky-proxy.js](javascript/ky-proxy.js) | Fetch wrapper (node-fetch + agent) |
| [wretch](https://github.com/elbywan/wretch) | [wretch-proxy.js](javascript/wretch-proxy.js) | Fetch wrapper (polyfill) |
| [make-fetch-happen](https://github.com/npm/make-fetch-happen) | [make-fetch-happen-proxy.js](javascript/make-fetch-happen-proxy.js) | npm-style fetch |
| [typed-rest-client](https://github.com/microsoft/typed-rest-client) | [typed-rest-client-proxy.js](javascript/typed-rest-client-proxy.js) | REST client (built-in proxy option) |

> **Note:** None of these libraries currently support sending custom headers to the proxy during HTTPS CONNECT tunneling or reading proxy response headers. See [javascript-proxy-headers](https://github.com/proxymesh/javascript-proxy-headers) for extension modules that add this capability.

## Ruby Proxy Examples

These examples use [Bundler](https://bundler.io/). Install Ruby development headers and libcurl first so native extensions can compile (Debian/Ubuntu: `ruby-dev` and `libcurl4-openssl-dev`; Fedora: `ruby-devel` and `libcurl-devel`).

```bash
cd ruby
bundle install
```

**Running examples:**

```bash
# Required: set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Optional: target URL (default: https://api.ipify.org?format=json)
export TEST_URL='https://httpbin.org/ip'

# Optional: print one response header
export RESPONSE_HEADER='X-ProxyMesh-IP'

# Single example (from ruby/)
bundle exec ruby faraday-proxy.rb

# All examples as tests
bundle exec ruby run_tests.rb

# Specific examples
bundle exec ruby run_tests.rb faraday typhoeus
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [Net::HTTP](https://docs.ruby-lang.org/en/master/Net/HTTP.html) (stdlib) | [net-http-proxy.rb](ruby/net-http-proxy.rb) | Low-level HTTP with proxy (`Net::HTTP.new` + proxy host/port/user/pass) |
| [Faraday](https://lostisland.github.io/faraday/) | [faraday-proxy.rb](ruby/faraday-proxy.rb) | Middleware-style client; `Faraday.new(proxy: url)` |
| [HTTParty](https://github.com/jnunemaker/httparty) | [httparty-proxy.rb](ruby/httparty-proxy.rb) | Simple API; `http_proxyaddr` / `http_proxyport` / credentials |
| [HTTP.rb](https://github.com/httprb/http) | [http-rb-proxy.rb](ruby/http-rb-proxy.rb) | Lightweight DSL; proxy via `HTTP.via(host, port, user, pass)` |
| [RestClient](https://github.com/rest-client/rest-client) | [rest-client-proxy.rb](ruby/rest-client-proxy.rb) | Simple REST API; proxy via `RestClient.proxy = url` |
| [Typhoeus](https://github.com/typhoeus/typhoeus) | [typhoeus-proxy.rb](ruby/typhoeus-proxy.rb) | libcurl via Ethon; `proxy:` URL on the request |
| [Excon](https://github.com/excon/excon) | [excon-proxy.rb](ruby/excon-proxy.rb) | Fast client; `Excon.get(url, proxy: url)` |
| [HTTPClient](https://github.com/nahi/httpclient) | [httpclient-proxy.rb](ruby/httpclient-proxy.rb) | LWP-like client; pass full proxy URL to `HTTPClient.new` |
| [Mechanize](https://github.com/sparklemotion/mechanize) | [mechanize-proxy.rb](ruby/mechanize-proxy.rb) | Crawling / forms; `set_proxy(host, port, user, password)` |
| [Nokogiri](https://nokogiri.org/) | [nokogiri-proxy.rb](ruby/nokogiri-proxy.rb) | Parse HTML after a proxied `Net::HTTP` fetch |

Libraries above are actively maintained on RubyGems (releases within the last year as of early 2026). Like most high-level Ruby HTTP clients, they do not expose custom headers on the HTTPS `CONNECT` tunnel to the proxy or proxy response headers; for ProxyMesh-style custom proxy headers, lower-level clients or a dedicated helper library may be required.

## PHP Proxy Examples

**Installation:**

```bash
cd php
composer install
```

**Running Examples:**

```bash
# Required: Set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Run a single example
php php/guzzle_proxy.php

# Run all examples as tests
php php/run_tests.php
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [cURL](https://www.php.net/manual/en/book.curl.php) | [curl_proxy.php](php/curl_proxy.php) | PHP's built-in HTTP client (libcurl) |
| [Guzzle](https://docs.guzzlephp.org/) | [guzzle_proxy.php](php/guzzle_proxy.php) | Most popular PHP HTTP client |
| [Symfony HttpClient](https://symfony.com/doc/current/http_client.html) | [symfony_http_client_proxy.php](php/symfony_http_client_proxy.php) | Modern PSR-18 HTTP client |
| [Buzz](https://github.com/kriswallsmith/Buzz) | [buzz_proxy.php](php/buzz_proxy.php) | Simple PSR-18 HTTP client |
| [PHP Streams](https://www.php.net/manual/en/book.stream.php) | [streams_proxy.php](php/streams_proxy.php) | Built-in PHP streams (file_get_contents) |
| [Amp HTTP](https://amphp.org/http-client) | [amphp_proxy.php](php/amphp_proxy.php) | Async HTTP client |

> **Note:** See [php-proxy-headers](https://github.com/proxymeshai/php-proxy-headers) for extensions that add custom proxy header support.

These examples use [Bundler](https://bundler.io/). Install Ruby development headers and libcurl first so native extensions can compile (Debian/Ubuntu: `ruby-dev` and `libcurl4-openssl-dev`; Fedora: `ruby-devel` and `libcurl-devel`).

```bash
cd ruby
bundle install
```

**Running examples:**

```bash
# Required: set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Optional: target URL (default: https://api.ipify.org?format=json)
export TEST_URL='https://httpbin.org/ip'

# Optional: print one response header
export RESPONSE_HEADER='X-ProxyMesh-IP'

# Single example (from ruby/)
bundle exec ruby faraday-proxy.rb

# All examples as tests
bundle exec ruby run_tests.rb

# Specific examples
bundle exec ruby run_tests.rb faraday typhoeus
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [Net::HTTP](https://docs.ruby-lang.org/en/master/Net/HTTP.html) (stdlib) | [net-http-proxy.rb](ruby/net-http-proxy.rb) | Low-level HTTP with proxy (`Net::HTTP.new` + proxy host/port/user/pass) |
| [Faraday](https://lostisland.github.io/faraday/) | [faraday-proxy.rb](ruby/faraday-proxy.rb) | Middleware-style client; `Faraday.new(proxy: url)` |
| [HTTParty](https://github.com/jnunemaker/httparty) | [httparty-proxy.rb](ruby/httparty-proxy.rb) | Simple API; `http_proxyaddr` / `http_proxyport` / credentials |
| [HTTP.rb](https://github.com/httprb/http) | [http-rb-proxy.rb](ruby/http-rb-proxy.rb) | Lightweight DSL; proxy via `HTTP.via(host, port, user, pass)` |
| [RestClient](https://github.com/rest-client/rest-client) | [rest-client-proxy.rb](ruby/rest-client-proxy.rb) | Simple REST API; proxy via `RestClient.proxy = url` |
| [Typhoeus](https://github.com/typhoeus/typhoeus) | [typhoeus-proxy.rb](ruby/typhoeus-proxy.rb) | libcurl via Ethon; `proxy:` URL on the request |
| [Excon](https://github.com/excon/excon) | [excon-proxy.rb](ruby/excon-proxy.rb) | Fast client; `Excon.get(url, proxy: url)` |
| [HTTPClient](https://github.com/nahi/httpclient) | [httpclient-proxy.rb](ruby/httpclient-proxy.rb) | LWP-like client; pass full proxy URL to `HTTPClient.new` |
| [Mechanize](https://github.com/sparklemotion/mechanize) | [mechanize-proxy.rb](ruby/mechanize-proxy.rb) | Crawling / forms; `set_proxy(host, port, user, password)` |
| [Nokogiri](https://nokogiri.org/) | [nokogiri-proxy.rb](ruby/nokogiri-proxy.rb) | Parse HTML after a proxied `Net::HTTP` fetch |

Libraries above are actively maintained on RubyGems (releases within the last year as of early 2026). Like most high-level Ruby HTTP clients, they do not expose custom headers on the HTTPS `CONNECT` tunnel to the proxy or proxy response headers; for ProxyMesh-style custom proxy headers, lower-level clients or a dedicated helper library may be required.

## Related Documentation

More examples and language-specific proxy-header tooling:

### Python

* [python-proxy-headers on PyPI](https://pypi.org/project/python-proxy-headers/)
* [python-proxy-headers Documentation](https://python-proxy-headers.readthedocs.io/)
* [python-proxy-headers GitHub](https://github.com/proxymesh/python-proxy-headers)

### JavaScript / Node.js

* [javascript-proxy-headers GitHub](https://github.com/proxymesh/javascript-proxy-headers)
* [javascript-proxy-headers on npm](https://www.npmjs.com/package/javascript-proxy-headers)
* [javascript-proxy-headers on JSR](https://jsr.io/@proxymesh/javascript-proxy-headers)

### Ruby

* Ruby examples in this repository: [ruby/](ruby/)

## Contributing

Contributions are welcome for all supported languages in this repository (Python, JavaScript, Ruby, and PHP), as well as new language examples.

When opening a Pull Request:

* Follow the existing file naming and environment variable patterns (`PROXY_URL`, `TEST_URL`, and optional response/proxy header variables).
* Include runnable examples and update the language section in this README.
* Add or update the language test runner (`run_tests`) where applicable.
