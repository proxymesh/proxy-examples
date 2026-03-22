#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTPClient with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# Set the proxy on the client with HTTPClient#proxy= (full URL with optional userinfo).
#
# Documentation: https://www.rubydoc.info/gems/httpclient/HTTPClient
require 'bundler/setup'
require 'httpclient'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

client = HTTPClient.new
client.proxy = proxy_url

response = client.get(test_url)
body = response.body.respond_to?(:content) ? response.body.content : response.body.to_s

status = response.status
status_code = status.respond_to?(:code) ? status.code : status
puts "Status: #{status_code}"
puts "Body: #{body}"
if response_header && !response_header.empty?
  h = response.headers[response_header] || response.headers[response_header.downcase]
  puts "#{response_header}: #{h}"
end
