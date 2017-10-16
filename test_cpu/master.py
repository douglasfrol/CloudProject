from flask import Flask, jsonify
import time, os
app = Flask("master")
dir_files = 'files_info/'

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

def create_file(slave_id, cpu):
    file_status = file_exists(path+slave_id)
    if check_writable(dir_files) and not file_status:
        try:
            f = open('myfile', 'w')
            f.write('hi there\n')  # python will convert \n to os.linesep
            f.close()
            return True
        except Exception as e:
            print 'wrong in create_file() ----> error'
            print e
    elif file_status:
        return False

    return False

def read_files():

    return

def update_file(slave_id, cpu):

    return

def delete_file(slave_id):

    return

@app.route('/slave/<int:slave_id>/<string:action>')
def get_info(slave_id, action):
    if action == 'Q':
        print 'quitting slave'
        print slave_id
        #remove file in dir
    elif action == 'N':
        print 'new user'
        print slave_id
        #create file in dir
    else:
        print 'not a good input'
        return jsonify(0)
    #determin if the new caller is unique
    return jsonify(1)


@app.route('/slave/<int:slave_id>/<float:cpu>')
def get_info_cpu(slave_id, cpu):
    print slave_id
    print cpu

    if update_file(slave_id, cpu) is None:
        print "it went crazy ", slave_id, cpu
        return 0

    info_slaves = read_files()
    if info_slaves is not None:
        #iterate over array and se if it is time for a scaleing
        #call webhook to activate action
        return

    return jsonify(1)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
