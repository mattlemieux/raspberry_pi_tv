from KY040 import KY040
from tv_service import TVService
from player_service import PlayerService
from threading import Thread
import asyncio

async def main():
    CLOCKPIN = 13
    DATAPIN = 6
    SWITCHPIN = 5
    BACKLIGHTPIN = 18
    VIDEO_DIR = '/home/pi/videos'

    playerservice = asyncio.create_task(PlayerService(VIDEO_DIR).run())
    tvservice = asyncio.create_task(TVService(CLOCKPIN, DATAPIN, SWITCHPIN, BACKLIGHTPIN).run())

    await playerservice
    awaittvservice

if __name__ == "__main__":
    asyncio.run(main())
