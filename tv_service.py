
from KY040 import KY040
from time import sleep
import logging
import os
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

# rm CMakeCache.txt
# cmake -DARMV6Z=ON -DADAFRUIT_HX8357D_PITFT=ON -DSPI_BUS_CLOCK_DIVISOR=8 -DSTATISTICS=0 -DBACKLIGHT_CONTROL=ON ..
# make -j
# sudo ./fbcp-ili9341

class TVService:
    def turn_screen_on(self):
        logger.debug("turning screen on")
        os.system('raspi-gpio set 19 op a5') # audio on
        GPIO.output(18, GPIO.HIGH) # video on


    def turn_screen_off(self):
        logger.debug("turning screen off")
        os.system('raspi-gpio set 19 ip') # audio off
        GPIO.output(18, GPIO.LOW) # video off


    def rotary_change(self, direction):
        logger.debug("rotary_change - " + str(direction))


    def switch_pressed(self):
        if self.screen_on:
            self.turn_screen_off()
        else:
            self.turn_screen_on()
        self.screen_on = not self.screen_on


    def run(self):
        logger.debug("staring tv_service")
        self.ky040.start()
        self.turn_screen_on()

        try:
            logger.debug("listening for events....")
            while True:
                sleep(0.1)
        finally:
            logger.debug("shutting down tv_service")
            GPIO.cleanup()
            self.ky040.stop()


    def __init__(self, clock_pin, data_pin, switch_pin, backlight_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(backlight_pin, GPIO.OUT)
        os.system('raspi-gpio set 19 ip')

        ky040 = KY040(clock_pin, data_pin, switch_pin, self.rotary_change, self.switch_pressed)

        self.ky040 = ky040
        self.screen_on = True
