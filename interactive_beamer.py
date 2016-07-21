#!/usr/bin/python

import Tkinter as tk
from PIL import ImageTk
from PIL import Image
import os
import sys
import time
import threading
from time import sleep
try:
	import Adafruit_MPR121.MPR121 as MPR121
except:
	print "Could not import Adafruit Module"

root = tk.Tk()
root.attributes("-fullscreen", True)
stop = False
logging = True
log_path = "./log/touch.log"

available_keys = ["a","d","f","g","s","w"]

name = os.path.join("Images","base_image.png")
base_image = ImageTk.PhotoImage(file=name)

images = []
for key in available_keys:
	name = os.path.join("Images",key+".png")
	im = ImageTk.PhotoImage(file=name)
	images.append(im)

images_sensors = []
for i in range (0,12):
	name = os.path.join("Images",str(i)+".png")
	try:
		im = ImageTk.PhotoImage(file=name)
		images_sensors.append(im)
		print "Loaded Image: "+str(i)
	except: 
		print "Could not load Image: "+str(i)

current = "w"

def updateImage():
	global root, panel, im, current, available_keys, timer, log_path
	timer.cancel()
	timer = threading.Timer(30, resetImage)
	index = available_keys.index(current)
	panel.configure(image=images[index], background = "black")
	panel ["image"] = images[index]
	panel.pack(side="bottom",fill ="both",expand="yes")
	print "loaded image", current
	try:
		log_file = open(log_path,'a')
		log_file.write(str(time.time())+";"+time.ctime()+";"+str(current)+"\n")
		log_file.close()
	except:
		print "Error during logging"
	timer.start()

def resetImage():
	global base_image, panel
	panel.configure(image=base_image, background = "black")
	panel ["image"] = base_image
	panel.pack(side="bottom",fill ="both",expand="yes")
	print "Reset Image to base image by timer"
	try:
		log_file = open(log_path,'a')
		log_file.write(str(time.time())+";"+time.ctime()+";"+"reload base_image\n")
		log_file.close()
	except:
		print "Error during logging"

def key(event):
	global root, panel, im, current, available_keys
	current = repr(event.char)[1]
	if not current in available_keys:
		return
	print "pressed", current
	updateImage()

def leftKey(event):
	global root, panel, im, current, available_keys
	print "pressed left"
	moveLeft()
	updateImage()

def rightKey(event):
	global root, panel, im, current, available_keys
	print "pressed right"
	moveRight()
	updateImage()

def pressedSpace(event):
	global root, panel, im, current, available_key
	print "pressed space"
	moveRight()
	updateImage()

def pressedEnter(event):
	global root, panel, im, current, available_key
	print "pressed enter"
	moveRight()
	updateImage()

def moveRight():
	global root, panel, im, current, available_key
	newPos = (getPositionOf(current) + 1) % len(available_keys)
	current = available_keys[newPos]

def moveLeft():
	global root, panel, im, current, available_key
	newPos = (getPositionOf(current) - 1) % len(available_keys)
	if (newPos < 0):
		len(available_keys)
	current = available_keys[newPos]

def getPositionOf(key):
	global root, panel, im, current, available_keys
	for i in range(len(available_keys)):
		if available_keys[i] == key:
			return i
	return -1

def escape(event):
	global root, timer, sensorListener, stop
	root.destroy()
	timer.cancel()
	stop = True
	sys.exit()

def listenToSensors(arg):
	global current

        print 'Loading Adafruit MPR121 Capacitive Touch Sensor'
        # Create MPR121 instance.
        cap = MPR121.MPR121()
        
        if not cap.begin():
                print 'Error initializing MPR121.  Check your wiring!'
                sys.exit(1)

        #
        cap.set_thresholds(255,255)
        listen(cap)


def listen(cap):
        global current, stop
        last_touched = cap.touched()
        listens = 0
        while True:
            current_touched = cap.touched()
            # Check each pin's last and current state to see if it was pressed or released.
            for i in range(12):
                # Each pin is represented by a bit in the touched value.  A value of 1
                # means the pin is being touched, and 0 means it is not being touched.
                pin_bit = 1 << i
                # First check if transitioned from not touched to touched.
                if current_touched & pin_bit and not last_touched & pin_bit:
                    print '{0} touched!'.format(i)
                    current = int(i)
                    updateImageFromSensor()
                # Next check if transitioned from touched to not touched.
                if not current_touched & pin_bit and last_touched & pin_bit:
                    print '{0} released!'.format(i)
            # Update last state and wait a short period before repeating.
            last_touched = current_touched
            time.sleep(0.1)
            listens += 1
            if listens % 150 == 0:
                    cap.begin()
                    cap.set_thresholds(255,255)
                    print "Reset sensors"
            if stop:
                return

def updateImageFromSensor():
	global root, panel, im, current, timer, images_sensors
	timer.cancel()
	timer = threading.Timer(30, resetImage)
	position = int(current)
	print "Position: "+str(position)+" Length: "+str(len(images_sensors))
	panel.configure(image=images_sensors[position], background = "black")
	panel ["image"] = images_sensors[position]
	panel.pack(side="bottom",fill ="both",expand="yes")
	print "loaded image", current
	try:
		log_file = open(log_path,'a')
		log_file.write(str(time.time())+";"+time.ctime()+";"+str(position)+"\n")
		log_file.close()
	except:
		print "Error during logging"
	timer.start()

root.bind("<Key>", key)
root.bind("<Left>", leftKey)
root.bind("<Right>", rightKey)
root.bind("<Escape>", escape)
root.bind("<Return>", pressedEnter)
root.bind("<space>", pressedSpace)

name = os.path.join("Images",current+".png")
im = ImageTk.PhotoImage(file=name)
panel =  tk.Label(root,image = im)
panel ["image"] = im
panel.pack(side="bottom",fill ="both",expand="yes")

timer = threading.Timer(30, resetImage)
sensorListener = threading.Thread(target = listenToSensors, args = (12, ))
sensorListener.start()
root.mainloop()
