#!/usr/bin/env ruby
# frozen_string_literal: true

# RestClient with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# RestClient supports proxy via RestClient.proxy or HTTP(S)_PROXY env vars.
#
# Documentation: https://github.com/rest-client/rest-client
require 'bundler/setup'
require 'rest-client'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

RestClient.proxy = proxy_url
response = RestClient.get(test_url)

puts "Status: #{response.code}"
puts "Body: #{response.body}"
puts "#{response_header}: #{response.headers[response_header.downcase.to_sym]}" if response_header && !response_header.empty?
