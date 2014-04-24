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
    
    posS = 17.369
    posE = 18.369
    n = 50

    zStage.moveAbsolute(posS)
    i = 1

    while not zStage.readyToMove():
        pass

    for lf in [5, 10, 20, 50]:
        print("Setting Lf = " + str(lf))

        zStage.setLf(lf)

        time.sleep(1)

        os.mkdir("repeatability-" + str(lf))

        for i in range(n):
            print i

            posList = []
            f = open('z_position_list.csv', 'w')

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
            os.rename("data.dat", "repeatability-" + str(lf) + "/data" + str(i) + ".dat")
            os.rename("z_position_list.csv", "repeatability-" + str(lf) + "/z_position_list" + str(i) + ".csv")

            while not zStage.readyToMove():
                pass
            
            #raw_input("press enter to continue")
                
    zStage.close()
