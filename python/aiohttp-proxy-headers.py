# See https://github.com/proxymesh/python-proxy-headers
from python_proxy_headers import aiohttp_proxy

async with aiohttp_proxy.ProxyClientSession() as session:
	async with session.get('https://api.ipify.org?format=json', proxy="http://PROXYHOST:PORT", proxy_headers={'X-ProxyMesh-Country': 'US'}) as r:
		await r.text()

r.headers['X-ProxyMesh-IP']