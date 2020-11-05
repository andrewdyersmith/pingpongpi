import os

FAKE_COLORS = [" ","░","▒","▓"]
class FakeScreen:
  """ Pretends to be a screen for quickly checking the plugin looks roughly ok
      without having to deploy to the screen."""
  def __init__(self, width, height):
    self.pixels = [[(0,0,0) for y in range(0,height)] for x in range(0,width)]
    self.width = width
    self.height = height
    
  def write_pixel_tuple(self, x,y,c):
    self.write_pixel(x,y,c[0],c[1],c[2])
    
  def write_pixel(self, x,y,r,g,b):
    if x < 0 or y < 0 or x >= self.width or y >= self.height:
      # don't write outside bounds
      return

    self.pixels[x][y]=(r,g,b)

  def show(self):
    os.system('clear')
    for j in range(0,self.height):
      for i in range(self.width):
        c = int(3*self.pixels[i][j][0]/255.0)
        print(FAKE_COLORS[c], end="")
      print("")
          

  def clear(self):
    for i in range(0,self.width):
      for j in range(self.height):
        self.pixels[i][j] = (0,0,0)
