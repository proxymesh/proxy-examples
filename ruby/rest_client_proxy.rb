#!/usr/bin/env ruby
# frozen_string_literal: true

# RestClient with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#
# RestClient is a simple REST client. It reads proxy from environment variables
# (HTTP_PROXY/HTTPS_PROXY) or can be set via RestClient.proxy.
# Does NOT support custom CONNECT headers or proxy response headers.

require 'rest-client'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

# Set proxy globally
RestClient.proxy = proxy_url

begin
  response = RestClient.get(test_url)

  puts "Status: #{response.code}"
  puts "Body: #{response.body}"
rescue RestClient::ExceptionWithResponse => e
  warn "HTTP Error: #{e.response.code}"
  exit 1
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
