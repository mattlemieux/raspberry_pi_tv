from subprocess import Popen
import logging
import os
import random

logging.basicConfig(filename='playerservice.log', level=logging.INFO)

class PlayerService:

    def get_videos(self):
        videos = []
        for folder in os.listdir(self.video_dir):
            for file in os.listdir(os.path.join(self.video_dir, folder)):
                if file.lower().endswith('.mp4'):
                    newvideo = os.path.join(self.video_dir, folder, file)
                    videos.append(newvideo)
        random.shuffle(videos)
        return videos


    def start_player(self, videos):
        try:
            for video in videos:
                self.currentFile = video
                self.process = Popen(
                  ['omxplayer', '--no-osd', '--aspect-mode', 'fill', self.currentFile],
                  close_fds=True,
                  bufsize=0,
                )
                self.process.wait()
        except Exception as e:
            logging.error("Error occured playing file [%s]: %s", self.currentFile, e)

    def stop_player(self):
        p = self.process
        if p is not None:
            try:
                p.terminate()
                p.wait()
            except EnvironmentError as e:
                logging.error("can't stop %s: %s", self.currentFile, e)
            else:
                self.process = None

    def run(self):
        logging.info("starting player_service")
        logging.info("video directory: %s", self.video_dir)
        try:
            while True:
                self.start_player(self.videos)
        finally:
            logging.info("stopping player_service process")
            self.stop_player()


    def __init__(self, video_dir):
        self.currentFile = ""
        self.video_dir = video_dir
        self.videos = self.get_videos()
