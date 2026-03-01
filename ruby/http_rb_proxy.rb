#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTP.rb (http gem) with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#
# HTTP.rb is a simple Ruby DSL for making HTTP requests. It supports proxies
# but does NOT support sending custom headers during HTTPS CONNECT or reading
# proxy response headers.

require 'http'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

proxy_uri = URI.parse(proxy_url)

proxy_options = [proxy_uri.host, proxy_uri.port]
if proxy_uri.user
  proxy_options << proxy_uri.user
  proxy_options << proxy_uri.password
end

begin
  response = HTTP.via(*proxy_options).get(test_url)

  puts "Status: #{response.status}"
  puts "Body: #{response.body}"
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
