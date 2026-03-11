#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTParty with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#
# HTTParty makes HTTP fun! It supports proxies but does NOT support sending
# custom headers during HTTPS CONNECT or reading proxy response headers.

require 'httparty'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

proxy_uri = URI.parse(proxy_url)

http_proxy_options = {
  http_proxyaddr: proxy_uri.host,
  http_proxyport: proxy_uri.port
}

if proxy_uri.user
  http_proxy_options[:http_proxyuser] = proxy_uri.user
  http_proxy_options[:http_proxypass] = proxy_uri.password
end

begin
  response = HTTParty.get(test_url, **http_proxy_options)

  puts "Status: #{response.code}"
  puts "Body: #{response.body}"
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
