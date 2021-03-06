import serial
import glob
import time
import subprocess
from datetime import datetime
from conex import *
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
    #print "Found ports:"
    #for name in scan():
    #    print name

    pd = []

    zStage = ConexAGP('/dev/ttyUSB0')

    print zStage.seekOrigin()
    print zStage.getPosition()

    time.sleep(1)

    f = open('position_list.csv', 'w')
    
    pos = 4.46

    zStage.moveAbsolute(pos)
    i = 1

    while not zStage.readyToMove():
        pass

    print getInputSequence()

    
    while pos < 4.54:
        current_position = zStage.getPosition()
        print pos
        print>>f, (i, current_position)

        pos += 0.0001
        zStage.moveAbsolute(pos)
    
        while not zStage.readyToMove():
            pass

        os.rename("data.dat", "AOMsweep/data" + str(i) + ".dat")
        getInputSequence()
        i = i + 1
        time.sleep(0.001)

            
    zStage.close()
