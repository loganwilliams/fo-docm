import serial
import glob
import time

def scan():
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

def getPosition(ser):
    ser.write("1TP?\r\n")
    line = ser.readline()
    line = line[3:-2]
    return float(line)

def seekOrigin(ser):
    ser.write("1OR\r\n")
    return ser.readline()

def moveRelative(ser, x):
    ser.write("1PR" + str(x) + "\r\n")

def moveAbsolute(ser, x):
    ser.write("1PA" + str(x) + "\r\n")

def getStatus(ser):
    ser.write("1TS?\r\n")
    line = ser.readline()
    return line[-4:-2]

def readyToMove(ser):
    status = getStatus(ser)
    return (status == "34" or status == "33" or status == "32")

if __name__=='__main__':
    print "Found ports:"
    for name in scan():
        print name

    ser = serial.Serial('/dev/ttyUSB0', 921600, timeout=1)

    print seekOrigin(ser)
    print getPosition(ser)
    moveAbsolute(ser, 0)

    time.sleep(1)

    # move 1mm in 1um increments, reporting position every step
    current_position = 0.0
    while (current_position <= 0.1):
        if readyToMove(ser):
            moveRelative(ser,0.001)
            current_position = getPosition(ser)
            print current_position

    ser.close()
