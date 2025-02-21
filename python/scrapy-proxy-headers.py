# See https://github.com/proxymesh/scrapy-proxy-headers

# In your Scrapy `settings.py`, add the following:
DOWNLOAD_HANDLERS = {
  "https": "scrapy_proxy_headers.HTTP11ProxyDownloadHandler"
}

# add to your request procesing method
request.meta["proxy_headers"] = {"X-ProxyMesh-Country": "US"}

# then when you get a response
response.headers["X-ProxyMesh-IP"]