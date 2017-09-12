import serial

id = "5810546552"
name = "kamontat"
data = "temp"

with serial.Serial('/dev/tty.SLAB_USBtoUART', 9600) as ser:
    s = ser.readline()
    while (s != 'end\r\n'):
        print "GET " + s,
        if (s == 'id\r\n'):
            ser.write(b''+id+'\r\n')
            print "send ID RESPONSE: "+id
        elif (s == 'name\r\n'):
            ser.write(b''+name+'\r\n')
            print "send name RESPONSE: "+name
        elif (s == 'data\r\n'):
            ser.write(b''+data+'\r\n')
            print "send data RESPONSE: "+data
        else:
            s = s.replace('\r\n','')
            action,key,value=s.split('$')
            if (action == "set"):
                message = 'SET \'' + key + "\' to value: " + value
                if (key == "data"):
                    data = value
                elif (key == "id"):
                    id = value
                elif (key == "name"):
                    name = value
                else:
                    message = "ERROR\r\n"
                ser.write(b''+ message + '\r\n')
                print message.replace('\r\n', '')
            else:
                ser.write(b'ERROR\r\n')
            print "unknown message"
        s = ser.readline()
    print("close.")
    ser.write(b'close\r\n')
    ser.close()
