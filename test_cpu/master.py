from flask import Flask, jsonify
app = Flask("master")

@app.route('/')
def hello_world():
    return 'Hello, Slave!!!'

@app.route('/slave/<int:slave_id>')
def get_info(slave_id):
    print slave_id
    #determin if the new caller is unique
    return "u\n"


@app.route('/slave/<int:slave_id>/<float:cpu>')
def get_info_cpu(slave_id, cpu):
    print slave_id
    print cpu

    #see if it is time for a scale up
    #call webhook to activate action

    return jsonify(1)

if __name__ == '__main__':
    app.run(host= '0.0.0.0', debug=True)
