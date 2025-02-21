import httpx
# See https://github.com/proxymesh/python-proxy-headers
from python_proxy_headers import httpx_proxy

proxy = httpx.Proxy('http://PROXYHOST:PORT', headers={'X-ProxyMesh-Country': 'US'})
r = httpx_proxy.get('https://api.ipify.org?format=json', proxy=proxy)
r.headers['X-ProxyMesh-IP']