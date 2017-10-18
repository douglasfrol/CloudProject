import requests, flask, psutil, time, re, signal, sys

from random import randint
UUID = randint(2, 1000000)
patToFile = "file_ip.txt"
fileStream = open(patToFile, 'r')
UUID_str = str(UUID)
ip_to_master = ''
run = True
failed_con = 0

def make_call(url_link, value):
    global failed_con
    try:
        r = requests.get(url_link+value)
        response_json = r.json()
    except Exception as e:
        failed_con += 1
        return
    failed_con = 0
    return response_json

def signal_handler(signal, frame):
        global run
        print('quitting')
        run = False

def get_url():
    url = 'http://'
    try:
        with fileStream as openFile:
            for line in openFile:
                if line != '\n':
                    ip_to_master = re.sub('[^0-9.]+', '', line)
                    url += ip_to_master+':5000/slave/'+UUID_str+'/'
    except Exception as e:
        print "nu blev det GALET"
        print e
        return
    finally:
        fileStream.close()
    return url


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    url = get_url()
    make_call(url, 'N') # init new slave
    try:
        while run:
            cpu = psutil.cpu_percent(interval=5, percpu=False)
            cpu_in_string = str(cpu)
            response = make_call(url, cpu_in_string)
            if response is None and failed_con < 10:
                print 'problem med att ansluta till server'
                time.sleep(2)
            elif failed_con >= 10:
                break
            elif response != 1:
                print 'galet med respons --> mastern'
            else:
                print 'the response was: ', response
            time.sleep(15)

    except Exception as e:
        print e
    finally:
        print 'quitting'
        res = make_call(url, 'Q')
        time.sleep(1)
