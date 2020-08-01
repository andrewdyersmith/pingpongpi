#!env/bin/python -u
import math
import time
import board
import neopixel
from PIL import Image
from multiprocessing import Process,Queue
from multiprocessing.connection import Listener
import zmq
from game_of_life import GameOfLifePlayer
from text_player import TextPlayer
from gif_player import GifPlayer
from fire_player import FirePlayer
from plasma_player import PlasmaPlayer
from camera_player import CameraPlayer
from water_player import WaterPlayer

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18


# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB


WIDTH=10
HEIGHT=15


class Screen:
  def __init__(self, width, height):
    self.width=width
    self.height=height
    # The number of NeoPixels
    self.num_pixels = width * height

    self.pixels = neopixel.NeoPixel(
  pixel_pin, self.num_pixels, brightness=0.7, auto_write=False, pixel_order=ORDER
)


  def show(self):
    self.pixels.show()
    
  def write_pixel(self,x,y,r,g,b):
    """ writes a pixel in the x,y position, based on a string of neopixels laid
    out in a continuous line like this:
  
    ____________________
                         \
     ____________________/
    /
    \____________________
    """
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      # don't write outside bounds
      return
    
    # work out the row direction
    if y % 2==0:
      # left to right
      self.pixels[int(x + (y * self.width))] = (max(0,min(255,int(r))),max(0,min(255,int(g))),max(0,min(255,int(b))))
    else:
      # right to left
      self.pixels[int(((y+1) * self.width)  - (x+1))] = (max(0,min(255,int(r))),max(0,min(255,int(g))),max(0,min(255,int(b))))

  def clear(self):
    self.pixels.fill(000)

class Rainbow:
  def __init__(self, frequency):
    """ frequency is number of loops through the whole rainbow per second."""
    self.frequency=frequency

  def update(self, screen, time):
    start_position = (time / self.frequency) % 1
    for x in range(0,screen.width):
      r = int(255 * (math.sin(( x/screen.width+start_position) * 2 * math.pi) + 1)/2)
      g = int(255 * (math.sin(( x/screen.width+start_position + 1/3) * 2 * math.pi) + 1)/2)
      b = int(255 * (math.sin(( x/screen.width+start_position + 2/3) * 2 * math.pi) + 1)/2)
      for y in range(0,screen.height):
        screen.write_pixel(x,y,r,g,b)
    

class ScreenOffPlayer:
  def __init__(self):
    pass
  def update(self, screen):
    for y in range(0, screen.height):
      for x in range(0, screen.width):
        screen.write_pixel(x, y, 0, 0, 0)
                         

message_queue = Queue()
message_process = Process()

def message_loop(message_queue):
  print("Starting message listener")
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")

  while True:
    #  Wait for next request from client
    message = socket.recv_json()
    print("Received request: %s" % message)
    if message:
      message_queue.put(message)
    socket.send(b"OK")

    
def setup_ipc():
  global message_process
  global message_queue
  message_process = Process(target=message_loop, args=(message_queue,))
  message_process.start()

MODE_RAINBOW = "rainbow"
MODE_GIF = "gif"
MODE_TEXT = "text"
MODE_GAME_OF_LIFE = "game-of-life"
MODE_PLASMA = "plasma"
MODE_FIRE = "fire"
MODE_WATER = "water"
MODE_CAMERA = "camera"
MODE_OFF = "off"

def main():
  global message_queue
  global message_process
  
  screen = Screen(WIDTH,HEIGHT)
  rainbow = Rainbow(1.0)
  gifplayer = GifPlayer("../assets/isaac.gif", 0.1)
  textplayer = TextPlayer("Hello world")
  plasmaplayer = PlasmaPlayer(WIDTH,HEIGHT)
  gameoflifeplayer = GameOfLifePlayer(WIDTH,HEIGHT)
  offplayer = ScreenOffPlayer()
  fireplayer = FirePlayer(WIDTH,HEIGHT)
  camera_player = CameraPlayer(0.1)
  waterplayer = WaterPlayer(WIDTH,HEIGHT)
  start_time = time.time()
  mode = MODE_RAINBOW
  
  setup_ipc()
  while True:
    t = time.time() - start_time
    if mode==MODE_RAINBOW:
      rainbow.update(screen, t)
    elif mode==MODE_GIF:
      gifplayer.update(screen, t)
    elif mode==MODE_TEXT:
      textplayer.update(screen, t)
    elif mode==MODE_GAME_OF_LIFE:
      gameoflifeplayer.update(screen, t)
    elif mode==MODE_FIRE:
      fireplayer.update(screen, t)
    elif mode==MODE_PLASMA:
      plasmaplayer.update(screen, t)
    elif mode==MODE_WATER:
      waterplayer.update(screen, t)
    elif mode==MODE_CAMERA:
      camera_player.update(screen, t)
    elif mode==MODE_OFF:
      offplayer.update(screen)
    screen.show()
    # do something with msg
    if not message_queue.empty():
      msg = message_queue.get()
      if msg:
        if msg[0] == 'close':
          
          break
        if msg[0]=="mode":
          if len(msg)>1:
            mode = msg[1]
            if mode==MODE_TEXT and len(msg)>2:
              textplayer.text = msg[2]
            if mode==MODE_CAMERA:
              camera_player.start()
            elif camera_player.running():
              # camera was running, but now it shouldn't
              camera_player.stop()
  message_process.join()

    
if __name__ == "__main__":
  main()
