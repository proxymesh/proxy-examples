#!/usr/bin/env ruby
# frozen_string_literal: true

# HTTPClient fetch through a proxy, then parse the response (scraping-style pipeline).
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# The default test URL returns JSON; this example uses stdlib JSON.parse. For HTML
# scraping, a parser such as Nokogiri is common (installable once ruby-dev is available).
#
# Documentation: https://www.rubydoc.info/gems/httpclient/HTTPClient
require 'bundler/setup'
require 'httpclient'
require 'json'

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
unless proxy_url
  warn 'Error: Set PROXY_URL environment variable'
  exit 1
end

test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'
response_header = ENV['RESPONSE_HEADER']

client = HTTPClient.new
client.proxy = proxy_url

response = client.get(test_url)
body = response.body.respond_to?(:content) ? response.body.content : response.body.to_s

status = response.status
status_code = status.respond_to?(:code) ? status.code : status
puts "Status: #{status_code}"
puts "Body: #{body}"
if response_header && !response_header.empty?
  h = response.headers[response_header] || response.headers[response_header.downcase]
  puts "#{response_header}: #{h}"
end

begin
  data = JSON.parse(body)
  puts "Parsed JSON keys: #{data.keys.join(', ')}" if data.is_a?(Hash)
rescue JSON::ParserError
  puts 'Body is not JSON (use an HTML/XML parser for markup).'
end
