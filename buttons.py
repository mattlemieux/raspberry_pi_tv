import RPi.GPIO as GPIO
import time
import os
import KY040

os.system('raspi-gpio set 19 ip')
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)

# Define your pins
CLOCKPIN = 13
DATAPIN = 6
SWITCHPIN = 5

def turn_screen_on():
    os.system('raspi-gpio set 19 op a5')
    GPIO.output(18, GPIO.HIGH)

def turn_screen_off():
    os.system('raspi-gpio set 19 ip')
    GPIO.output(18, GPIO.LOW)

# Callback for rotary change
def rotaryChange(direction):
    print ("turned - " + str(direction))

# Callback for switch button pressed
def switchPressed():
    if screen_on:
        turn_screen_off()
    else:
        turn_screen_on()
    screen_on = not screen_on
        
# Create a KY040 and start it
ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN, rotaryChange, switchPressed)
ky040.start()

turn_screen_off()
screen_on = False
# Keep your proccess running
try:
    while True:
        sleep(0.1)
finally:
    ky040.stop()
    GPIO.cleanup()
