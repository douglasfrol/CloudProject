from flask import Flask, jsonify
import time, os, requests
app = Flask("master")

webhook_url_up = ""
webhook_url_down = ""
webhook_token = ""

#######################
#
#
# Fulare kod kan man leta efter.....
#
#
#
#######

@app.route('/')
def hello_world():
    return 'Hello, Slave!'

def check_writable(path):
    try:
        return os.access(path, os.W_OK)
    except Exception as e:
        print 'not allowed to write in folder'
        print e
    return False

def file_exists(path_file):
        return os.path.exists(path_file)

def getFiles(path_files):

    try:
        filesInDir = os.listdir(path_files)
        return filesInDir
    except Exception as e:
        print e

    return []

def create_file(path, slave_id, cpu):
    file_status = file_exists(path+str(slave_id))
    if check_writable(path) and not file_status:
        try:
            f = open(path+str(slave_id), 'w')
            f.write(str(slave_id)+','+str(cpu)+','+str(time.time()))
            f.close()
            return True
        except Exception as e:
            print 'wrong in create_file() ----> error'
            print e

    return False

def get_info_in_file(path_file):
    fileStream = open(path_file, 'r')
    try:
        with fileStream as openFile:
            for line in openFile:
                if line != '\n':
                    return line.split(",")

    except Exception as e:
        print '---> galet i get_info_in_file()'
        print e

    return

def read_files(path_files):
    ret = []
    files = getFiles(path_files)
    for f in files:
        if f[0] != '.' and  f[0] != '0':
            info = get_info_in_file(path_files+f)
            info = [int(info[0]),float(info[1]),float(info[2])]
            ret.append(info)
    return ret

def update_file(path, slave_id, cpu):
    if file_exists(path) and check_writable(path+str(slave_id)):
        try:
            f = open(path+str(slave_id), 'w')
            f.write(str(slave_id)+','+str(cpu)+','+str(time.time()))
            f.close()
            return True
        except Exception as e:
            print 'Wrong in update_file() ---> error'
            print e

    return False

def delete_file(file_path):

    if file_exists(file_path):
        os.remove(file_path)
        return True

    return False

def clear_dir(path):

    files = getFiles(path)
    for f in files:
        if f[0] != '.':
            delete_file(path+f)

def determin_scaleing(slave_info):
    s_upp = 90 # Cpu
    s_down = 30 #Cpu
    time_lim = 180
    dir_file = 'files_info/0'
    scale_flag = -1
    for slave in slave_info:
        if slave[1] is not None and slave[2] is not None:
            if slave[1] > s_upp and slave[2] > time.time()-time_lim and scale_flag != 0:
                scale_flag = 1
            elif slave[1] < s_down and slave[2] > time.time()-time_lim :
                scale_flag = 0

    if scale_flag == 1:
        info_master = get_info_in_file(dir_file)
        if int(info_master[1]) == 1 and float(info_master[2]) < time.time()-(90):

            headers = {
                'X-Auth-Token': webhook_token,
            }
            requests.post(webhook_url_up, headers=headers)

            print 'time to scale upp'
        elif int(info_master[1]) == 0:
            update_file('files_info/', 0, 1)
    elif scale_flag == 0:
        info_master = get_info_in_file(dir_file)
        if int(info_master[1]) == 0 and float(info_master[2]) < time.time()-(90):

            headers = {
                'X-Auth-Token': webhook_token,
            }
            requests.post(webhook_url_down, headers=headers)

            print 'time to scale down'
        elif int(info_master[1]) == 1:
            update_file('files_info/', 0, 0)


@app.route('/slave/<int:slave_id>/<string:action>')
def get_info(slave_id, action):
    dir_files = 'files_info/'
    if action == 'Q':
        print 'quitting slave'
        print slave_id
        print delete_file(dir_files+str(slave_id))
    elif action == 'N':
        print 'new user'
        print slave_id
        print create_file(dir_files, slave_id, 0.0)
    else:
        print 'not a good input'
        return jsonify(0)

    return jsonify(1)


@app.route('/slave/<int:slave_id>/<float:cpu>')
def get_info_cpu(slave_id, cpu):
    dir_files = 'files_info/'
    print slave_id
    print cpu

    if update_file(dir_files, slave_id, cpu) is None:
        print "it went crazy ", slave_id, cpu
        return jsonify(0)

    info_slaves = read_files(dir_files)
    if info_slaves is not None:
        determin_scaleing(info_slaves)

    return jsonify(1)

if __name__ == '__main__':
    clear_dir('files_info/')
    create_file('files_info/', 0, 0)
    app.run(host= '0.0.0.0', debug=True)
