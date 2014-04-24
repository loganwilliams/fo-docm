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

def getInputSequence():
    args = ("AdSync/AdSync","2000000", "10000000")
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    #popen.wait()
    #output = popen.stdout.readline()
    return popen

for i in range(87,101):
    print str(i)
    x = getInputSequence()    
    x.wait()

    os.rename("ch3.dat", "4-21-2/ch3_" + str(i) + ".dat");
    os.rename("ch4.dat", "4-21-2/ch4_" + str(i) + ".dat");
