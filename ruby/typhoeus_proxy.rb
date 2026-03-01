#!/usr/bin/env ruby
# frozen_string_literal: true

# Typhoeus with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#
# Typhoeus wraps libcurl for fast HTTP requests. It has the BEST proxy support
# of all Ruby HTTP libraries because libcurl supports CURLOPT_PROXYHEADER.
# However, the Ruby binding does not expose this option directly.
# Proxy response headers may be accessible via response.headers with some configuration.

require 'typhoeus'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

begin
  response = Typhoeus.get(test_url, proxy: proxy_url)

  if response.success?
    puts "Status: #{response.code}"
    puts "Body: #{response.body}"
  elsif response.timed_out?
    warn 'Error: Request timed out'
    exit 1
  else
    warn "Error: #{response.return_message}"
    exit 1
  end
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
