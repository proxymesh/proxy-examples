import random
import requests
proxy_choices = ['HOST1:PORT', 'HOST2:PORT']
proxy = random.choice(proxy_choices)
proxies = {
	'http': f'http://{proxy}',
	'https': f'http://{proxy}'
}
response = requests.get('http://example.com', proxies=proxies)