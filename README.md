# Proxy Examples

Example code for using proxy servers in different programming languages. Currently we have examples for these languages:

* Python
* Ruby

## Python Proxy Examples

### Using python-proxy-headers

The [python-proxy-headers](https://github.com/proxymesh/python-proxy-headers) library enables sending custom headers to proxy servers and receiving proxy response headers. This is essential for services like [ProxyMesh](https://proxymesh.com) that use custom headers for country selection and IP assignment.

**Installation:**

```bash
pip install python-proxy-headers
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

## Ruby Proxy Examples

* [requests_proxy.rb](ruby/requests_proxy.rb) - Ruby HTTP with proxy, from [rpolley](https://github.com/rpolley)

## Documentation

For more information on using proxy headers with Python:

* [python-proxy-headers on PyPI](https://pypi.org/project/python-proxy-headers/)
* [python-proxy-headers Documentation](https://python-proxy-headers.readthedocs.io/)
* [GitHub Repository](https://github.com/proxymesh/python-proxy-headers)

## Contributing

If you have example code for another language, please share it with a Pull Request.
