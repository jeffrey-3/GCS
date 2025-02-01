import serial
import time
import struct
from cobs import cobs

bluetooth = serial.Serial('COM9', 115200, timeout=1000)

while True:
    if bluetooth.in_waiting > 0:
        data_raw = bluetooth.read_all() # Flush buffer
        last_idx = data_raw.rfind(0b00000000)
        second_last_idx = data_raw.rfind(0b00000000, 0, last_idx)
        data = data_raw[second_last_idx:last_idx]

        if len(data) == 40:
            # Figure out what type of payload
            if data[0] == 0: # Telemetry payload
                data = data[1:] # Remove start byte
                data = cobs.decode(data) # Decode COBS
                data = data[1:-9] # Remove empty bytes and the "payload type" byte
                print(struct.unpack("<fffffff", data)) # Use endian to remove padding