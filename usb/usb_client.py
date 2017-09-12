import serial
import time

message = "start"
while (message != "end"):
    message = raw_input('Enter your input:')
    ser = serial.Serial('/dev/tty.SLAB_USBtoUART', 9600,8,serial.PARITY_NONE,1)

    print "send request: " + message
    ser.write(b'' + message + '\r\n')
    # time.sleep(0.3)
    with ser as c:
        recv = c.readline()
        print(recv.decode())
ser.close()
