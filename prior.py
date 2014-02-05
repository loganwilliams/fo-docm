import serial
from datetime import datetime
import string

class PriorXY:
	def __init__(self, device):
		self.device = device
		self.open()

	def open(self, baud=9600):
		self.ser = serial.Serial(self.device, baud, timeout=1)
		#self.ser.write("COMP,0\r")

	def close(self):
		self.ser.close()

	def getPosition(self):
		self.ser.write("P\r")
		line = self.ser.readline()
		line = string.split(line, ",")
		return (int(line[0]), int(line[1]))

	def setPosition(self, x, y):
	    self.ser.write("9," + str(x) + "," + str(y) + ",0\r")
	    line = self.ser.readline()

	def moveRelative(self, x, y):
		self.ser.write("GR," + str(x) + "," + str(y) + "\r")
	    line = self.ser.readline()


	def moveAbsolute(self, x, y):
		self.ser.write("G," + str(x) + "," + str(y) + "\r")
		line = self.ser.readline()

	def stop(self):
		self.ser.write("I")

	def setSpeed(self, speed):
		self.ser.write("O," + str(speed) + "\r")

	def setJoystickEnabled(self, joystickEnabled):
		if joystrickEnabled:
			self.ser.write("J\r")
		else:
			self.ser.write("H\r")
