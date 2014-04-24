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
    posS = 3.68 - 0.1
    posE = 3.68 + 0.1
    n = 10

    zStage.moveAbsolute(posS)
    i = 1

    while not zStage.readyToMove():
        pass

    posList = []

    step = 0.0005
    curpos = zStage.getPosition()

    while curpos < posE:
        print curpos
        posList.append(curpos)

        subp = getInputSequence()

        time.sleep(0.1)

        os.rename("data.dat", "psf-water/data" + str(i) + ".dat")

        curpos += step
        zStage.moveAbsolute(curpos)

        while not zStage.readyToMove():
            pass
        

        i += 1

    f = open('psf-water/position_list.csv', 'w')
    for j in range(len(posList)):
        print>>f, str(posList[j])
        
    f.close()
            
    zStage.close()
