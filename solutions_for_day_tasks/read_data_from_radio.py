import struct
import serial
import time


class Coder:
    def code(self, command):
        com, number = command.split()
        return struct.pack('>ch', bytes(com, encoding='utf-8'), int(number))

    def decode(self, command):
        return struct.unpack('>ch', command)




if __name__ == '__main__':
    cd = Coder()
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    ser.setDTR(False)
    
    while True:
        print(ser.read())
        time.sleep(1)
