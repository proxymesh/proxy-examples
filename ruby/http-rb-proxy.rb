#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTP.rb (http gem) with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# HTTP.rb supports proxies through HTTP.via(host, port, user, pass).
#
# Documentation: https://github.com/httprb/http
require 'bundler/setup'
require 'http'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

proxy = URI.parse(proxy_url)
response = HTTP.via(proxy.host, proxy.port, proxy.user, proxy.password).get(test_url)

puts "Status: #{response.status}"
puts "Body: #{response.to_s}"
puts "#{response_header}: #{response.headers[response_header]}" if response_header && !response_header.empty?
