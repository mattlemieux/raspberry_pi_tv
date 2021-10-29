
from KY040 import KY040
from omxplayer.player import OMXPlayer
from pathlib import Path
from threading import Thread, Lock, currentThread
from time import sleep

import os
import random
import RPi.GPIO as GPIO

# sudo apt-get update && sudo apt-get install -y libdbus-1{,-dev}
# pip install omxplayer-wrapper

class TVService:
    def turn_screen_on(self):
        print("turning screen on")
        os.system('raspi-gpio set 19 op a5') # audio on
        GPIO.output(18, GPIO.HIGH) # video on


    def turn_screen_off(self):
        print("turning screen off")
        os.system('raspi-gpio set 19 ip') # audio off
        GPIO.output(18, GPIO.LOW) # video off


    def rotary_change(self, direction):
        print ("rotary_change - " + str(direction))
        # # 1 - open next folder
        # # 0 - play previous folder
        # self.lock.acquire()
        # try:
        #     new_index = self.current_video_index
        #     if (direction == KY040.ANTICLOCKWISE):
        #         if (new_index + 1 >= len(self.video_dict)):
        #             new_index = 0
        #         else:
        #             new_index+=1
        #     else:
        #         if (new_index - 1 < 0):
        #             new_index = len(self.video_dict) - 1
        #         else:
        #             new_index-=1
        #     if new_index != self.current_video_index:
        #         self.current_video_index = new_index 
        #         self.play_videos(self.video_dict[list(self.video_dict)[self.current_video_index]])
        # finally:
        #     self.lock.release()


    def switch_pressed(self):
        if self.screen_on:
            self.turn_screen_off()
        else:
            self.turn_screen_on()
        self.screen_on = not self.screen_on


    def get_videos(self):
        videos = {}
        for folder in os.listdir(self.video_dir):
            for file in os.listdir(os.path.join(self.video_dir, folder)):
                if file.lower().endswith('.mp4'):
                    newvideo = os.path.join(self.video_dir, folder, file)
                    if videos.get(folder):
                        videos.get(folder).append(newvideo)
                    else:
                        videos[folder] = [newvideo]
            if (videos.get(folder)):
                random.shuffle(videos.get(folder))
        return videos


    def play_video_thread(self, videos):
        player = {}
        try:
            for video in videos:
                print("starting video player")
                player = OMXPlayer(video, args='--no-osd --vol -500 --aspect-mode fill')
        except Exception as err:
            print(err)
        finally:
            print("shutting down video thread")
            if player is not None:
                player.quit()

    def stop_play_video_thread(self):
        if (self.omx_thread and self.omx_thread.isAlive()):
            print("stopping video thread")
            self.omx_thread.do_run = False
            self.omx_thread.join()

    def start_play_video_thread(self, videos):
        print("starting video thread")
        self.omx_thread = Thread(target=self.play_video_thread, args=(videos,))
        self.omx_thread.start()

    def play_videos(self, videos):
        self.stop_play_video_thread()
        self.start_play_video_thread(videos)

    def run(self):
        print("staring video service")
        self.turn_screen_on()
        self.ky040.start()
        
        self.play_videos(self.video_dict[list(self.video_dict)[self.current_video_index]])

        try:
            print("listening for events....")
            while True:
                sleep(0.1)
        finally:
            print("shutting down")
            self.stop_play_video_thread()
            self.ky040.stop()
            GPIO.cleanup()


    def __init__(self, clock_pin, data_pin, switch_pin, backlight_pin, video_dir):
        GPIO.setmode(GPIO.BCM)
        os.system('raspi-gpio set 19 ip')
        GPIO.setup(backlight_pin, GPIO.OUT)

        ky040 = KY040(clock_pin, data_pin, switch_pin, self.rotary_change, self.switch_pressed)

        self.ky040 = ky040
        self.video_dir = video_dir

        self.screen_on = True
        self.video_dict = self.get_videos()
        self.current_video_index = 0

        self.omx_thread = None
        self.lock = Lock()

# rm CMakeCache.txt
# cmake -DARMV6Z=ON -DADAFRUIT_HX8357D_PITFT=ON -DSPI_BUS_CLOCK_DIVISOR=8 -DSTATISTICS=0 -DBACKLIGHT_CONTROL=ON ..
# make -j
# sudo ./fbcp-ili9341
