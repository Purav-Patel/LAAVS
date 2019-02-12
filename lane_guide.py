# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)

count = 0
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
boundaries = [([0, 0, 0], [20, 20, 255])]
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	#to save picture#camera.capture('foo.jpg')
	
	fram = image[400:450,340:480] #checking
	framx = image[400:650,0:640] #dis
	framd = image[300:450,340:480] #dis
    # Print perticular color
	for (lower,upper) in boundaries:
	 # create NumPy arrays from the boundaries
		lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        # find the colors within the specified boundaries and apply the mask
        mask = cv2.inRange(fram, lower, upper)
        
        output = cv2.bitwise_and(fram, fram, mask = mask)
        count = 0
        for i in range(0,50):
			for j in range(140):
				px = output[i,j]

				# Store BGR pixel value in list
				lst =list (px)
				blue = lst[0]
				green = lst[1]
				red = lst[2]
				if (blue>=0 and green>=0 and red>=75):
					count += 1
		
				
		
				 
	# show the frame
	cv2.imshow("Frame", output)
	cv2.imshow("Frame2", framx)
	cv2.imshow("Frame3", framd)
	if (count > 100):
		print("True\t%d"%count)
		GPIO.output(3,1)
		GPIO.output(5,1)
		GPIO.output(7,1)

	else:
		print("False\t%d"%count)
		GPIO.output(3,0)
		GPIO.output(5,0)
		GPIO.output(7,0)

	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	#print lst
	if key == ord("q"):
		break
