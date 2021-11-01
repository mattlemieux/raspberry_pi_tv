from KY040 import KY040
from tv_service import TVService
from player_service import PlayerService
from multiprocessing import Process

def run_cpu_tasks_in_parallel(tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()

def main():
    CLOCKPIN = 13
    DATAPIN = 6
    SWITCHPIN = 5
    BACKLIGHTPIN = 18
    VIDEO_DIR = '/home/pi/videos'

    playerservice = PlayerService(VIDEO_DIR)
    tvservice = TVService(CLOCKPIN, DATAPIN, SWITCHPIN, BACKLIGHTPIN)

    run_cpu_tasks_in_parallel([
        lambda: playerservice.run(),
        lambda: tvservice.run(),
    ])

if __name__ == "__main__":
    main()
