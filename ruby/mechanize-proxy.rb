#!/usr/bin/env ruby
# frozen_string_literal: true

# Mechanize (browser-like crawling) with an HTTP proxy.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# Use Mechanize#set_proxy(address, port, user = nil, password = nil) with host/port
# and credentials parsed from the proxy URL.
#
# Documentation: https://www.rubydoc.info/gems/mechanize/Mechanize#set_proxy-instance_method
require 'bundler/setup'
require 'mechanize'
require 'uri'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

proxy = URI.parse(proxy_url)

agent = Mechanize.new
agent.set_proxy(proxy.host, proxy.port, proxy.user, proxy.password)

page = agent.get(test_url)

puts "Status: #{page.code}"
puts "Body: #{page.body}"
if response_header && !response_header.empty?
  puts "#{response_header}: #{page.response[response_header]}"
end
