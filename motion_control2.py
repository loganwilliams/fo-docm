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
    (out, err) = popen.communicate()
    #popen.wait()
    #output = popen.stdout.read()
    return out

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
    
    posS = 1.6
    posE = 3
    n = 10

    zStage.moveAbsolute(posS)
    i = 1

    while not zStage.readyToMove():
        pass

    for i in range(n):
        print i

        zStage.moveAbsolute(posE)

        ot = datetime.now()
        print getInputSequence()
        (p,t) = zStage.getPositionAndTime()
        dt = (t - ot)        

        print (p, dt.seconds*1000000 + dt.microseconds)
        
        while not zStage.readyToMove():
            pass

        zStage.moveAbsolute(posS)
        
        os.rename("data.dat", "reproducibility/data" + str(i) + ".dat")

        while not zStage.readyToMove():
            pass
            
    zStage.close()
