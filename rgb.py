from flask import Flask, request, render_template
from flask_sockets import Sockets
import gevent
import time
import json


app = Flask(__name__)
app.debug = True

sockets = Sockets(app)

clients = list()


class Client:
	def __init__(self):
		self.queue = gevent.queue.Queue()
	def put(self, v):
		self.queue.put_nowait(v)
	def get(self):
		return self.queue.get()

def send_all(msg):
	for client in clients:
		client.put(msg)


def read_ws(ws, client):
	while not ws.closed:
		gevent.sleep(0)
		try:
			msg = ws.receive() # This command blocks!
			print "WS RECEIVED: %s" % msg
			if(msg is None):
				client.put(msg)
			else
                send_all(msg)
		except:
			print "WS ERROR: read_ws exception"


@sockets.route('/subscribe')
def subscribe_socket(ws):
	client = Client() # User-defined object to store client info
	clients.append(client) 
	print '# Clients: {}'.format(len(clients))
	g = gevent.spawn( read_ws, ws, client)
	# If data is received by the queue, send it to the websocket
	try:
		while g:
			msg = client.get() # This command blocks!
			if msg is not None:
				ws.send(msg)
			else:
				break
	except Exception as e:
		print "WS ERROR: %s" % e
	finally:
		ws.close()
		clients.remove(client)
		gevent.kill(g)



@sockets.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message=ws.receive()
        ws.send(message)




@app.route('/')
def index():
	return render_template("index.html")
