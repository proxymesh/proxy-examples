#!/usr/bin/env ruby
# frozen_string_literal: true

# Typhoeus (libcurl) with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# Pass the full proxy URL as the :proxy option on Typhoeus::Request (Ethon / libcurl).
#
# Documentation: https://github.com/typhoeus/typhoeus#proxies
require 'bundler/setup'
require 'typhoeus'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

request = Typhoeus::Request.new(
  test_url,
  proxy: proxy_url,
  ssl_verifypeer: true,
  ssl_verifyhost: 2
)

response = request.run

puts "Status: #{response.code}"
puts "Body: #{response.body}"
if response_header && !response_header.empty?
  puts "#{response_header}: #{response.headers[response_header] || response.headers[response_header.downcase]}"
end
