from KY040 import KY040
from tv_service import TVService
from player_service import PlayerService
from threading import Thread

def main():
    CLOCKPIN = 13
    DATAPIN = 6
    SWITCHPIN = 5
    BACKLIGHTPIN = 18
    VIDEO_DIR = '/home/pi/videos'

    playerservice = PlayerService(VIDEO_DIR)
    tvservice = TVService(CLOCKPIN, DATAPIN, SWITCHPIN, BACKLIGHTPIN)

    threads = [
        Thread(target = playerservice.run()),
        Thread(target = tvservice.run())
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
