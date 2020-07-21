from flask import Flask, render_template
from multiprocessing import Process, Queue
from multiprocessing.connection import Client

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/mode/<name>')
def mode(name):
  global message_queue
  message_queue.put([MODE,name])
  return "\"OK\""

message_queue = Queue
message_process = None

def message_loop(message_queue):
  address = ('localhost', 6000)
  conn = Client(address, authkey=b'secret password')
  print('connection made to', listener.last_accepted)
  while True:
    msg = message_queue.get()
    conn.send(msg)
    
@app.before_first_request
def setup_ipc():
  global message_process
  global message_queue
  message_process = Process(target=message_loop, args=(message_queue,))
  message_process.start()


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
