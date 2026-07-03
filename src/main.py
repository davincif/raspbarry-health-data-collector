#!python3
"""
Author: Leonardo Da Vinci
Date: July of 2026
Description: A wacther for the raspberry pi linux environment
"""

from time import perf_counter, sleep, time
import psutil

import globals
from watchers.cpu import CPU
from watchers.disks import Disks
from watchers.memory import Memory
from watchers.net import Net
from watchers.temperature import Temperature
from watchers.up_time import UpTime

cost = 0


def main():
    validate_os()

    globals.set_globals()
    watch()


def validate_os():
    if not (psutil.LINUX or psutil.POSIX):
        raise OSError("System not suported")


def watch():
    initial_time = time()
    print("initial_time", initial_time)

    temp_sensor = Temperature()
    up_time = UpTime()
    cpu = CPU()
    memory = Memory()
    disk = Disks()
    net = Net()

    show_print = True

    while True:
        start = perf_counter()

        # updates
        temp_sensor.update()

        up_time.update()

        cpu.update()

        memory.update()

        disk.update()

        net.update()

        if show_print:
            print(temp_sensor)
            print(up_time)
            print(cpu)
            print(memory)
            print(disk)
            print(net)
        # #######

        cost = perf_counter() - start
        ramining = globals.update_rate - cost

        print("measurement cost", cost, "\n")
        if ramining > 0:
            sleep(ramining)


if __name__ == "__main__":
    main()
