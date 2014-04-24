from conex import *

zStage = ConexAGP('/dev/ttyUSB0')

move = 1

while True:
    
    zStage.moveRelative(move)

    while not zStage.readyToMove():
        pass

    move = move * -1

