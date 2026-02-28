#!/usr/bin/env ruby
# frozen_string_literal: true

# Net::HTTP with proxy example.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#
# Net::HTTP is Ruby's built-in HTTP client. It supports proxies but does NOT
# support sending custom headers during HTTPS CONNECT or reading proxy response headers.

require 'net/http'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

proxy_uri = URI.parse(proxy_url)
target_uri = URI.parse(test_url)

proxy_options = {
  p_addr: proxy_uri.host,
  p_port: proxy_uri.port,
  p_user: proxy_uri.user,
  p_pass: proxy_uri.password
}

begin
  Net::HTTP.start(target_uri.host, target_uri.port, **proxy_options, use_ssl: target_uri.scheme == 'https') do |http|
    request = Net::HTTP::Get.new(target_uri)
    response = http.request(request)

    puts "Status: #{response.code}"
    puts "Body: #{response.body}"
  end
rescue StandardError => e
  warn "Error: #{e.message}"
  exit 1
end
