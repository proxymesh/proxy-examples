#!/usr/bin/env ruby
# frozen_string_literal: true

# Mechanize with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://example.com)
#
# Mechanize is a web automation library. It uses Net::HTTP internally and
# supports proxies, but does NOT support custom CONNECT headers or proxy
# response headers.

require 'mechanize'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://example.com'

proxy_uri = URI.parse(proxy_url)

begin
  agent = Mechanize.new
  agent.set_proxy(proxy_uri.host, proxy_uri.port, proxy_uri.user, proxy_uri.password)

  page = agent.get(test_url)

  puts "Status: #{page.code}"
  puts "Title: #{page.title}"
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
