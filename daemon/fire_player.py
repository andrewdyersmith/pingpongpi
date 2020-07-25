import random
import os
from time import sleep
import colorsys
import math

class FirePlayer:
  def __init__(self, width, height):
      self.width = width
      self.height = height + 1
      self.fire  = [[0 for y in range(0,self.height)] for x in range(0,self.width)]


  def update(self, screen, time):

    # randomize the bottom row of the fire buffer
    for x in range(0,self.width):
        self.fire[x][self.height-1] = random.random()
    
    # do the fire calculations for every pixel, from top to bottom
    for y in range(0,self.height):
      for x in range(0,self.width):

        self.fire[x][y] = (self.fire[(x - 1 + self.width) % self.width][(y + 1) % self.height]
                                       + self.fire[(x) % self.width][(y + 1) % self.height]
                                       + self.fire[(x + 1) % self.width][(y + 1) % self.height]
                                       + self.fire[(x) %self.width][(y + 2) % self.height]
                                     ) / 5.6
        
    for y in range(0,self.height):
      for x in range(0,self.width):
        hue = self.fire[x][y]/5 # 0-0.33 is red to yellow
        lightness = min(1.0,self.fire[x][y]*((y+5)/(self.height)))
        col = colorsys.hsv_to_rgb(hue,1,lightness)

        screen.write_pixel(x,y,256*col[0],256*col[1],256*col[2])

"""
  //generate the palette
  for(int x = 0; x < 256; x++)
  {
    //HSLtoRGB is used to generate colors:
    //Hue goes from 0 to 85: red to yellow
    //Saturation is always the maximum: 255
    //Lightness is 0..255 for x=0..128, and 255 for x=128..255
    color = HSLtoRGB(ColorHSL(x / 3, 255, std::min(255, x * 2)));
    //set the palette to the calculated RGB value
    palette[x] = RGBtoINT(color);
  }
"""

            
def main():
  from fake_screen import FakeScreen
  gameplayer = FirePlayer(10,10)
  screen = FakeScreen(10,10)
  for i in range(0,100):
    gameplayer.update(screen,i)
#    screen.show()
    sleep(0.2)

if __name__ == "__main__":
    main()
