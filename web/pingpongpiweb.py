from flask import Flask, render_template
from multiprocessing.connection import Client

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/mode/<name>')
def mode(name):
  conn.send([MODE,name])
  return "\"OK\""

conn=None
@app.before_first_request
def setup_ipc():
  global conn
  address = ('localhost', 6000)
  conn = Client(address, authkey='secret password')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
