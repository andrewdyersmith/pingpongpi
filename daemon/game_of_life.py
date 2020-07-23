import random
import os
from time import sleep

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
    self.last_time = time
    
    old_grid = self.grid.copy()
    no_change=True
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
            no_change=False
            self.grid[i][j] = OFF
        else: 
          if total == 3:
            no_change=False
            self.grid[i][j] = ON
        if self.grid[i][j]==ON:
          screen.write_pixel(i,j,255,255,255)
        else:
          screen.write_pixel(i,j,0,0,0)
    if no_change:
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
