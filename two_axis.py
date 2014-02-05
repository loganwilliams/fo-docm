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

def getInput():
    args = ("capture-one/AdInputAD")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output

def getInputSequence():
    args = ("capture/AdSampling")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    return output

if __name__=='__main__':

    startZ = 9.4
    endZ = 9.8

    xRange = range(0, 100, 2)
    y = 100

    zStage = ConexAGP('/dev/ttyUSB0')
    xyStage = PriorXY('/dev/ttyS0')

    #zStage.seekOrigin()
    #time.sleep(1)

    zStage.moveAbsolute(startZ)

    while not zStage.readyToMove():
        pass

    for xPos in xRange:
        xyStage.moveAbsolute(xPos, y)

        print("X position: " + str(xPos))

        posList = []
        f = open('z_position_list.csv')

        zStage.moveAbsolute(endZ)

        (op, ot) = zStage.getPositionAndTime()
        ot = ot.second*1000000 + ot.microsecond
        posList.append((op, ot))

        subp = getInputSequence()

        while not zStage.readyToMove():
            (np, nt) = zStage.getPositionAndTime()
            nt = nt.second*1000000 + nt.microsecond
            posList.append((np, nt))

        adcStartTime = int(subp.stdout.readline())

        for j in range(len(posList)):
            (p, t) = posList[j]
            t = t - adcStartTime
            
            posList[j] = (p, t)
            print>>f, (str(t) + "," +str(p))

        zStage.moveAbsolute(startZ)

        f.close()
        os.rename("data.dat", "two_axis/data" + str(xPos) + ".dat")
        os.rename("z_position_list.csv", "two_axis/z_position_list" + str(xPos) + ".csv")

        while not zStage.readyToMove():
            pass

    zStage.close()
