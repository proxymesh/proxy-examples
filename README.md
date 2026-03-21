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

The `javascript-proxy-headers` dependency is currently resolved from GitHub (`feature/tier-a-proxy-extensions`) so the examples can use the v0.2.0 subpath exports before they appear on npm. After `javascript-proxy-headers@0.2.0` is published, `package.json` can be switched to `"javascript-proxy-headers": "^0.2.0"`.

**Running Examples:**

```bash
cd javascript
npm install

# Required: Set your proxy URL
export PROXY_URL='http://user:pass@proxy.example.com:8080'

# Optional: custom CONNECT headers and a proxy response header to print (ProxyMesh-style)
export PROXY_HEADER='X-ProxyMesh-Country'
export PROXY_VALUE='US'
export RESPONSE_HEADER='X-ProxyMesh-IP'

# Run a single example
node axios-proxy.js

# Run all examples as tests
node run_tests.js

# Run specific examples (substring match on filename)
node run_tests.js axios ky-proxy-headers
```

**Examples (basic proxy tunnel):**

| Library | Example | Description |
|---------|---------|-------------|
| [axios](https://axios-http.com/) | [axios-proxy.js](javascript/axios-proxy.js) | Popular promise-based HTTP client |
| [node-fetch](https://github.com/node-fetch/node-fetch) | [node-fetch-proxy.js](javascript/node-fetch-proxy.js) | Fetch API for Node.js |
| [got](https://github.com/sindresorhus/got) | [got-proxy.js](javascript/got-proxy.js) | Human-friendly HTTP client |
| [undici](https://undici.nodejs.org/) | [undici-proxy.js](javascript/undici-proxy.js) | Fast HTTP client (powers Node.js fetch) |
| [superagent](https://github.com/ladjs/superagent) | [superagent-proxy.js](javascript/superagent-proxy.js) | Flexible HTTP client |
| [needle](https://github.com/tomas/needle) | [needle-proxy.js](javascript/needle-proxy.js) | Lean HTTP client (`https-proxy-agent`) |
| [puppeteer](https://pptr.dev/) | [puppeteer-proxy.js](javascript/puppeteer-proxy.js) | Headless Chrome automation |
| [playwright](https://playwright.dev/) | [playwright-proxy.js](javascript/playwright-proxy.js) | Browser automation |
| [cheerio](https://cheerio.js.org/) | [cheerio-proxy.js](javascript/cheerio-proxy.js) | HTML parsing with node-fetch |

> **Note:** The examples above use a standard HTTPS proxy agent. They do not send custom headers on the CONNECT request or surface the proxy’s CONNECT response headers. For that, use **[javascript-proxy-headers](https://github.com/proxymesh/javascript-proxy-headers)** and the `*-proxy-headers.js` examples below.

**Examples ([javascript-proxy-headers](https://github.com/proxymesh/javascript-proxy-headers)) — custom CONNECT headers:**

| Library | Example | Description |
|---------|---------|-------------|
| [ky](https://github.com/sindresorhus/ky) | [ky-proxy-headers.js](javascript/ky-proxy-headers.js) | Fetch wrapper with custom `fetch` |
| [wretch](https://github.com/elbywan/wretch) | [wretch-proxy-headers.js](javascript/wretch-proxy-headers.js) | Fetch wrapper + polyfill |
| [make-fetch-happen](https://github.com/npm/make-fetch-happen) | [make-fetch-happen-proxy-headers.js](javascript/make-fetch-happen-proxy-headers.js) | npm-style fetch with `agent` |
| [needle](https://github.com/tomas/needle) | [needle-proxy-headers.js](javascript/needle-proxy-headers.js) | Same client as `needle-proxy.js`, with CONNECT headers |
| [typed-rest-client](https://github.com/microsoft/typed-rest-client) | [typed-rest-client-proxy-headers.js](javascript/typed-rest-client-proxy-headers.js) | Azure/DevOps-style REST client |

## Ruby Proxy Examples

* [requests_proxy.rb](ruby/requests_proxy.rb) - Ruby HTTP with proxy, from [rpolley](https://github.com/rpolley)

## Documentation

For more information on using proxy headers with Python:

* [python-proxy-headers on PyPI](https://pypi.org/project/python-proxy-headers/)
* [python-proxy-headers Documentation](https://python-proxy-headers.readthedocs.io/)
* [GitHub Repository](https://github.com/proxymesh/python-proxy-headers)

## Contributing

If you have example code for another language, please share it with a Pull Request.
