#!/usr/bin/env ruby
# frozen_string_literal: true

# Run all Ruby proxy examples as tests.
#
# Configuration via environment variables:
#   PROXY_URL       - Proxy URL (required), e.g., http://user:pass@proxy:8080
#   TEST_URL        - URL to request (default: https://api.ipify.org?format=json)
#   PROXY_HEADER    - Header name to send to proxy (optional)
#   PROXY_VALUE     - Header value to send to proxy (optional)
#
# Usage:
#   ruby run_tests.rb              # Run all examples
#   ruby run_tests.rb faraday      # Run specific example
#   ruby run_tests.rb -l           # List available examples
#   ruby run_tests.rb -v           # Verbose output

EXAMPLES = %w[
  net_http_proxy.rb
  faraday_proxy.rb
  httparty_proxy.rb
  rest_client_proxy.rb
  typhoeus_proxy.rb
  http_rb_proxy.rb
  excon_proxy.rb
  httpclient_proxy.rb
  mechanize_proxy.rb
].freeze

def parse_args(args)
  options = {
    verbose: false,
    list: false,
    help: false,
    examples: []
  }

  args.each do |arg|
    case arg
    when '-v', '--verbose'
      options[:verbose] = true
    when '-l', '--list'
      options[:list] = true
    when '-h', '--help'
      options[:help] = true
    else
      options[:examples] << arg unless arg.start_with?('-')
    end
  end

  options
end

def show_help
  puts <<~HELP
    Run all Ruby proxy examples as tests.

    Usage:
      ruby run_tests.rb [options] [example1] [example2] ...

    Options:
      -v, --verbose    Show full output from each example
      -l, --list       List available examples
      -h, --help       Show this help message

    Environment Variables:
      PROXY_URL        Proxy URL (required), e.g., http://user:pass@proxy:8080
      TEST_URL         URL to request (default: https://api.ipify.org?format=json)
      PROXY_HEADER     Header name to send to proxy (optional)
      PROXY_VALUE      Header value to send to proxy (optional)

    Examples:
      PROXY_URL='http://proxy:8080' ruby run_tests.rb
      ruby run_tests.rb faraday httparty
  HELP
end

def list_examples
  puts 'Available examples:'
  EXAMPLES.each do |example|
    puts "  #{example.sub('_proxy.rb', '')}"
  end
end

def mask_password(url)
  url.sub(/:[^:@]+@/, ':****@')
end

def run_example(name, verbose)
  script_dir = File.dirname(__FILE__)
  script_path = File.join(script_dir, name)

  unless File.exist?(script_path)
    return { success: false, error: "Script not found: #{script_path}" }
  end

  output = `ruby #{script_path} 2>&1`
  success = $?.success?

  if verbose
    puts output
  end

  { success: success, output: output }
end

def main
  options = parse_args(ARGV)

  if options[:help]
    show_help
    exit 0
  end

  if options[:list]
    list_examples
    exit 0
  end

  proxy_url = ENV['PROXY_URL'] || ENV['HTTPS_PROXY']
  unless proxy_url
    warn 'Error: Set PROXY_URL environment variable'
    warn "\nExample:"
    warn "  export PROXY_URL='http://user:pass@proxy:8080'"
    exit 1
  end

  examples_to_run = if options[:examples].any?
    EXAMPLES.select { |e| options[:examples].any? { |arg| e.include?(arg) } }
  else
    EXAMPLES
  end

  test_url = ENV['TEST_URL'] || 'https://api.ipify.org?format=json'

  puts '=' * 60
  puts 'Ruby Proxy Examples - Test Runner'
  puts '=' * 60
  puts "Proxy URL:       #{mask_password(proxy_url)}"
  puts "Test URL:        #{test_url}"
  puts "Examples:        #{examples_to_run.length}"
  puts '=' * 60
  puts

  passed = 0
  failed = 0

  examples_to_run.each do |example|
    name = example.sub('_proxy.rb', '')
    print "Testing #{name}... "

    result = run_example(example, options[:verbose])

    if result[:success]
      puts 'OK'
      passed += 1
    else
      puts 'FAILED'
      unless options[:verbose]
        error_line = result[:output]&.lines&.first&.strip
        puts "  Error: #{error_line}" if error_line
      end
      failed += 1
    end
  end

  puts
  puts '=' * 60
  puts "Results: #{passed} passed, #{failed} failed"
  puts '=' * 60

  exit(failed.positive? ? 1 : 0)
end

main if __FILE__ == $PROGRAM_NAME
