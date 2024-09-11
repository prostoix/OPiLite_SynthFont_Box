#!/usr/bin/env python
# -*- coding: utf-8 -*-

### FLUIDSYNTH
import array
import json
from telnetlib import Telnet

# Список инструментов
with open('inst.JSON') as f:
    instrument = json.load(f)

count_inst = len(instrument["inst"])
#print(piano["inst"][0]["name"])
#print(len(piano["inst"]))

#fs = Telnet("localhost",9800, 10)
#fs.write('noteon 1 25 127\n'.encode('ascii'))
#time.sleep(1.0)
#telnet.close()

### OLED
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
#OLED config 
serial = i2c(port=0, address=0x3C)
device = ssd1306(serial)

### GPIO
import OPi.GPIO as GPIO
from time import sleep          
# GPIO config 
GPIO.setboard(GPIO.PCPCPLUS)        
GPIO.setmode(GPIO.BOARD)        
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_OFF)    
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

count = 0

def oled_count(count):
    with canvas(device) as draw:
        device.size = 15
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((30, 40), count, fill="white")
    return oled_count

def walker(step):
    if step == "up": count += 1
    else: count -= 1
    if count > count_inst: count = 0
    if count < 0: count = count_inst
    return walker


try:
    while True:                 # this will carry on until you hit CTRL+C
        if GPIO.input(29) == False:      # if pin 15 == 1
            print("29")
            count -= 1
            walker("down")
            oled_count(instrument["inst"][count]["name"])
            sleep(0.5)
        if GPIO.input(31) == False:      # if pin 15 == 1
            print("31")
            walker("up")
            oled_count(instrument["inst"][count]["name"])
            sleep(0.5)
        if GPIO.input(33) == False:      # if pin 15 == 1
            print ("33")
            oled_count("reverb")
            
            sleep(0.5)
        sleep(0.10)              # wait 0.1 seconds

finally:                        # this block will run no matter how the try block exits
    print("Finally")
   # GPIO.output(11, 0)
    GPIO.cleanup()              # clean up after yourself