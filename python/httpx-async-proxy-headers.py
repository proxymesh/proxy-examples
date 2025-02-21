import httpx
# See https://github.com/proxymesh/python-proxy-headers
from python_proxy_headers.httpx_proxy import AsyncHTTPProxyTransport

proxy = httpx.Proxy('http://PROXYHOST:PORT', headers={'X-ProxyMesh-Country': 'US'})
transport = AsyncHTTPProxyTransport(proxy=proxy)

async with httpx.AsyncClient(mounts={'http://': transport, 'https://': transport}) as client:
	r = await client.get('https://api.ipify.org?format=json')

r.headers['X-ProxyMesh-IP']