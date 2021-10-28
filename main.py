from KY040 import KY040
from tv_service import TVService

def main():
    CLOCKPIN = 13
    DATAPIN = 6
    SWITCHPIN = 5
    BACKLIGHTPIN = 18
    VIDEO_DIR = '/home/pi/videos'

    tvservice = TVService(CLOCKPIN, DATAPIN, SWITCHPIN, BACKLIGHTPIN, VIDEO_DIR)
    tvservice.run()

if __name__ == "__main__":
    main()
