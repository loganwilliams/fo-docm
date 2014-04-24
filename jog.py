from prior import *
from conex import *

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

zStage = ConexAGP('/dev/ttyUSB0')
xyStage = PriorXY('/dev/ttyS0')

zJog = 0.05
xyJog = 0.1

zPos = zStage.getPosition()
(xPos, yPos) = xyStage.getPosition()
flag = True

while flag:
    c = getch()

    if (c == '8'):
        xyStage.moveRelative(0, xyJog*1000)
        yPos += xyJog*1000
    elif (c == '2'):
        xyStage.moveRelative(0, -xyJog*1000)
        yPos -= xyJog*1000
    elif (c == '6'):
        xyStage.moveRelative(xyJog*1000, 0)
        xPos += xyJog*1000
    elif (c == '4'):
        xyStage.moveRelative(-xyJog*1000, 0)
        xPos -= xyJog*1000
    elif (c == '-'):
        zStage.moveRelative(zJog)
        zPos = zStage.getPosition()
    elif (c == '+'):
        zStage.moveRelative(-zJog)
        zPos = zStage.getPosition()
    elif (c == 'r'):
        xyStage.setPosition(0,0)
        xPos = 0
        yPos = 0
    elif (c == 'a'):
        zJog *= 2
        print('Z jog is ' + str(zJog) + ' mm')
    elif (c == 'z'):
        zJog /= 2
        print('Z jog is ' + str(zJog) + ' mm')
    elif (c == 's'):
        xyJog *= 2
        print('XY jog is ' + str(xyJog) + ' mm')
    elif (c == 'x'):
        xyJog /= 2
        print('XY jog is ' + str(xyJog) + ' mm')
    elif (c == 'q'):
        flag = False
    else:
        print 'Unknown entry'

    print('X: ' + str(xPos) + '\tY: ' + str(yPos) + '\tZ: ' + str(zPos))

    
        
