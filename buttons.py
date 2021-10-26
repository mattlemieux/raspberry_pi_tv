import RPi.GPIO as GPIO
from KY040 import KY040
from time import sleep

import board
import pwmio
import os


#KY040 setup
GPIO.setmode(GPIO.BCM)
CLOCKPIN = 13
DATAPIN = 6
SWITCHPIN = 5

#PiTFT Setup
# SCREEN = pwmio.PWMOut(board.D18, frequency=5000, duty_cycle=0)
SCREEN_ON = False
os.system('raspi-gpio set 19 ip')
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)


def turn_screen_on():
    # brighten screen
    # for i in range(101):
    #     SCREEN.duty_cycle = int(i * 65535 / 100)
    #     sleep(0.01)
    os.system('raspi-gpio set 19 op a5')
    GPIO.output(18, GPIO.HIGH)

def turn_screen_off():
    # dim screen
    # for i in range(100, -1, -1):
    #     SCREEN.duty_cycle = int(i * 65535 / 100)
    #     sleep(0.01)
    os.system('raspi-gpio set 19 ip')
    GPIO.output(18, GPIO.LOW)

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
