import math
import serial
import socket

class Input():
    def __init__(self, mode):
        self.mode = mode
        self.x = 0

        if self.mode == "bluetooth":
            self.init_bluetooth()
        elif self.mode == "serial":
            self.init_serial()
        elif self.mode == "socket":
            self.init_socket()
        elif self.mode == "random":
            return
        else:
            mode = "random"

    def init_serial(self):
        self.ser = serial.Serial("COM25", 115200)

    def init_socket(self):
        self.client_socket = socket.socket()
        self.client_socket.connect(('127.0.0.1', 44444))

    def init_bluetooth(self):
        return
    
    def getData(self):
        roll = 0.
        pitch = 0.
        altitude = 0.
        speed = 0.

        if self.mode == "random":
            roll = 5 * math.cos(self.x / 20)
            pitch = 10 * math.sin(self.x / 20)
            altitude = 50 - 30 * math.sin(self.x / 20)
            speed = 10 - 5 * math.cos(self.x / 20)

            self.x = self.x + 1
        elif self.mode == "serial":
            print(self.ser.readline())
        elif self.mode == "socket":
            recv = self.client_socket.recv(1000).decode('utf8').replace("\x00", "").split(",")
            roll = float(recv[0])
            pitch = float(recv[1])
            altitude = float(recv[2])
            speed = float(recv[3])
            print(recv)

        return (pitch, roll, altitude, speed)