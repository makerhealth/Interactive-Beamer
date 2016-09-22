# Interactive-Beamer

### Introduction
The idea of the project is to combine a RaspberryPi, a capacitative touch sensor and a projector to create a smart projector wall. The repository contains the python code which runs on the RaspberryPi and also contains instructions for setting up the hardware.

### What is the meaning of the repositories name?
In German a projector is also called beamer. This a typical anglicism the Germans love to use. If you are interested in more strange German, you can watch this video https://www.youtube.com/watch?v=DCYnK-mlK2A.

### Materials
For this project the following materials are needed:
 - 1 RaspberryPi 2 or 3
 - 1 Adafruit 12-Key Capacitive Touch Sensor Breakout - MPR121
 - 1 Breadboard
 - 16 Jumperwires
 - Wires
 - 12 Aluminum Plates
 - White Acrylic Board  
 - Velcro Tape
 - Duck Tape

### First Setup
  Follow the steps to create your own interactive projector wall. 
  1. Install Raspbian or Noobs on your RaspberryPi. See https://www.raspberrypi.org/downloads/
  2. Install the Python library for the Capacitative Touch Sensor as discribed by Adafruit: https://learn.adafruit.com/mpr121-capacitive-touch-sensor-on-raspberry-pi-and-beaglebone-black/software
  3. Connect the MPR121 sensor with the RaspberryPi as discribed by Adafruit: https://learn.adafruit.com/mpr121-capacitive-touch-sensor-on-raspberry-pi-and-beaglebone-black/hardware
  4. Place the aluminum plates on the acrylic board as you which and locate them with each two stripes of Velcro. 
  5. Drill one hole for each aluminum plate into the acrylic board. The hole should be in the center of the aluminums plate location.
  6. Solder one wire and one jumper wire together
  7. Roughen the back side of each aluminum plate
  8. Tape each one wire with the Duck Tape to one aluminum plate and pull the wire trough the hole to the back of the acrylic board.
  9. Connect the ends of all the wires from the projector wall into the breadboard and connect them in that way to the MRP121 sensor
  10. Now clone this git repository to your RaspberryPi with the command 
      ``` git clone git@github.com:makerhealth/Interactive-Beamer.git ```
  11. Place the 13 pictures you want to display in the folder Images, one Images should be named base_image.png the other Images should be named from 0.png to 11.png
  12. Run the script in the git repository by the command ```python interactive_beamer.py```

### Setup
  To use the interactive wall follow the given steps:
  1. Plugin the keyboard, mouse, and the projector (via HDMI-cable) into the Raspberry Pi
  2. Make sure the touch sensor and cobbler are connected
      3V3 -> VIN
      GND -> GND
      SDA -> SDA
      SCL -> SCL
  3. Power up the Raspberry Pi and the Projector
     If you experience problems try another power supply.
  4. Open the terminal and type the following lines


### Licence
This project is published under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).
