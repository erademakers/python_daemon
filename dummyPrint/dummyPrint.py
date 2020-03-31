#!/usr/bin/python3

import sys
import serial
import time

def dummyPrint(device):
    print(device)
    ser = serial.Serial(device, 115200, timeout=1)
    ser.close()
    ser.open()
    while True:
        flag = 0
        try:
            ser.write("BPM=100\n".encode('utf-8'))
            ser.write("VOL=200\n".encode('utf-8'))
            ser.write("TRIG=0\n".encode('utf-8'))
            ser.write("PRES=20\n".encode('utf-8'))
            if ser.in_waiting > 0:
                rcv = ser.read()
                if rcv == 'T':
                    flag = 1
                rcv = ser.read()
            if flag == 1:
                ser.write("OK\n".encode('utf-8'))
            else:
                ser.write("NOK\n".encode('utf-8'))
        except:
            print("Serial disconnected or not available")
            ser.close()
            break
        time.sleep(0.1)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        dummyPrint(sys.argv[1])
