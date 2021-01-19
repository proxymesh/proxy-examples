require 'net/http'
require 'uri'

uri = URI('http://example.com')
proxy_uri = URI('http://host:port')
proxy_options = {
  p_addr: proxy_options.host,
  p_port: proxy_options.port,
  # username/password are optional if you have IP authentication
  p_user: 'USERNAME',
  p_pass: 'PASSWORD',
}

Net::HTTP.start(uri.host, uri.port, **proxy_options) do |http|
  response = http.get('/')
end