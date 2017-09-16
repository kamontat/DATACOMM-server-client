#!/usr/bin/env python

import socket
# import time

HOST = '127.0.0.1'
PORT = 8080

print "Start client."
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Open socket."
s.connect((HOST, PORT))

print "Connected to the server..."

while 1:
    message = raw_input('Enter your input: ')  # wait user
    s.sendall(message)
    data = s.recv(1024)  # wait server
    print 'Received', repr(data)
    if (data == "quit"):
        break

s.close()
