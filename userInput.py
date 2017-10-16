import sys
from database import readValues

def getUserInput():
    cmdArgs = sys.argv
    cmdArgs.pop(0)
    cmdArgs = [ int(x) for x in cmdArgs ]
    return (cmdArgs)

def anglesToCheck():
    values = getUserInput()
    lowerAngle = values[0] 
    upperAngle = values[1]
    n_angles = values[2]
    interval = (upperAngle - lowerAngle)/n_angles
    angleList = []
    angle = 0
    for i in range(0, n_angles+1):
        angle = (lowerAngle + interval*i)
        angleList.append(angle)
    print (angleList)

def checkDatabase():
    angles = anglesToCheck()
    for i in angels:
        if readValues(i) != (-1,-1):
            print "Values already stored in database! Velocity: " + str(readValues(i)[0]) + ", Pressure: " + str(readValues(i)[1])
        else:
             