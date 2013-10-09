import serial
import glob
import time
import subprocess

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

def getInput():
    args = ("capture-one/AdInputAD")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output

if __name__=='__main__':
    #print "Found ports:"
    #for name in scan():
    #    print name

    pd = []

    ser = serial.Serial('/dev/ttyUSB0', 921600, timeout=1)

    #print seekOrigin(ser)
    #print getPosition(ser)

    while (1 == 1):
        moveAbsolute(ser, 9.5)
        time.sleep(0.3)
        moveAbsolute(ser, 9.9)
        time.sleep(0.3)    

    start_pos = 5
    move_interval = 0.0005
    end_pos = 6

    moveAbsolute(ser, start_pos)

    time.sleep(1)

    f = open('data', 'w')

    # move 1mm in 1um increments, reporting position every step
    current_position = start_pos
    while (current_position < end_pos):
        if readyToMove(ser):
            moveRelative(ser,move_interval)
            current_position = getPosition(ser)
            print current_position
            val = int(getInput(),16)
            pd.append(val)
            print>>f, val
            
    ser.close()
