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

> **Note:** None of these libraries currently support sending custom headers to the proxy during HTTPS CONNECT tunneling or reading proxy response headers. See [javascript-proxy-headers](https://github.com/proxymesh/javascript-proxy-headers) for extension modules that add this capability.

## Ruby Proxy Examples

**Installation:**

```bash
cd ruby
bundle install
```

**Running Examples:**

```bash
# Required: Set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Run a single example
ruby ruby/faraday_proxy.rb

# Run all examples as tests
ruby ruby/run_tests.rb

# Run specific examples
ruby ruby/run_tests.rb faraday httparty
```

**Examples:**

| Library | Example | Description |
|---------|---------|-------------|
| [Net::HTTP](https://ruby-doc.org/stdlib/libdoc/net/http/rdoc/Net/HTTP.html) | [net_http_proxy.rb](ruby/net_http_proxy.rb) | Ruby standard library HTTP client |
| [Faraday](https://lostisland.github.io/faraday/) | [faraday_proxy.rb](ruby/faraday_proxy.rb) | HTTP client with middleware support |
| [HTTParty](https://github.com/jnunemaker/httparty) | [httparty_proxy.rb](ruby/httparty_proxy.rb) | Makes HTTP fun again |
| [RestClient](https://github.com/rest-client/rest-client) | [rest_client_proxy.rb](ruby/rest_client_proxy.rb) | Simple REST client |
| [Typhoeus](https://typhoeus.github.io/) | [typhoeus_proxy.rb](ruby/typhoeus_proxy.rb) | Fast HTTP client (libcurl wrapper) |
| [HTTP.rb](https://github.com/httprb/http) | [http_rb_proxy.rb](ruby/http_rb_proxy.rb) | Simple Ruby DSL for HTTP |
| [Excon](https://github.com/excon/excon) | [excon_proxy.rb](ruby/excon_proxy.rb) | Fast, simple HTTP(S) client |
| [HTTPClient](https://github.com/nahi/httpclient) | [httpclient_proxy.rb](ruby/httpclient_proxy.rb) | LWP-like HTTP client |
| [Mechanize](https://github.com/sparklemotion/mechanize) | [mechanize_proxy.rb](ruby/mechanize_proxy.rb) | Web automation library |

> **Note:** None of these libraries currently support sending custom headers to the proxy during HTTPS CONNECT tunneling or reading proxy response headers. See [ruby-proxy-headers](https://github.com/proxymeshai/ruby-proxy-headers) for extension modules that add this capability.

## Documentation

For more information on using proxy headers with Python:

* [python-proxy-headers on PyPI](https://pypi.org/project/python-proxy-headers/)
* [python-proxy-headers Documentation](https://python-proxy-headers.readthedocs.io/)
* [GitHub Repository](https://github.com/proxymesh/python-proxy-headers)

## Contributing

If you have example code for another language, please share it with a Pull Request.
