from PIL import Image
import math
import colorsys

from time import sleep

class SnakesPlayer:
  def __init__(self, width,height):
    self.width = width
    self.height = height
    self.worm = []
    self.apple = None

  def add_apple(self):
    """ Returns true if we could place an apple."""
    valid_spot = False
    proposed_spot = None
    max_spots = self.width * self.height
    spot_trys = 0
    while not valid_spot and spot_trys < max_spots:
      proposed_spot = (random.randint(0,self.width), random.nextint(0,self.height))
      if not proposed_spot in self.worm:
        valid_spot = True
      else:
        spot_trys += 1
    if spot_trys>=max_spots:
      # whoa we ran out of places to put the apple!
      return false
    else:
      self.apple = proposed_spot
      
  def update(self, screen, time):
    if not self.apple:
      self.add_apple()

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
