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
    args = ("AdSync/AdSync","2000000", "2000000")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    #popen.wait()
    #output = popen.stdout.readline()
    return popen


if __name__=='__main__':
    #print "Found ports:"
    #for name in scan():
    #    print name

    pd = []

    xyStage = PriorXY('/dev/ttyS0')
 
    yStart = 16.4 #mm
    yEnd = 15.8 # mm
    yStep = 5 # microns

    xStart = 0
    xEnd = .001
    xStep = 1 # microns
    
    yNum = math.floor(1000*abs(yStart - yEnd) / yStep)
    xNum = math.floor(1000*abs(xStart - xEnd) / xStep)

    print "Enter scan number> ",
    scanNo = raw_input()

    for xi in range(xNum):
        os.makedirs(str(scanNo) + "/" + str(xi) + "/")

    xPos = xStart
    yPos = yStart

    #xyStage.moveAbsolute(xPos*1000, yPos*1000);

    xi = 0

    while xPos < xEnd:
        yPos = yStart
 
        print str(xPos) + "," + str(yPos)

        print "moving to start"
        xyStage.moveAbsolute(xPos*1000, yStart*1000);
        time.sleep(0.1)

        yi = 0

        print "beginning scan"

        #time.sleep(1.0)

        subp = getInputSequence()

        #zStage.moveAbsolute(zPos)
        xyStage.moveAbsolute(xPos*1000, yEnd*1000)




        subp.wait()
        subp.stdout.read()


        
        #os.rename("ch1.dat", str(scanNo) + "/" + str(xi) + "/ch1_" + str(yi) + ".dat");
        #os.rename("ch2.dat", str(scanNo) + "/" + str(xi) + "/ch2_" + str(yi) + ".dat");
        os.rename("ch3.dat", str(scanNo) + "/" + str(xi) + "/ch3_" + str(yi) + ".dat");
        #os.rename("ch4.dat", str(scanNo) + "/" + str(xi) + "/ch4_" + str(yi) + ".dat");
       
        xPos += float(xStep)/1000
        xi += 1

    xyStage.close()

