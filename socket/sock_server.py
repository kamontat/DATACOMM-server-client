#!/usr/bin/env python

import socket
import sys
import getopt
import operator
from datetime import datetime
# print "start server"

HOST = '127.0.0.1'
PORT = 8080
BYTE_MESSAGE = 1024

SEPARATOR = ','

TIME_FORMAT_FOR_LOG = '%Y-%m-%d %H:%M:%S'
TIME_FORMAT_FOR_RETURN = '%I:%M %p'

ERROR_MESSAGE = "ERROR"

CLIENT_ADDRESS = ""


def bind_and_accept():
    """return value => conn, addr"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print "Open port: ", PORT
    s.listen(1)
    print "Waiting..."
    return s.accept()


def get_log_time():
    return datetime.now().strftime(TIME_FORMAT_FOR_LOG)


def to_client_log(message):
    return ">> {}: ({!r}, {!s}) --> {}: {}".format(get_log_time(), HOST, PORT, CLIENT_ADDRESS, message)


def to_server_log(message):
    return ">> {}: ({!r}, {!s}) <-- {}: {}".format(get_log_time(), HOST, PORT, CLIENT_ADDRESS, message)


def a_quit(connection, msg):
    """quit action"""
    if (msg == "quit"):
        connection.sendall(msg)
        return True
    else:
        return False


def a_time(connection, msg):
    """getting localtime action"""
    if(msg.lower() == 'localtime'):
        time = datetime.now().strftime(TIME_FORMAT_FOR_RETURN)
        connection.sendall(time)
        print to_client_log(time)
        return True
    else:
        return False


def get_ops(op):
    return {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.div,
        '%': operator.mod,
        '^': operator.xor,
    }[op]


def a_format_operation(connection, msg):
    """reformat operation of input string action"""
    if(SEPARATOR in msg and msg.count(SEPARATOR) == 2):
        v1, v2, op = msg.split(',')
        try:
            connection.sendall('{} {} {} = {}'.format(v1, op, v2, get_ops(op)(int(v1), int(v2))))
        except KeyError:
            return False
        print to_client_log(v1 + op + v2)
        return True
    return False


def a_throw_error(connection):
    """throw error action"""
    connection.sendall(ERROR_MESSAGE)
    print to_client_log(ERROR_MESSAGE)


def close(connection):
    connection.close()


def main(argv):
    global HOST
    global PORT
    global BYTE_MESSAGE
    global TIME_FORMAT_FOR_RETURN
    global TIME_FORMAT_FOR_LOG
    global ERROR_MESSAGE
    global CLIENT_ADDRESS

    try:
        opts, args = getopt.getopt(argv, "hH:P:S:T:t:E:", [
                                   "help", "host=", "port=", "msg-size=", "time-log-format=", "time-format=", "error-message="])
    except getopt.GetoptError:
        print 'sock_server.py [-H|--host] <host> [-P|--port] <port_number> ', '[-S|--msg-size] <msg_size> [-T|--time-format] <response_time_format> ', '[-t|--time-log-format] <format_of_time_in_log> [-E|--error-message] <response_message_when_error> ', '[-h|--help]'
        sys.exit(0)
    for opt, arg in opts:
        if opt == '-h':
            print 'sock_server.py [-H|--host] <host> [-P|--port] <port_number> ', '[-S|--msg-size] <msg_size> [-T|--time-format] <response_time_format> ', '[-t|--time-log-format] <format_of_time_in_log> [-E|--error-message] <response_message_when_error> ', '[-h|--help]'
            print 'help             -- this command'
            print 'host             -- require parameter'
            print '                 -- specify host (default=localhost)'
            print 'port             -- require parameter'
            print '                 -- specify port (default=8080)'
            print 'msg-size         -- require parameter'
            print '                 -- size of buffer that server will read (default=1024)'
            print 'time-format      -- require parameter'
            print '                 -- format of time that server will response to client in `localtime` command (default=%I:%M %p)'
            print 'time-log-format  -- require parameter'
            print '                 -- format of time that server will log to console (default=%Y-%m-%d %H:%M:%S)'
            print 'error-message    -- require parameter'
            print '                 -- the message that server will response when some error occured (default=ERROR)'
            sys.exit()
        elif opt in ("-H", "--host"):
            HOST = arg
        elif opt in ("-P", "--port"):
            PORT = int(arg)
        elif opt in ("-S", "--msg-size"):
            BYTE_MESSAGE = arg
        elif opt in ("-T", "--time-format"):
            TIME_FORMAT_FOR_RETURN = arg
        elif opt in ("-E", "--error-message"):
            ERROR_MESSAGE = arg
        elif opt in ("-t", "--time-log-format"):
            TIME_FORMAT_FOR_LOG = arg
    # start binding and accept
    connection, CLIENT_ADDRESS = bind_and_accept()
    print "Connected by", CLIENT_ADDRESS
    # running server loop
    while 1:
        msg = connection.recv(BYTE_MESSAGE)
        print to_server_log(msg)
        # if quit break loop
        if (a_quit(connection, msg)):
            break
        # if not getting time and not format oper -> throw error
        elif (not a_time(connection, msg) and not a_format_operation(connection, msg)):
            a_throw_error(connection)

    close(connection)

if __name__ == "__main__":
    main(sys.argv[1:])
