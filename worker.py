from celery import celery
import subprocess
from calcAverageForce import *

hostIP = '129.16.125.231'
brokerURL = 'amqp://guest@localhost/'
sshKey = '/home/ubuntu/dofr_keypair.pem'
airfoilDirectory = '/home/ubuntu/murtazo/navier_stokes_solver'

app = Celery('tasks', broker=brokerURL , backend='amqp://')

@app.task
def airfoil(filename):
	hostXmlLocation = 'ubuntu@' + hostIP + ':/home/ubuntu/murtazo/cloudnaca/msh/' + filename
	scpStrings = ['sudo', 'scp', '-i', sshKey, hostXmlLocation, airfoilDirectory]
	subprocess.call(scpStrings, cwd = airfoilDirectory)

	airfoilStrings = ['./airfoil', '10', '0.0001', '10.', '1', airfoilDirectory + filename]
	subprocess.call(airfoilStrings, cwd = airfoilDirectory)
	avg_drag, avg_lift = calcAvgLiftAndDrag()
	return avg_drag, avg_lift






