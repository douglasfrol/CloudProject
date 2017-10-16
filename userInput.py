import sys
import subprocess
import os
from database import readValues

def getUserInput():
    cmdArgs = sys.argv
    cmdArgs.pop(0)
    cmdArgs = [ int(x) for x in cmdArgs ]
    return (cmdArgs)

def anglesToCheck(values):
    lowerAngle = values[0] 
    upperAngle = values[1]
    n_angles = values[2]
    interval = (upperAngle - lowerAngle)/n_angles
    angleList = []
    angle = 0
    for i in range(0, n_angles+1):
        angle = (lowerAngle + interval*i)
        angleList.append(angle)
    return (angleList)

def checkDatabase():
    values = getUserInput()
    angles = anglesToCheck(values)
    notInDb = []
    for i in angles:
        if readValues(i) != (-1,-1):
            print "Values already stored in database! Velocity: " + str(readValues(i)[0]) + ", Pressure: " + str(readValues(i)[1])
        else:
            notInDb.append(i)        

    #Check if list is not empty
    if notInDb:
        print "Creating meshes for angles"
        createMeshes(values)
        convertMeshes(angles)
    else:
        print "All angles already calculated"
    

def createMeshes(values):
    directory = '/home/ubuntu/murtazo/cloudnaca'
    bashStrings = ['sudo', './runme.sh', str(values[0]), str(values[1]), str(values[2]), '200', '3']
    #subprocess.call(['sudo', './runme.sh', '100', '130', '10', '200', '3'], cwd = directory)
    subprocess.call(bashStrings, cwd = directory)

def convertMeshes(angles):
    directory = '/home/ubuntu/murtazo/cloudnaca/msh'
    for angle in angles:
        bashStrings = ['sudo', 'dolfin-convert', 'r0a' + str(angle) + 'n200.msh', 'r0a' + str(angle) + 'n200.xml']
        subprocess.call(bashStrings, cwd = directory)        
checkDatabase()