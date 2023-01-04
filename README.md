# Pico power monitor

## Goal

The goal is to be able to measure the power consumption of my house and send that information to [home assistant](https://www.home-assistant.io/) over MQTT where it will be logged.

## Setup
* [load micropython onto the pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)

You'll then load the software onto the pico.  With the thorny IDE you can go to \[File\]->\[Save as\] and then select pico as your location.
* Add ads115.py as a file to your pico
* Add consts.py as a file to your pico.  This file will have you wifi passwords and mqtt settings in it.
* Add main.py to your pico.  This one will auto boot when you plug it in

# support lib
* [ADS1115](https://github.com/robert-hh/ads1x15/blob/master/ads1x15.py) included the original source to be thorough 

### Some helpfull links for learning how this works
* [mqtt on micropython](https://www.tomshardware.com/how-to/send-and-receive-data-raspberry-pi-pico-w-mqtt)
