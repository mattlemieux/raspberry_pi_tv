import RPi.GPIO as GPIO
from KY040 import KY040
from time import sleep

import board
import pwmio
import os
from subprocess import PIPE, Popen, STDOUT

#KY040 setup
GPIO.setmode(GPIO.BCM)
CLOCKPIN = 13
DATAPIN = 6
SWITCHPIN = 5

#PiTFT Setup
# SCREEN = pwmio.PWMOut(board.D18, frequency=5000, duty_cycle=0)
SCREEN_ON = False
os.system('raspi-gpio set 19 ip')

def turn_screen_on():
    os.system('raspi-gpio set 19 op a5')
    os.system("sudo sh -c 'echo \"1\" > /sys/class/backlight/soc:backlight/brightness'")

def turn_screen_off():
    os.system('raspi-gpio set 19 ip')
    os.system("sudo sh -c 'echo \"0\" > /sys/class/backlight/soc:backlight/brightness'")

# Callback for rotary change
def rotary_change(direction):
    # 1 - open next folder
    # 0 - play previous folder
    print ("turned - " + str(direction))

# Callback for switch button pressed
def switch_pressed():
    global SCREEN_ON
    if SCREEN_ON:
        print("turning screen off")
        turn_screen_off()
    else:
        print("turning screen on")
        turn_screen_on()
    SCREEN_ON = not SCREEN_ON
 
turn_screen_off()

# Create a KY040 and start it
ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotary_change, switch_pressed)
ky040.start()

try:
    while True:
        sleep(0.1)
finally:
    ky040.stop()
    GPIO.cleanup()
