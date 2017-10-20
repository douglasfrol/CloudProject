from celery import Celery
import subprocess
from calcAverageForce import *

hostIP = '129.16.125.231'
brokerURL = 'amqp://guest@localhost/'
sshKey = '/home/ubuntu/dofr_keypair.pem'
airfoilDirectory = '/home/ubuntu/murtazo/navier_stokes_solver/'
mshDirectory = '/home/ubuntu/murtazo/cloudnaca/msh/'

app = Celery('tasks', broker=brokerURL , backend='amqp://')

@app.task
def airfoil(filename):
	#hostXmlLocation = 'ubuntu@' + hostIP + ':/home/ubuntu/murtazo/cloudnaca/msh/' + filename
	#scpStrings = ['sudo', 'scp', '-i', sshKey, hostXmlLocation, airfoilDirectory]
	#subprocess.call(scpStrings, cwd = airfoilDirectory)

	airfoilStrings = ['./airfoil', '10', '0.0001', '10.', '1', mshDirectory + filename]
	print airfoilStrings
	subprocess.call(airfoilStrings, cwd = airfoilDirectory)
	avg_drag, avg_lift = calcAvgLiftAndDrag()
	print airfoilStrings
	#return -1, -1 
	return avg_drag, avg_lift






