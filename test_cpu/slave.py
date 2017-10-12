import requests, flask, psutil, time

from random import randint
UUID = randint(0, 10000)

UUID_str = str(UUID)
url = 'http://130.239.81.63:5000/slave/'+UUID_str+'/'
for i in range(100):
    cpu = psutil.cpu_percent(interval=1, percpu=True)
    cpu_in_string = str(cpu[0])
    r = requests.get(url+cpu_in_string)
    response_json = r.json()
    print response_json
    time.sleep(1)
