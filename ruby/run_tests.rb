#!/usr/bin/env ruby
# frozen_string_literal: true

# Run all Ruby proxy examples as tests.
#
# Configuration via environment variables:
#     PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#     TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#     RESPONSE_HEADER - Optional header name to print from the response
#
# Usage:
#     bundle exec ruby run_tests.rb              # Run all examples
#     bundle exec ruby run_tests.rb httpclient   # Run specific example
#     bundle exec ruby run_tests.rb -l           # List available examples
#
# Install dependencies first: bundle install
require 'open3'
require 'uri'

SCRIPT_DIR = File.expand_path(__dir__)

EXAMPLES = %w[
  net-http-proxy.rb
  httpclient-proxy.rb
  httpclient-scrape-proxy.rb
  httparty-proxy.rb
  typhoeus-proxy.rb
  excon-proxy.rb
].freeze

def parse_args(argv)
  options = { list: false, help: false, examples: [] }
  argv.each do |arg|
    case arg
    when '-l', '--list' then options[:list] = true
    when '-h', '--help' then options[:help] = true
    when /^-/
      # ignore unknown flags
    else
      options[:examples] << arg
    end
  end
  options
end

def show_help
  puts <<~HELP
    Run all Ruby proxy examples as tests.

    Usage:
        bundle exec ruby run_tests.rb [options] [example ...]

    Options:
        -l, --list       List available examples
        -h, --help       Show this help message

    Environment variables:
        PROXY_URL        Proxy URL (required), e.g., http://user:pass@proxy:8080
        TEST_URL         URL to request (default: https://api.ipify.org?format=json)
        RESPONSE_HEADER  Optional header name to print from the response

    Install dependencies first: bundle install
  HELP
end

def list_examples
  puts 'Available examples:'
  EXAMPLES.each do |f|
    puts "  #{f.sub(/-proxy\.rb$/, '')}"
  end
end

def mask_password(url)
  u = URI.parse(url)
  return url unless u.password

  url.sub(":#{u.password}@", ':****@')
rescue URI::InvalidURIError
  url
end

def run_example(filename)
  path = File.join(SCRIPT_DIR, filename)
  return [false, 'script not found'] unless File.file?(path)

  env = ENV.to_h
  _stdout, stderr, status = Open3.capture3(
    env,
    'bundle', 'exec', 'ruby', path,
    chdir: SCRIPT_DIR
  )
  [status.success?, stderr.lines.first&.strip]
end

options = parse_args(ARGV)

if options[:help]
  show_help
  exit 0
end

if options[:list]
  list_examples
  exit 0
end

unless ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
  warn 'Error: Set PROXY_URL environment variable'
  warn ''
  warn 'Example:'
  warn "  export PROXY_URL='http://user:pass@proxy:8080'"
  exit 1
end

to_run = if options[:examples].empty?
           EXAMPLES
         else
           EXAMPLES.select do |f|
             stem = f.sub('-proxy.rb', '')
             options[:examples].any? { |arg| f.include?(arg) || stem.start_with?(arg) }
           end
         end

if to_run.empty?
  warn 'No matching examples.'
  exit 1
end

proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

puts '=' * 60
puts 'Ruby Proxy Examples - Test Runner'
puts '=' * 60
puts "Proxy URL:       #{mask_password(proxy_url)}"
puts "Test URL:        #{test_url}"
puts "Examples:        #{to_run.size}"
puts '=' * 60
puts

passed = 0
failed = 0

to_run.each do |filename|
  name = filename.sub('.rb', '')
  print "Testing #{name}... "
  ok, err = run_example(filename)
  if ok
    puts 'OK'
    passed += 1
  else
    puts 'FAILED'
    warn "  Error: #{err}" if err
    failed += 1
  end
end

puts
puts '=' * 60
puts "Results: #{passed} passed, #{failed} failed"
puts '=' * 60

exit(failed.positive? ? 1 : 0)
