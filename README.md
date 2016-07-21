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

### Setup
  Follow the steps to create your own interactive projector wall. You can finde a more detailed description including images on our homepage http://www.makerhealth.co.
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
  11. Run the script in the git repository by the command ```python interactive_beamer.py```
  
### Licence
This project is published under the MIT License.
