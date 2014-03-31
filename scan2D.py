import serial
import glob
import time
import subprocess
from datetime import datetime
from conex import *
from prior import *
import math
import os
from threading import Thread

def scan():
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

def getInput():
    args = ("capture-one/AdInputAD")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output

def getInputSequence():
    args = ("AdSync/AdSync","32768", "5000000")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.readline()
    return output


if __name__=='__main__':
    #print "Found ports:"
    #for name in scan():
    #    print name

    pd = []

    zStage = ConexAGP('/dev/ttyUSB0')
    xyStage = PriorXY('/dev/ttyS0')
 
    zStart = 7.25-.25 #mm
    zEnd = 7.25+.05 # mm
    zStep = 3 # microns

    xStart = 0
    xEnd = .100
    xStep = 5 # microns

    y = 0
    
    zNum = math.floor(1000*abs(zStart - zEnd) / zStep)
    xNum = math.floor(1000*abs(xStart - xEnd) / xStep)

    print "Enter scan number> ",
    scanNo = raw_input()

    curpos = zStage.getPosition()

    for xi in range(xNum):
        os.makedirs(str(scanNo) + "/" + str(xi) + "/")

    xPos = xStart

    xyStage.moveAbsolute(xPos, y);

    xi = 0

    while xPos < xEnd:
        xyStage.moveAbsolute(xPos*1000, y);
        time.sleep(0.1)

        zPos = zStart
        zi = 0

        while zPos < zEnd:
            zStage.moveAbsolute(zPos)

            while not zStage.readyToMove():
                pass

            print str(xPos) + "," + str(zPos)

            subp = getInputSequence()
            
            os.rename("ch1.dat", str(scanNo) + "/" + str(xi) + "/ch1_" + str(zi) + ".dat");
            os.rename("ch2.dat", str(scanNo) + "/" + str(xi) + "/ch2_" + str(zi) + ".dat");
            os.rename("ch3.dat", str(scanNo) + "/" + str(xi) + "/ch3_" + str(zi) + ".dat");
            os.rename("ch4.dat", str(scanNo) + "/" + str(xi) + "/ch4_" + str(zi) + ".dat");
            
            zi += 1
            zPos += float(zStep)/1000
       
        xPos += float(xStep)/1000
        xi += 1

    zStage.close()
    xyStage.close()

