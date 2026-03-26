#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTParty with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# Set http_proxyaddr, http_proxyport, and optional http_proxyuser / http_proxypass
# (see HTTParty::ClassMethods).
#
# Documentation: https://www.rubydoc.info/gems/httparty/HTTParty/ClassMethods
require 'bundler/setup'
require 'httparty'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

proxy = URI.parse(proxy_url)

response = HTTParty.get(
  test_url,
  http_proxyaddr: proxy.host,
  http_proxyport: proxy.port,
  http_proxyuser: proxy.user,
  http_proxypass: proxy.password
)

puts "Status: #{response.code}"
puts "Body: #{response.body}"
if response_header && !response_header.empty?
  h = response.headers[response_header] || response.headers[response_header.downcase]
  puts "#{response_header}: #{h}"
end
