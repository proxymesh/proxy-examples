# See https://github.com/proxymesh/python-proxy-headers
from python_proxy_headers import urllib3_proxy_manager

proxy = urllib3_proxy_manager.ProxyHeaderManager('http://PROXYHOST:PORT', proxy_headers={'X-ProxyMesh-Country': 'US'})
r = proxy.request('GET', 'https://api.ipify.org?format=json')
r.headers['X-ProxyMesh-IP']