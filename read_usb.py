import serial

ser = serial.Serial("COM25", 115200)
while True:
    print(ser.readline())