#!/usr/bin/env ruby
# frozen_string_literal: true

# Net::HTTP (stdlib) with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# Net::HTTP routes HTTPS traffic through the proxy using CONNECT. Extra headers on
# CONNECT are not exposed in the high-level API; see ProxyMesh docs for advanced cases.
#
# Documentation: https://docs.ruby-lang.org/en/master/Net/HTTP.html
require 'net/http'
require 'openssl'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

uri = URI.parse(test_url)
proxy = URI.parse(proxy_url)

http = Net::HTTP.new(
  uri.host,
  uri.port,
  proxy.host,
  proxy.port,
  proxy.user,
  proxy.password
)

if uri.scheme == 'https'
  http.use_ssl = true
  http.verify_mode = OpenSSL::SSL::VERIFY_PEER
end

request = Net::HTTP::Get.new(uri)
response = http.request(request)

puts "Status: #{response.code}"
puts "Body: #{response.body}"
puts "#{response_header}: #{response[response_header]}" if response_header && !response_header.empty?
