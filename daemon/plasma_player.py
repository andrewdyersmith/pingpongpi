from PIL import Image
import math
import colorsys

from time import sleep

class PlasmaPlayer:
  def __init__(self, width,height):
    self.width = width
    self.height = height
    
  def update(self, screen, time):
    for x in range (self.width):
      for y in range(self.height):
        hue = 4.0 + math.sin(x  + time/3) + math.sin(y / 2.0 + math.sqrt(time/4)) \
              + math.sin((x + y) / 3 + time) + math.sin(math.sqrt(x**2.0 + y**2.0) / 4.0 + time)
        hsv = colorsys.hsv_to_rgb(hue/6.0, 1, 1)
        screen.write_pixel(x, y,round(hsv[0] * 255.0),round(hsv[1] * 255.0),round(hsv[2] * 255.0))


def main():
  from fake_screen import FakeScreen
  textplayer = PlasmaPlayer(10,15)
  screen = FakeScreen(10,15)
  for i in range(0,1000):
    textplayer.update(screen,i/10)
    screen.show()
    sleep(0.1)

if __name__ == "__main__":
    main()
