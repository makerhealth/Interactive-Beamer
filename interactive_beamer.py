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

import Tkinter as Tk
from PIL import ImageTk
import os
import sys
import time
import threading
import urllib
try:
    import Adafruit_MPR121.MPR121 as MPR121
except:
    print "Could not import Adafruit Module"
    sys.exit(1)

# Setting up UI
root = Tk.Tk()
root.attributes("-fullscreen", True)

# Initializing general variables
stop = False
logging = True
log_path = "./beamer.log"
reset_time = 30
download_source = "None"
base_image
panel

# Reading configuration file
config_path = "./config.txt"
try:
    config_file = open(config_path)
except:
    print "Could not read configuration file"

for line in config_file.readlines():
    # Remove leading and trailing whit space chars.
    # This is necessary, because the user might add
    # them without any reason.
    line = line.strip()

    if line.startswith("log_path="):
        log_path = line.split("log_path=")[1]
        logging = True
    if line.startswith("logging=False"):
        logging = False
    if line.startswith("reset_time="):
        reset_time = line.split("reset_time=")[1]
    if line.startswith("download_source="):
        download_source = line.split("download_source=")[1]


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
                    log(str(pin) + " touched")
                    current = int(pin)
                    update_image()
                # Next check if transitioned from touched to not touched.
                if not current_pin & pin_bit and last_pin & pin_bit:
                    log(str(pin) + " released")

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
    global root, panel, im, current, timer, images_sensors, reset_time
    # Resetting timer, will be started after image has been updated
    timer.cancel()
    timer = threading.Timer(reset_time, reset_image)

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


# Downloading images, if source server is given
if download_source != "None":

    for i in range(0, 12):
        name = os.path.join("Images", str(i) + ".png")
        try:
            urllib.urlretrieve(download_source+"/"+name, name)
            log("Downloaded Image: " + str(i))
        except:
            log("Could not downloaded Image: " + str(i))

# Loading images in advance to increase the performance
name = os.path.join("Images", "base_image.png")
base_image = ImageTk.PhotoImage(file=name)
panel = Tk.Label(root, image=base_image)

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
timer = threading.Timer(reset_time, reset_image)

# Listening to sensor input
sensorListener = threading.Thread(target=listen_to_sensors)
sensorListener.start()

# Displaying root
root.mainloop()
