import random
import os
from time import sleep

ON=1
OFF=0

class GameOfLifePlayer:
  def __init__(self, width, height):
    self.grid = [random.choices([0,1],[0.8,0.2],k=height) for x in range(0,width)]
    self.width = width
    self.height = height
    print(self.grid)
        
  def update(self, screen, time):
    old_grid = self.grid.copy() 
    for i in range(self.width): 
      for j in range(self.height): 
  
        # compute 8-neghbor sum 
        # using toroidal boundary conditions - x and y wrap around  
        # so that the simulaton takes place on a toroidal surface. 
        total = int((old_grid[i][ (j-1)%self.height] + old_grid[i][ (j+1)%self.height] + 
                     old_grid[(i-1)%self.width][ j] + old_grid[(i+1)%self.width][ j] + 
                     old_grid[(i-1)%self.height][ (j-1)%self.height] + old_grid[(i-1)%self.width][ (j+1)%self.height] + 
                     old_grid[(i+1)%self.width][ (j-1)%self.height] + old_grid[(i+1)%self.width][ (j+1)%self.height])) 
        # apply Conway's rules
        if self.grid[i][j]  == ON: 
          if (total < 2) or (total > 3): 
            self.grid[i][j] = OFF 
        else: 
          if total == 3: 
              self.grid[i][ j] = ON
        if old_grid[i][j]==ON:
          screen.write_pixel(i,j,1,1,1)
        else:
          screen.write_pixel(i,j,0,0,0))
            

      print("")


def main():
  gameplayer = GameOfLifePlayer(10,10)
  while True:
    gameplayer.update(None,None)

if __name__ == "__main__":
    main()
