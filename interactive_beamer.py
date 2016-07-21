# Copyright (c) 2016 MakerHealth
# Author: Max-Philipp Schrader
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import Tkinter as tk
from PIL import ImageTk
import os
import sys
import time
import threading
try:
    import Adafruit_MPR121.MPR121 as MPR121
except:
    print "Could not import Adafruit Module"
    sys.exit(1)

# Setting up UI
root = tk.Tk()
root.attributes("-fullscreen", True)

# Initializing general variables
stop = False
logging = True
log_path = "./log/touch.log"
base_image
panel


def reset_image():
    """
    Resets displayed image to base image.
    :return:
    """
    global base_image, panel
    panel.configure(image=base_image, background="black")
    panel["image"] = base_image
    panel.pack(side="bottom", fill="both", expand="yes")
    log("Reset to base image by timer")


def escape(event):
    """
    Closes program as soon as the user presses escape.
    :param event:
    :return:
    """
    global root, timer, sensorListener, stop
    root.destroy()
    timer.cancel()
    stop = True
    sys.exit()


def listen_to_sensors():
    """
    Loads the Adafruit library and starts listening for sensor input
    :return:
    """

    log('Loading Adafruit MPR121 Capacitive Touch Sensor')
    # Create MPR121 instance.
    cap = MPR121.MPR121()
        
    if not cap.begin():
        log('Error initializing MPR121.  Check your wiring!')
        sys.exit(1)
    log("Initialized sensor")
    cap.set_thresholds(255, 255)
    log("Start listening")
    listen(cap)


def listen(cap):
        """
        Listening to the input of the sensor.
        :param cap:
        :return:
        """
        global current, stop
        last_pin = cap.touched()
        listens = 0
        while True:
            current_pin = cap.touched()
            # Check each pin's last and current state to see if it was pressed or released.
            for pin in range(12):
                # Each pin is represented by a bit in the touched value.  A value of 1
                # means the pin is being touched, and 0 means it is not being touched.
                pin_bit = 1 << pin
                # First check if transitioned from not touched to touched.
                if current_pin & pin_bit and not last_pin & pin_bit:
                    log('{0} touched'.format(pin))
                    current = int(pin)
                    update_image()
                # Next check if transitioned from touched to not touched.
                if not current_pin & pin_bit and last_pin & pin_bit:
                    log('{0} released'.format(pin))

            # Update last state and wait a short period before repeating.
            last_pin = current_pin
            time.sleep(0.1)
            listens += 1

            # Resetting sensor after a certain time to allow the baseline of the
            # touch sensor to be adjusted to environmental changes.
            if listens % 150 == 0:
                    cap.begin()
                    cap.set_thresholds(255, 255)
                    log("Reset Sensor")
            if stop:
                return


def update_image():
    """
    Updates image depending on the pin that was touched
    :return:
    """
    global root, panel, im, current, timer, images_sensors
    # Resetting timer, will be started after image has been updated
    timer.cancel()
    timer = threading.Timer(30, reset_image)

    position = int(current)

    # Updating image
    panel.configure(image=images_sensors[position], background="black")
    panel["image"] = images_sensors[position]
    panel.pack(side="bottom", fill="both", expand="yes")

    # Logging, if path exists otherwise there will be an error
    log('Loaded image '+str(position))

    # Starting timer
    timer.start()


def log(message):
    """
    Logging message to globally set log path.
    :param message:
    :return:
    """
    global log_path
    log_message = str(time.time()) + " - " + time.ctime() + " - " + str(message)
    print str(log_message)
    try:
        log_file = open(log_path, 'a')
        log_file.write(log_message + "\n")
        log_file.close()
    except:
        print "Error during logging"

# Loading images in advance to increase the performance
name = os.path.join("Images", "base_image.png")
base_image = ImageTk.PhotoImage(file=name)
panel = tk.Label(root, image=base_image)

images_sensors = []
for i in range(0, 12):
    name = os.path.join("Images", str(i) + ".png")
    try:
        im = ImageTk.PhotoImage(file=name)
        images_sensors.append(im)
        log("Loaded Image: " + str(i))
    except:
        log("Could not load Image: " + str(i))

# Finalizing root frame
root.bind("<Escape>", escape)
reset_image()

# Starting all threads
# Resetting the image after given time
timer = threading.Timer(30, reset_image)

# Listening to sensor input
sensorListener = threading.Thread(target=listen_to_sensors)
sensorListener.start()

# Displaying root
root.mainloop()
