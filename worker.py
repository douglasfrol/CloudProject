from celery import Celery
import subprocess
from calcAverageForce import *

hostIP = '129.16.125.241'
brokerURL = 'amqp://user:pwd@' + hostIP + ':5672/vhost'
sshKey = '/home/ubuntu/dofr_keypair.pem'
airfoilDirectory = '/home/ubuntu/murtazo/navier_stokes_solver/'
mshDirectory = '/home/ubuntu/murtazo/cloudnaca/msh/'

app = Celery('tasks', broker=brokerURL , backend='amqp://')

@app.task
def airfoil(filename):
	hostXmlLocation = 'ubuntu@' + hostIP + ':/home/ubuntu/murtazo/cloudnaca/msh/' + filename
	scpStrings = ['sudo', 'scp', '-i', sshKey, hostXmlLocation, mshDirectory]
	subprocess.call(scpStrings, cwd = airfoilDirectory)

	airfoilStrings = ['./airfoil', '10', '0.0001', '10.', '1', mshDirectory + filename]
	print airfoilStrings
	subprocess.call(airfoilStrings, cwd = airfoilDirectory)
	avg_drag, avg_lift = calcAvgLiftAndDrag()
	print airfoilStrings 
	return avg_drag, avg_lift






