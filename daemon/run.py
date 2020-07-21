#!env/bin/python -u
import math
import time
import board
import neopixel
from PIL import Image

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18


# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB


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

    # work out the row direction
    if y % 2==1:
      # left to right
      self.pixels[int(x + (y * self.width))] = (r,g,b)
    else:
      # right to left
      self.pixels[int((y+1) * self.width  - (x+1))] = (r,g,b)



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
    self.image = Image.open(file).convert('RGB')
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
    frame_num = (time/time_per_frame) % self.num_frames
    self.image.seek(frame_num)
    for y in range(0, min(self.image.format.height, screen.height)):
      for x in range(0, min(self.image.format.width, screen.width)):
        r,g,b = self.image.getpixel(x,y)
        screen.write_pixel(x, y, r, g, b)
                         
def wheel(pos):
  # Input a value 0 to 255 to get a color value.
  # The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    r = g = b = 0
  elif pos < 85:
    r = int(pos * 3)
    g = int(255 - pos * 3)
    b = 0
  elif pos < 170:
    pos -= 85
    r = int(255 - pos * 3)
    g = 0
    b = int(pos * 3)
  else:
    pos -= 170
    r = 0
    g = int(pos * 3)
    b = int(255 - pos * 3)
  return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
  for j in range(255):
    for i in range(num_pixels):
      pixel_index = (i * 256 // num_pixels) + j
      pixels[i] = wheel(pixel_index & 255)
    pixels.show()
    time.sleep(wait)

def main():
  screen = Screen(10,15)
  rainbow = Rainbow(1.0)
  start_time = time.time()
  while True:
    rainbow.update(screen,time.time()-start_time)
    screen.show()
    
if __name__ == "__main__":
  main()
