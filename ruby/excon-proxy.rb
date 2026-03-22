#!/usr/bin/env ruby
# frozen_string_literal: true

# Excon with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# Pass :proxy with the proxy URL to Excon.get / Excon.new (see Excon docs).
#
# Documentation: https://github.com/excon/excon#proxy-support
require 'bundler/setup'
require 'excon'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

response = Excon.get(test_url, proxy: proxy_url, ssl_verify_peer: true)

puts "Status: #{response.status}"
puts "Body: #{response.body}"
puts "#{response_header}: #{response.headers[response_header]}" if response_header && !response_header.empty?
