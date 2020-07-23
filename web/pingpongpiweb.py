from flask import Flask, render_template, appcontext_tearing_down, request
from multiprocessing import Process, Queue
from multiprocessing.connection import Client
import atexit
import time
import zmq

app = Flask(__name__)




@app.route('/')
def index():
  return render_template('index.html')

MODE="mode"

@app.route('/mode/<name>', methods=['POST'])
def mode(name):
  text = request.args.get("val", default="", type=str)
  message_queue.put([MODE,name,text])
  return "\"OK\""

message_queue = Queue()
message_process = None

def message_loop(message_queue):
  print("Starting message loop")
  context = zmq.Context()
  while True:
    try:
      socket = context.socket(zmq.REQ)
      socket.connect("tcp://localhost:5555")
      print("Connected to daemon")
      while True:
        msg = message_queue.get()
        print("Sending ", msg)
        socket.send_json(msg)
        socket.recv()
    except Exception as ex:
      print(ex)
    time.sleep(5)


def stop_message_loop():
  print("Terminating")
  if message_process:
    message_process.terminate()

atexit.register(stop_message_loop)

    
@app.before_first_request
def setup_ipc():
  global message_process
  message_process = Process(target=message_loop, args=(message_queue,))
  message_process.start()


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
