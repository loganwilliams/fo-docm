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
    args = ("AdSync/AdSync","2000", "5000000")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.readline()
    return output


if __name__=='__main__':
    #print "Found ports:"
    #for name in scan():
    #    print name

    pd = []

    xyStage = PriorXY('/dev/ttyS0')
 
    yStart = .1
    yEnd = .3
    yStep = 1

    xStart = .03
    xEnd = .15
    xStep = 1 # microns

    y = 0
    
    yNum = math.floor(1000*abs(yStart - yEnd) / yStep)
    xNum = math.floor(1000*abs(xStart - xEnd) / xStep)

    print "Enter scan number> ",
    scanNo = raw_input()

    for xi in range((xEnd - xStart)*1000/xStep):
        os.makedirs(str(scanNo) + "/" + str(xi) + "/")

    xPos = xStart
    yPos = yStart

    xyStage.moveAbsolute(xPos, yPos);

    xi = 0

    while xPos < xEnd:
        yPos = yStart
        yi = 0

        while yPos < yEnd:
            xyStage.moveAbsolute(xPos*1000, yPos*1000)

            print str(xPos) + "," + str(yPos)

            subp = getInputSequence()
            
            #os.rename("ch1.dat", str(scanNo) + "/" + str(xi) + "/ch1_" + str(yi) + ".dat");
            #os.rename("ch2.dat", str(scanNo) + "/" + str(xi) + "/ch2_" + str(yi) + ".dat");
            os.rename("ch3.dat", str(scanNo) + "/" + str(xi) + "/ch3_" + str(yi) + ".dat");
            #os.rename("ch4.dat", str(scanNo) + "/" + str(xi) + "/ch4_" + str(yi) + ".dat");
            
            yi += 1
            yPos += float(yStep)/1000
       
        xPos += float(xStep)/1000
        xi += 1

    xyStage.close()

