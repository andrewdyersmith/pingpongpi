# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import argparse

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='vtest.avi')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()
capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened:
  print('Unable to open: ' + args.input)
  exit(0)
while True:
  ret, frame = capture.read()
  if frame is None:
    break

  fgMask = backSub.apply(frame)


  cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
  cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
             cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
  

  cv.imshow('Frame', frame)
  cv.imshow('FG Mask', fgMask)
  
  keyboard = cv.waitKey(30)
  if keyboard == 'q' or keyboard == 27:
      break

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320, 240))
if args.algo == 'MOG2':
  backSub = cv.createBackgroundSubtractorMOG2()
else:
  backSub = cv.createBackgroundSubtractorKNN()
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    # show the frame
    sleep(1)
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
      break
