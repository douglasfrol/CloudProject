from flask import Flask, jsonify
import time
app = Flask("master")
dir_files = 'files_info/'

@app.route('/')
def hello_world():
    return 'Hello, Slave!'

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
    #update files

    #see if it is time for a scale up

    #call webhook to activate action

    return jsonify(1)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
