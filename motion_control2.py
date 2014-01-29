import serial
import glob
import time
import subprocess
from datetime import datetime
from conex import *
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
    args = ("capture/AdSampling",)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    #(out, err) = popen.communicate()
    #popen.wait()
    #popen.stdout.flush()
    #output = popen.stdout.readline()
    #print output
    return popen
    #return None

if __name__=='__main__':
    #print "Found ports:"
    #for name in scan():
    #    print name

    pd = []

    zStage = ConexAGP('/dev/ttyUSB0')

    #print zStage.seekOrigin()
    #print zStage.getPosition()

    time.sleep(1)
    
    center = 9.64

    #posS = center - 0.2
    #posE = center + 1.0
    posS = 0
    posE = 2
    n = 10

    zStage.moveAbsolute(posS)
    i = 1

    while not zStage.readyToMove():
        pass

    for i in range(n):
        print i

        posList = []
        f = open('position_list.csv', 'w')

        # tell the stage to start moving
        zStage.moveAbsolute(posE)

        (op, ot) = zStage.getPositionAndTime()
        ot = ot.second*1000000 + ot.microsecond
        posList.append((op, ot))

        # tell the card to start capturing data
        subp = getInputSequence()

        while not zStage.readyToMove():
            (np, nt) = zStage.getPositionAndTime()
            nt = nt.second*1000000 + nt.microsecond
            posList.append((np, nt))

        adcStartTime = int(subp.stdout.readline())

        for j in range(len(posList)):
            (p, t) = posList[j]
            t = t - adcStartTime
            
            #if (t < 0):
            #    t = t + 60000000
            
            posList[j] = (p, t)
            print>>f, (str(t) + "," +str(p))

        zStage.moveAbsolute(posS)
        
        f.close()
        os.rename("data.dat", "reproducibility/data" + str(i) + ".dat")
        os.rename("position_list.csv", "reproducibility/position_list" + str(i) + ".csv")

        while not zStage.readyToMove():
            pass
        
        #raw_input("press enter to continue")
            
    zStage.close()
