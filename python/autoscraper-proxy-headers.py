#!/usr/bin/env python3
"""
AutoScraper with proxy headers example.

This example shows how to use AutoScraper with custom proxy headers.
AutoScraper automatically learns scraping rules while python-proxy-headers
enables sending custom headers to the proxy server.

See: https://github.com/proxymesh/python-proxy-headers
Docs: https://python-proxy-headers.readthedocs.io/en/latest/autoscraper.html
"""
from python_proxy_headers.autoscraper_proxy import ProxyAutoScraper

# Create an AutoScraper with proxy header support
scraper = ProxyAutoScraper(proxy_headers={'X-ProxyMesh-Country': 'US'})

# Proxy configuration
proxies = {
    'http': 'http://USERNAME:PASSWORD@PROXYHOST:PORT',
    'https': 'http://USERNAME:PASSWORD@PROXYHOST:PORT'
}

# Build scraping rules from a sample page
# AutoScraper learns what to extract based on the wanted_list
result = scraper.build(
    url='https://quotes.toscrape.com/',
    wanted_list=['The world as we have created it is a process of our thinking.'],
    request_args={'proxies': proxies}
)

print(f"Found {len(result)} matching quotes")
for quote in result[:5]:
    print(f"  - {quote[:60]}...")

# Save learned rules for later use
# scraper.save('quotes_rules.json')

# Use learned rules on another page
# result = scraper.get_result_similar(
#     url='https://quotes.toscrape.com/page/2/',
#     request_args={'proxies': proxies}
# )

scraper.close()
