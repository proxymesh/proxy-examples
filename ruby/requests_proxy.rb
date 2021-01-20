require 'net/http'
require 'uri'

uri = URI('http://example.com')
proxy_options = {
  p_addr: 'PROXYHOST',
  p_port: PORT,
  # username/password are optional if you have IP authentication
  p_user: 'USERNAME',
  p_pass: 'PASSWORD',
}

Net::HTTP.start(uri.host, uri.port, **proxy_options) do |http|
  request = Net::HTTP::Get.new uri
  response = http.request request
end
