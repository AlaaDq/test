from flask import Flask, request, render_template
from flask_sockets import Sockets
import gevent
import time
import json


app = Flask(__name__)
app.debug = True

sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message=ws.receive()
        ws.send(message)


@app.route('/')
def index():
	return render_template("index.html")
