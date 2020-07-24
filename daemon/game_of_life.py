import random
import os
from time import sleep
import colorsys
import math

ON=1
OFF=0

class GameOfLifePlayer:
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.last_time = 0
    self.reset()

  def reset(self):
    self.grid = [random.choices([0,1],[0.9,0.1],k=self.height) for x in range(0,self.width)]

  def update(self, screen, time):
    if time<self.last_time+0.1:
      return
    if time>1000:
      self.reset()
    self.last_time = time
    
    old_grid = self.grid.copy()
    changes=0
    for i in range(self.width): 
      for j in range(self.height): 
  
        # compute 8-neghbor sum 
        # using toroidal boundary conditions - x and y wrap around  
        # so that the simulaton takes place on a toroidal surface. 
        total =(old_grid[i]               [(j-1)%self.height] + old_grid[i]               [ (j+1)%self.height] + 
                old_grid[(i-1)%self.width][j]                 + old_grid[(i+1)%self.width][ j] + 
                old_grid[(i-1)%self.width][(j-1)%self.height] + old_grid[(i-1)%self.width][ (j+1)%self.height] + 
                old_grid[(i+1)%self.width][(j-1)%self.height] + old_grid[(i+1)%self.width][ (j+1)%self.height])
        # apply Conway's rules
        if old_grid[i][j]  == ON: 
          if (total < 2) or (total > 3):
            changes+=1
            self.grid[i][j] = OFF
        else: 
          if total == 3:
            changes+=1
            self.grid[i][j] = ON
        if self.grid[i][j]==ON:
          hue = 4.0 + math.sin(i  + time/2) + math.sin(j / 2.0 + math.sqrt(time/4)) \
                + math.sin((i + j) / 2 + time) + math.sin(math.sqrt(i**2.0 + j**2.0) / 1.275 + time)
          hsv = colorsys.hsv_to_rgb(hue/6.0, 1, 1)
          screen.write_pixel(i, j,round(hsv[0] * 255.0),round(hsv[1] * 255.0),round(hsv[2] * 255.0))

        else:
          screen.write_pixel(i,j,0,0,0)
    if changes<3:
      self.reset()
            
def main():
  from fake_screen import FakeScreen
  gameplayer = GameOfLifePlayer(10,10)
  screen = FakeScreen(10,10)
  for i in range(0,100):
    gameplayer.update(screen,i)
    screen.show()
    sleep(0.1)

if __name__ == "__main__":
    main()
