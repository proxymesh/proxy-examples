#!/usr/bin/env ruby
# frozen_string_literal: true

# Excon with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#
# Excon is a fast, simple HTTP(S) client. It supports proxies but does NOT
# support sending custom headers during HTTPS CONNECT or reading proxy response headers.

require 'excon'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

begin
  response = Excon.get(test_url, proxy: proxy_url)

  puts "Status: #{response.status}"
  puts "Body: #{response.body}"
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
