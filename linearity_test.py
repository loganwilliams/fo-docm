import serial
import glob
import time
import subprocess
from datetime import datetime
from conex import *

def scan():
    return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')

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

    zStage = ConexAGP('/dev/ttyUSB0')

    print zStage.seekOrigin()
    print zStage.getPosition()

    time.sleep(1)

    f = open('linearity_test.csv', 'w')
    
    zStage.moveAbsolute(0)

    while not zStage.readyToMove():
        pass

    zStage.moveAbsolute(27)

    o_dt = datetime.now()

    while not zStage.readyToMove():
        (current_position,t) = zStage.getPositionAndTime()
        dt = t - o_dt
        print>>f, (current_position, dt.seconds*1000000 + dt.microseconds )
            
    zStage.close()
