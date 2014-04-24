import serial
import glob
import time
import subprocess
from datetime import datetime
from conex import *
from prior import *
import os

def scan():
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

def getInputSequence(length, sampling_rate=2e6):
    args = ("AdSync/AdSync",str(length), str(sampling_rate))
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    #(out, err) = popen.communicate()
    #popen.wait()
    #popen.stdout.flush()
    #output = popen.stdout.readline()
    #print output
    return popen

if __name__=='__main__':

    startZ = 17.4
    endZ = 15.8

    print "Enter scan number >",
    scanNo = raw_input()

    os.makedirs(str(scanNo))

    xRange = range(1)
    y = 0

    zStage = ConexAGP('/dev/ttyUSB0')
    xyStage = PriorXY('/dev/ttyS0')

    zStage.moveAbsolute(startZ)

    while not zStage.readyToMove():
        pass

    for xPos in xRange:
        #xyStage.moveAbsolute(y, xPos)

        print("X position: " + str(xPos))

        subp = getInputSequence(5e5 + 1.5e6*abs(startZ - endZ))
        time.sleep(0.1)

        zStage.moveAbsolute(endZ)

        while not zStage.readyToMove():
            pass

        zStage.moveAbsolute(startZ)

        subp.wait()

        os.rename("ch1.dat", str(scanNo) + "/ch1_" + str(xPos) + ".dat")
        os.rename("ch2.dat", str(scanNo) + "/ch2_" + str(xPos) + ".dat")
        os.rename("ch3.dat", str(scanNo) + "/ch3_" + str(xPos) + ".dat")
        os.rename("ch4.dat", str(scanNo) + "/ch4_" + str(xPos) + ".dat")

        while not zStage.readyToMove():
            pass

    zStage.close()
