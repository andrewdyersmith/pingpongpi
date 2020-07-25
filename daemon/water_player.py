from PIL import Image
import math
import colorsys
import random

from time import sleep

class WaterPlayer:
  def __init__(self, width,height):
    self.width = width
    self.height = height
    self.caustic = Image.open("../assets/caustics-texture.gif").resize((32,32))
    self.vec1 =[random.uniform(-0.2,0.2),random.uniform(-0.1,0.1)]
    self.pos1 = [0,0]
    self.size1 = random.random() + 0.5
    self.vec2 =[random.uniform(-0.5,0.5),random.uniform(-0.1,0.1)]
    self.pos2 = [0,0]
    self.size2 = random.random() + 0.5
    
  def update(self, screen, time):
    self.pos1[0] += self.vec1[0] * self.size1
    self.pos1[1] += self.vec1[1] * self.size1
    self.pos2[0] += self.vec2[0] * self.size2
    self.pos2[1] += self.vec2[1] * self.size2
  
    for x in range (self.width):
      for y in range(self.height):
        c1 =self.caustic.getpixel(((self.pos1[0]+x*self.size1)%self.caustic.size[0],(self.pos1[1]+y*self.size1) % self.caustic.size[1] ))
        c2 =self.caustic.getpixel(((self.pos2[0]+x*self.size2)%self.caustic.size[0],(self.pos2[1]+y*self.size2) % self.caustic.size[1] ))
        screen.write_pixel(x,y,0,0,32+min(255,min(c1,c2)))
                                                                                                  

def main():
  from fake_screen import FakeScreen
  waterplayer = WaterPlayer(10,15)
  screen = FakeScreen(10,15)
  for i in range(0,1000):
    waterplayer.update(screen,i/10)
    screen.show()
    sleep(0.1)

if __name__ == "__main__":
    main()
