import colorsys
import io
import time
import threading
import picamera
import picamera.array
import cv2
import numpy
from time import sleep
from PIL import Image, ImageEnhance
"""
class ImageProcessor(threading.Thread):
  def __init__(self, owner):
    super(ImageProcessor, self).__init__()
    self.stream = io.BytesIO()
    self.event = threading.Event()
    self.terminated = False
    self.owner = owner
    self.start()
    
    
  def run(self):
    # This method runs in a separate thread
    while not self.terminated:
      # Wait for an image to be written to the stream
      if self.event.wait(1):
        try:
          self.stream.seek(0)
          # Read the image and do some processing on it
          img = Image.open(self.stream)
          cropped_img = img.crop((35,0,110,100)).resize((10,15))
          #enhancer = ImageEnhance.Brightness(cropped_img)
          img_array = numpy.array(cropped_img)
          im_output = self.owner.back_sub.apply(img_array)
          #factor = 0.6 #gives original image
          #im_output = enhancer.enhance(factor)
          self.owner.next_image=im_output
          #...
          #...
          # Set done to True if you want the script to terminate
          # at some point
          #self.owner.done=True
        finally:
          # Reset the stream and event
          self.stream.seek(0)
          self.stream.truncate()
          self.event.clear()
          # Return ourselves to the available pool
          with self.owner.lock:
            self.owner.pool.append(self)
          
class ProcessOutput(object):
  def __init__(self):
    self.done = False
    # Construct a pool of 4 image processors along with a lock
    # to control access between threads
    self.lock = threading.Lock()
    self.pool = [ImageProcessor(self) for i in range(4)]
    self.processor = None
    self.current_image=None
    self.next_image=None
    self.back_sub = cv2.createBackgroundSubtractorMOG2()

  def write(self, buf):
    if buf.startswith(b'\xff\xd8'):
      # New frame; set the current processor going and grab
      # a spare one
      if self.processor:
        self.processor.event.set()
      with self.lock:
        if self.pool:
          self.processor = self.pool.pop()
        else:
          # No processor's available, we'll have to skip
          # this frame; you may want to print a warning
          # here to see whether you hit this case
          self.processor = None
    if self.processor:
      self.processor.stream.write(buf)

  def stop(self):
    self.done=True
    self.flush()
    
  def flush(self):
    # When told to flush (this indicates end of recording), shut
    # down in an orderly fashion. First, add the current processor
    # back to the pool
    if self.processor:
      with self.lock:
        self.pool.append(self.processor)
        self.processor = None
    # Now, empty the pool, joining each thread as we go
    while True:
      with self.lock:
        try:
          proc = self.pool.pop()
        except IndexError:
          return
      proc.terminated = True
      proc.join()
"""

class ProcessOutput(picamera.array.PiRGBAnalysis):
  def __init__(self, camera):
    super().__init__(camera)
    self.next_image=None
    self.back_sub = cv2.createBackgroundSubtractorMOG2()

    
  def analyse(self, array):
    im_output = self.back_sub.apply(array)
    self.next_image=im_output
                                
                          
class CameraPlayer:
  def __init__(self, time_per_frame):
    self.time_per_frame = time_per_frame
    self.running=False

  def start(self):
    print("Start")
    self.camera_processor = None
    self.thread = threading.Thread(target=self.run, args=())
    self.thread.start()


  def stop(self):
    print("Stopping")
    self.running=False
    #self.camera_processor.stop()
    #self.thread.join()
    
  def run(self):
    print("Starting thread")
    self.running=True
    try:
      with picamera.PiCamera(resolution=(160,120)) as camera:
        self.camera_processor = ProcessOutput(camera)
        camera.zoom=(0.2,0.3,0.6,0.45)
        camera.start_preview()
        time.sleep(2)
        camera.start_recording(self.camera_processor , format='rgb')
        while self.running:
          camera.wait_recording(1.0/15)
        camera.stop_recording()
    finally:
      camera.close()

  def update(self, screen, time):
    if self.camera_processor and not self.camera_processor.next_image is None:
      current_image = self.camera_processor.next_image
      self.camera_processor.next_image = None

      for y in range(0, min(current_image.shape[1], screen.height)):
        for x in range(0, min(current_image.shape[0], screen.width)):
          pix = current_image[9-x,y]
          #r,g,b = colorsys.hsv_to_rgb(pix[0],pix[1],pix[2])
          screen.write_pixel(x, y, pix,pix,pix)#r, g, b)

def main():
  from fake_screen import FakeScreen
  camera_player = CameraPlayer(0.1)
  screen = FakeScreen(10,15)
  camera_player.start()
  for i in range(0,28):
    camera_player.update(screen,i/10)
    screen.show()
    sleep(0.1)
  camera_player.stop()
  
if __name__ == "__main__":
    main()
