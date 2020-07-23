#!env/bin/python -u
import math
import time
import board
import neopixel
from PIL import Image
from multiprocessing import Process,Queue
from multiprocessing.connection import Listener
import zmq

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18


# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB


WIDTH=15
HEIGHT=10


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
      self.pixels[int(x + (y * self.width))] = (r,g,b)
    else:
      # right to left
      self.pixels[int(((y+1) * self.width)  - (x+1))] = (r,g,b)

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
                         
class GifPlayer:
  def __init__(self, file, time_per_frame):
    self.file=file
    self.time_per_frame=time_per_frame
    self.image = Image.open(file)
    i=1
    try:
      while 1:
        self.image.seek(self.image.tell()+1)
        i += 1
        # do something to im
    except EOFError:
      pass # end of sequence
    self.num_frames = i
    
  def update(self, screen, time):
    frame_num = (time/self.time_per_frame) % self.num_frames
    self.image.seek(int(frame_num))
    rgb_im = self.image.convert("RGB")
    for y in range(0, min(self.image.size[1], screen.height)):
      for x in range(0, min(self.image.size[0], screen.width)):
        r,g,b = rgb_im.getpixel((x,y))
        screen.write_pixel(x, y, r, g, b)

characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
class TextPlayer:
  def __init__(self, text):
    self.text = text
    self.font_sheet = Image.open("../assets/font.png").convert("RGB")

  def update(self, screen, time):
    screen.clear()
    pos = (time / 0.5) % len(self.text)
    offset = -8 * (pos-1)
    for i in range(0, len(self.text)):
      char_to_print = self.text[i]
      self.print_char(screen, char_to_print, offset + i*8, 3)
      
  def print_char(self, screen, char, pos_x, pos_y):
    i = characters.index(char)
    u = int(i % 16) * 8
    v = int(i / 16) * 12
    for y in range(0, 12):
      for x in range(0, 8):
        r,g,b = self.font_sheet.getpixel((x + u,y + v))
        if r>30 or g>30 or b > 30:
          screen.write_pixel(int(pos_x + x), int(pos_y + y), r, g, b)
                                                                                      
    

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
MODE_OFF = "off"

def main():
  global message_queue
  global message_process
  
  screen = Screen(WIDTH,HEIGHT)
  rainbow = Rainbow(1.0)
  gifplayer = GifPlayer("../assets/isaac.gif", 0.1)
  textplayer = TextPlayer("Hello world")
  gameoflifeplayer = GameOfLifeplayer(WIDTH,HEIGHT))
  offplayer = ScreenOffPlayer()
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
  message_process.join()

    
if __name__ == "__main__":
  main()
