#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTPClient with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#
# HTTPClient provides LWP-like functionality. It has advanced proxy support
# but does NOT expose custom CONNECT headers or proxy response headers.

require 'httpclient'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

begin
  client = HTTPClient.new(proxy_url)
  response = client.get(test_url)

  puts "Status: #{response.status}"
  puts "Body: #{response.body}"
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
