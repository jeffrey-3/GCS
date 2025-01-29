import serial
import time
import struct

bluetooth = serial.Serial('COM9', 115200, timeout=1000)

while True:
    if bluetooth.in_waiting > 0:
        data_raw = bluetooth.read_all() # Flush buffer
        idx = data_raw.rfind(b'\n')
        data = data_raw[idx-29:idx+1]

        print(struct.unpack('fffffff?c', data))

        time.sleep(0.1)