import requests
proxies = {
	# USERNAME:PASSWORD is optional if you have IP authentication
	'http': 'http://USERNAME:PASSWORD@HOST:PORT',
	'https': 'http://USERNAME:PASSWORD@HOST:PORT'
}
response = requests.get('http://example.com', proxies=proxies)