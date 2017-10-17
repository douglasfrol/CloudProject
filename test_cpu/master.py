from flask import Flask, jsonify
import time, os
app = Flask("master")

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
            f.write(str([slave_id, cpu, time.time()]) )
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
            print openFile[0]
    except Exception as e:
        print '---> galet i get_info_in_file()'
        print e

    return

def read_files(path_files):

    files = getFiles(path_files)
    for f in files:
        if f[0] != '.':
            get_info_in_file(path_files+f)
    return

def update_file(path, slave_id, cpu):
    if file_exists(path) and check_writable(path+str(slave_id)):
        try:
            f = open(path+str(slave_id), 'w')
            f.write(str([slave_id, cpu, time.time()]))  # python will convert \n to os.linesep
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

@app.route('/slave/<int:slave_id>/<string:action>')
def get_info(slave_id, action):
    dir_files = 'files_info/'
    print 'got call'
    if action == 'Q':
        print 'quitting slave'
        print slave_id
        print delete_file(dir_files+str(slave_id))
        #remove file in dir
    elif action == 'N':
        print 'new user'
        print slave_id
        print create_file(dir_files, slave_id, 0.0)
        #create file in dir
    else:
        print 'not a good input'
        return jsonify(0)
    #determin if the new caller is unique
    return jsonify(1)


@app.route('/slave/<int:slave_id>/<float:cpu>')
def get_info_cpu(slave_id, cpu):
    dir_files = 'files_info/'
    print slave_id
    print cpu

    if update_file(dir_files, slave_id, cpu) is None:
        print "it went crazy ", slave_id, cpu
        return 0

    info_slaves = read_files(dir_files)
    if info_slaves is not None:
        #iterate over array and se if it is time for a scaleing
        #call webhook to activate action
        return

    return jsonify(1)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
