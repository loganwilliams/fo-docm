import serial
import time
from datetime import datetime

class ConexAGP:
    def __init__(self, device):
        self.device = device
        self.open()

    def open(self, baud=921600):
        self.ser = serial.Serial(self.device, baud, timeout=1)

    def close(self):
        self.ser.close()

    def getPosition(self):
        self.ser.write("1TP?\r\n")
        line = self.ser.readline()
        line = line[3:-2]
        return float(line)

    def getPositionAndTime(self):
        self.ser.write("1TP?\r\n")
        t = datetime.now()
        line = self.ser.readline()
        line = line[3:-2]
        return (float(line),t)

    def seekOrigin(self):
        self.ser.write("1OR\r\n")
        return self.ser.readline()

    def moveRelative(self, x):
        self.ser.write("1PR" + str(x) + "\r\n")

    def moveAbsolute(self, x):
        self.ser.write("1PA" + str(x) + "\r\n")

    def getStatus(self):
        self.ser.write("1TS?\r\n")
        line = self.ser.readline()
        return line[-4:-2]

    def readyToMove(self):
        status = self.getStatus()
        return (status == "34" or status == "33" or status == "32")

    def reset(self):
        self.ser.write("1RS\r\n")

    def setKp(self, Kp):
        self.ser.write("1MM0\r\n")
        time.sleep(0.5)

        self.ser.write("1KP" + str(Kp) + "\r\n")
        time.sleep(0.5)

        self.ser.write("1MM1\r\n")
        time.sleep(0.5)

    def setLf(self, Lf):
        self.ser.write("1MM0\r\n")
        time.sleep(0.5)

        self.ser.write("1LF" + str(Lf) + "\r\n")
        time.sleep(0.5)

        self.ser.write("1MM1\r\n")
        time.sleep(0.5)

    def setKi(self, Ki):
        self.ser.write("1MM0\r\n")
        time.sleep(0.5)

        self.ser.write("1KP" + str(Ki) + "\r\n")
        time.sleep(0.5)

        self.ser.write("1MM1\r\n")
        time.sleep(0.5)

    def setKp(self, Kp):
        self.ser.write("1MM0\r\n")
        time.sleep(0.5)

        self.ser.write("1KP" + str(Kp) + "\r\n")
        time.sleep(0.5)

        self.ser.write("1MM1\r\n")
        time.sleep(0.5)

