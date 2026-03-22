# Proxy Examples

Example code for using proxy servers in different programming languages. Currently we have examples for these languages:

* Python
* JavaScript / Node.js
* Ruby

## Python Proxy Examples

### Using python-proxy-headers

The [python-proxy-headers](https://github.com/proxymesh/python-proxy-headers) library enables sending custom headers to proxy servers and receiving proxy response headers. This is essential for services like [ProxyMesh](https://proxymesh.com) that use custom headers for country selection and IP assignment.

**Installation:**

```bash
pip install python-proxy-headers
```

**Running Examples:**

All examples read proxy configuration from environment variables:

```bash
# Required: Set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Optional: Custom test URL (default: https://api.ipify.org?format=json)
export TEST_URL='https://httpbin.org/ip'

# Optional: Send a custom header to the proxy
export PROXY_HEADER='X-ProxyMesh-Country'
export PROXY_VALUE='US'

# Optional: Read a specific header from the response
export RESPONSE_HEADER='X-ProxyMesh-IP'

# Run a single example
python python/requests-proxy-headers.py

# Run all examples as tests
python python/run_tests.py

# Run specific examples
python python/run_tests.py requests-proxy-headers httpx-proxy-headers
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [requests](https://docs.python-requests.org/) | [requests-proxy-headers.py](python/requests-proxy-headers.py) | Simple HTTP requests with proxy headers |
| requests | [requests-proxy-headers-session.py](python/requests-proxy-headers-session.py) | Session-based requests for connection pooling |
| [urllib3](https://urllib3.readthedocs.io/) | [urllib3-proxy-headers.py](python/urllib3-proxy-headers.py) | Low-level HTTP client with proxy headers |
| [aiohttp](https://docs.aiohttp.org/) | [aiohttp-proxy-headers.py](python/aiohttp-proxy-headers.py) | Async HTTP client with proxy headers |
| [httpx](https://www.python-httpx.org/) | [httpx-proxy-headers.py](python/httpx-proxy-headers.py) | Modern HTTP client with proxy headers |
| httpx | [httpx-async-proxy-headers.py](python/httpx-async-proxy-headers.py) | Async httpx with proxy headers |
| [pycurl](http://pycurl.io/) | [pycurl-proxy-headers.py](python/pycurl-proxy-headers.py) | libcurl bindings with proxy headers |
| pycurl | [pycurl-proxy-headers-lowlevel.py](python/pycurl-proxy-headers-lowlevel.py) | Low-level pycurl integration |
| [cloudscraper](https://github.com/venomous/cloudscraper) | [cloudscraper-proxy-headers.py](python/cloudscraper-proxy-headers.py) | Cloudflare bypass with proxy headers |
| [autoscraper](https://github.com/alirezamika/autoscraper) | [autoscraper-proxy-headers.py](python/autoscraper-proxy-headers.py) | Automatic web scraping with proxy headers |

### Basic Proxy Examples

* [requests-proxy.py](python/requests-proxy.py) - Basic proxy usage with requests
* [requests-random-proxy.py](python/requests-random-proxy.py) - Random proxy rotation

### Scrapy

* [scrapy-proxy-headers.py](python/scrapy-proxy-headers.py) - Scrapy spider with proxy headers

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

**Installation:**

These examples use [Bundler](https://bundler.io/). Dependencies are pure Ruby or ship precompiled native gems (for example `ffi`); [Typhoeus](https://github.com/typhoeus/typhoeus) uses Ethon and needs the libcurl shared library at runtime. A normal `bundle install` should not require `ruby-dev` on common Linux x86_64 setups.

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
bundle exec ruby httpclient-proxy.rb

# All examples as tests
bundle exec ruby run_tests.rb

# Specific examples
bundle exec ruby run_tests.rb httpclient typhoeus
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [Net::HTTP](https://docs.ruby-lang.org/en/master/Net/HTTP.html) (stdlib) | [net-http-proxy.rb](ruby/net-http-proxy.rb) | Low-level HTTP with proxy (`Net::HTTP.new` + proxy host/port/user/pass) |
| [HTTPClient](https://github.com/nahi/httpclient) | [httpclient-proxy.rb](ruby/httpclient-proxy.rb) | Full-featured client; `HTTPClient#proxy=` then `get` |
| HTTPClient + stdlib JSON | [httpclient-scrape-proxy.rb](ruby/httpclient-scrape-proxy.rb) | Proxied fetch then parse JSON (scraping-style pipeline; use an HTML parser such as Nokogiri for markup) |
| [HTTParty](https://github.com/jnunemaker/httparty) | [httparty-proxy.rb](ruby/httparty-proxy.rb) | Simple API; `http_proxyaddr` / `http_proxyport` / credentials |
| [Typhoeus](https://github.com/typhoeus/typhoeus) | [typhoeus-proxy.rb](ruby/typhoeus-proxy.rb) | libcurl via Ethon; `proxy:` URL on the request |
| [Excon](https://github.com/excon/excon) | [excon-proxy.rb](ruby/excon-proxy.rb) | Fast client; `Excon.get(url, proxy: url)` |

Libraries above are actively maintained on RubyGems (check RubyGems for current release dates). Like most high-level Ruby HTTP clients, they do not expose custom headers on the HTTPS `CONNECT` tunnel to the proxy or proxy response headers; for ProxyMesh-style custom proxy headers, lower-level clients or a dedicated helper library may be required.

## Documentation

For more information on using proxy headers with Python:

* [python-proxy-headers on PyPI](https://pypi.org/project/python-proxy-headers/)
* [python-proxy-headers Documentation](https://python-proxy-headers.readthedocs.io/)
* [GitHub Repository](https://github.com/proxymesh/python-proxy-headers)

## Contributing

If you have example code for another language, please share it with a Pull Request.
