from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello"


@app.route('/rend', methods=['GET'])
def get_content():
    return "tbd", 200


app.run()
