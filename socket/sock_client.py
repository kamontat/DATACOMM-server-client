import socket
import time

HOST = '127.0.0.1'
PORT = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while 1:
    message = raw_input('Enter your input: ')  # wait user
    s.sendall(message)
    data = s.recv(1024)  # wait server
    print 'Received', repr(data)
    if (data == "quit"):
        break
s.close()
