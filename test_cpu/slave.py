import requests, flask, psutil, time, re, signal, sys

from random import randint
UUID = randint(0, 100000)
patToFile = "file_ip.txt"
fileStream = open(patToFile, 'r')
UUID_str = str(UUID)
ip_to_master = ''
url = 'http://'
run = True

def make_call(url_link, value):
    r = requests.get(url_link+cpu_in_string)
    response_json = r.json()
    return response_json

try:
    with fileStream as openFile:
        for line in openFile:
            if line != '\n':
                ip_to_master = re.sub('[^0-9.]+', '', line)
                url += ip_to_master+':5000/slave/'+UUID_str+'/'
                make_call(url, 'N')
except Exception as e:
    print "nu blev det GALET"
    print e
finally:
    fileStream.close()

def signal_handler(signal, frame):
        global run
        print('quitting')
        run = False

signal.signal(signal.SIGINT, signal_handler)




try
    while run:
        cpu = psutil.cpu_percent(interval=5, percpu=False)
        cpu_in_string = str(cpu)
        response = make_call(url, cpu_in_string)

        print response
        time.sleep(1)
except Exception as e:
    print e
finally:
    make_call(url, 'Q')
    print response_json
    time.sleep(1)
