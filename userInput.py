import sys
import subprocess
import os
from celery import Celery
from database import readValues
from worker import airfoil

appBroker = 'amqp://guest@localhost//'
debug = True

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

def checkDatabase(values, angles):    
    notInDb = []
    #'angle' = [drag, lift]
    inDb = {}
    for i in angles:
        if readValues(i) != (-1,-1):
            print "Values already stored in database! Drag: " + str(readValues(i)[0]) + ", Lift: " + str(readValues(i)[1])
            inDb[i] = [readValues(i)[0], readValues(i)[1]]
        else:
            notInDb.append(i)  
    return notInDb, inDb
    

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

def printDebug(string):
    if debug:
        print(string)

app = Celery('tasks', backend='rpc://', broker=appBroker)

def mainFunction():
    values = getUserInput()
    angles = anglesToCheck(values)
    notInDb, inDb = checkDatabase(values, angles)
    printDebug('DB checked. In database:')
    
    #Check if list is not empty
    if notInDb:
        print "Creating meshes for angles"
        #createMeshes(values)
        #convertMeshes(angles)
    else:
        print "All angles already calculated"
    #'angle' = [drag, lift]
    returnAngles = {}
    workerAngles = {}
    for angle in angles:
        if angle in notInDb: 
            workerAngles[angle] = airfoil.delay('r0a' + str(angle) + 'n200.xml')
        else:
            returnAngles[angle] = inDb[angle]
    
    for angle in angles:
	if angle in notInDb:
	     #Wait for worker
	     while not workerAngles[angle].ready():
	          pass
             #Get result from worker
	     returnAngles[angle] = workerAngles[angle].get()
	     #Save result to db
	     insertResults(angle, returnAngles[angle][0], returnAngles[angle][1])
    return returnAngles

    

mainFunction()
