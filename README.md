# Pico power monitor

## Goal

The goal is to be able to measure the power consumption of my house and send that information to [home assistant](https://www.home-assistant.io/) over MQTT where it will be logged.

## Setup
* [load micropython onto the pico](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html)
* Add ads115.py as a file to your pico
* Add consts.py as a file to your pico.  This file will have you wifi passwords and mqtt settings in it.

# support lib
* [ADS1115] (https://github.com/robert-hh/ads1x15/blob/master/ads1x15.py) included the original source to be thorough 
