#!/usr/bin/env python

import socket
from datetime import datetime

HOST = '127.0.0.1'
PORT = 1431
BYTE_MESSAGE = 1024

TIME_FORMAT_FOR_LOG = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT_FOR_RETURN = '%I:%M %p'

ERROR_MESSAGE = "ERROR"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((HOST, PORT))
print "Open port.. ", PORT
s.listen(1)
print "Waiting.. "

conn, addr = s.accept()

print "Connected to", addr

while 1:
    msg = conn.recv(BYTE_MESSAGE)
    log_time = datetime.now().strftime(TIME_FORMAT_FOR_LOG)
    print ">> {}: ({!r}, {!s}) <-- {}: {}".format(log_time, HOST, PORT, addr, msg)
    if (msg == "quit"):
        conn.sendall(msg)
        break
    elif(msg.lower() == 'localtime'):
        time = datetime.now().strftime(TIME_FORMAT_FOR_RETURN)
        conn.sendall(time)
        print ">> {}: ({!r}, {!s}) --> {}: {}".format(log_time, HOST, PORT, addr, time)
    elif(',' in msg and msg.count(',') == 2):
        v1, v2, op = msg.split(',')
        conn.sendall(v1 + op + v2)
        print ">> {}: ({!r}, {!s}) --> {}: {}".format(log_time, HOST, PORT, addr, v1 + op + v2)
    else:
        conn.sendall(ERROR_MESSAGE)
        print ">> {}: ({!r}, {!s}) --> {}: {}".format(log_time, HOST, PORT, addr, ERROR_MESSAGE)

conn.close()
