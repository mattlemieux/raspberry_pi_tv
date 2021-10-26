import RPi.GPIO as GPIO
from KY040 import KY040
from time import sleep

import os
import random
from subprocess import PIPE, Popen, STDOUT
from collections import defaultdict


#KY040 setup
GPIO.setmode(GPIO.BCM)
CLOCKPIN = 13
DATAPIN = 6
SWITCHPIN = 5

#PiTFT Setup
SCREEN_ON = False
VIDEOS = {}
CURR_INDEX = 0
os.system('raspi-gpio set 19 ip')

#Video Stuff
ROOT_DIR = '/home/pi/videos'

def turn_screen_on():
    os.system('raspi-gpio set 19 op a5')
    os.system("sudo sh -c 'echo \"1\" > /sys/class/backlight/soc:backlight/brightness'")

def turn_screen_off():
    os.system('raspi-gpio set 19 ip')
    os.system("sudo sh -c 'echo \"0\" > /sys/class/backlight/soc:backlight/brightness'")

# Callback for rotary change
def rotary_change(direction):
    print ("turned - " + str(direction))
    # 1 - open next folder
    # 0 - play previous folder
    global VIDEOS
    global CURR_INDEX

    if (direction == KY040.ANTICLOCKWISE):
        if (CURR_INDEX + 1 > len(VIDEOS)):
            CURR_INDEX = 0
        else:
            CURR_INDEX+=1
    else:
        if (CURR_INDEX - 1 > 0):
            CURR_INDEX = len(VIDEOS) - 1
        else:
            CURR_INDEX-=1

    play_video(list(VIDEOS)[CURR_INDEX])



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

def get_videos():
    videos = {}

    for folder in os.listdir(ROOT_DIR):
        print (folder)
        print (os.path.join(ROOT_DIR, folder))
        for file in os.listdir(os.path.join(ROOT_DIR, folder)):
            print (file)
            print (os.path.join(ROOT_DIR, folder, file))
            if file.lower().endswith('.mp4'):
                newvideo = os.path.join(ROOT_DIR, folder, file)
                if folder in videos:
                    videos[folder].append(newvideo)
                else:
                    videos[folder] = [newvideo]
    return videos

def play_video(videos):
    random.shuffle(videos)
    for video in videos:
        Popen(['omxplayer', '--no-osd', '--aspect-mode', 'fill', video])

VIDEOS = get_videos()
play_video(VIDEOS[list(VIDEOS)[CURR_INDEX]])

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
