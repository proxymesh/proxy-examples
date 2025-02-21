# See https://github.com/proxymesh/python-proxy-headers
from python_proxy_headers import requests_adapter

proxies = {
	# USERNAME:PASSWORD is optional if you have IP authentication
	'http': 'http://USERNAME:PASSWORD@HOST:PORT',
	'https': 'http://USERNAME:PASSWORD@HOST:PORT'
}

r = requests_adapter.get('https://api.ipify.org?format=json',
						 proxies=proxies,
						 proxy_headers={'X-ProxyMesh-Country': 'US'})

r.headers['X-ProxyMesh-IP']