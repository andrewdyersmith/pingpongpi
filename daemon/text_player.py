from PIL import Image

from time import sleep

characters = " !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
class TextPlayer:
  def __init__(self, text):
    self.text = text
    self.font_sheet = Image.open("../assets/font.png").convert("RGB")

  def update(self, screen, time):
    screen.clear()
    pos = (time / 0.5) % len(self.text)
    offset = -8 * (pos-1)
    for i in range(0, len(self.text)):
      char_to_print = self.text[i]
      self.print_char(screen, char_to_print, offset + i*8, 3)
      
  def print_char(self, screen, char, pos_x, pos_y):
    i = characters.index(char)
    u = int(i % 16) * 8
    v = int(i / 16) * 12
    for y in range(0, 12):
      for x in range(0, 8):
        r,g,b = self.font_sheet.getpixel((x + u,y + v))
        if r>30 or g>30 or b > 30:
          screen.write_pixel(int(pos_x + x), int(pos_y + y), r, g, b)


def main():
  from fake_screen import FakeScreen
  textplayer = TextPlayer("Hello world")
  screen = FakeScreen(10,15)
  for i in range(0,1000):
    textplayer.update(screen,i/10)
    screen.show()
    sleep(0.1)

if __name__ == "__main__":
    main()
