#!/usr/bin/env python

import socket
import time
import sys
import getopt

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8080


def connect(host, port):
    print "Start client.."
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "Try to connect..", host, ":", port,
    s.connect((host, int(port)))
    print "-- CONNECTED"
    return s


def run(s):
    while 1:
        message = raw_input('Enter your input: ')  # wait user
        s.sendall(message)
        data = s.recv(1024)  # wait server
        print 'Received', repr(data)
        if (data == "quit"):
            break


def close(socket):
    socket.close()


def main(argv):
    HOST = DEFAULT_HOST
    PORT = DEFAULT_PORT

    try:
        opts, args = getopt.getopt(argv, "hH:P:", ["host=", "port="])
    except getopt.GetoptError:
        print 'sock_client.py [-H|--host] <host> [-P|--port] <port_number> [-h|--help]'
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-h':
            print 'sock_client.py [-H|--host] <host> [-P|--port] <port_number> [-h|--help]'
            print 'help     -- this command'
            print 'host     -- require parameter'
            print '         -- specify host (default=localhost)'
            print 'port     -- require parameter'
            print '         -- specify port (default=8080)'
            sys.exit()
        elif opt in ("-H", "--host"):
            HOST = arg
        elif opt in ("-P", "--port"):
            PORT = arg
    socket = connect(HOST, PORT)
    run(socket)
    close(socket)

if __name__ == "__main__":
    main(sys.argv[1:])
