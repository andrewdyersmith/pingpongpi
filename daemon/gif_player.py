from PIL import Image
from time import sleep

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
                                                                                      

def main():
  from fake_screen import FakeScreen
  gifplayer = GifPlayer("../assets/mario.gif",0.1)
  screen = FakeScreen(10,15)
  for i in range(0,1000):
    gifplayer.update(screen,i/10)
    screen.show()
    sleep(0.1)

if __name__ == "__main__":
    main()
