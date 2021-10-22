import RPi.GPIO as GPIO
from KY040 import KY040
from time import sleep

import board
import pwmio

#KY040 setup
GPIO.setmode(GPIO.BCM)
CLOCKPIN = 13
DATAPIN = 6
SWITCHPIN = 5

#PiTFT Setup
SCREEN = pwmio.PWMOut(board.D18, frequency=5000, duty_cycle=0)
SCREEN_ON = False

def turn_screen_on():
    for i in range(101):
        SCREEN.duty_cycle = int(i * 65535 / 100)
        sleep(0.01)

def turn_screen_off():
    for i in range(100, -1, -1):
        SCREEN.duty_cycle = int(i * 65535 / 100)
        sleep(0.01)

# Callback for rotary change
def rotary_change(direction):
    print ("turned - " + str(direction))

# Callback for switch button pressed
def switch_pressed():
    global SCREEN_ON
    if SCREEN_ON:
        turn_screen_off()
    else:
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
