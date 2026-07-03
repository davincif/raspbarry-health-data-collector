#!python3

from time import perf_counter, sleep, time

import globals
from watchers.cpu import CPU
from watchers.disks import Disks
from watchers.memory import Memory
from watchers.temperature import Temperature
from watchers.up_time import UpTime

cost = 0


def main():
    globals.set_globals()
    watch()


def watch():
    initial_time = time()
    print("initial_time", initial_time)

    temp_sensor = Temperature()
    up_time = UpTime()
    cpu = CPU()
    memory = Memory()
    disk = Disks()

    while True:
        start = perf_counter()

        # updates
        temp_sensor.update()
        print(temp_sensor)

        up_time.update()
        print(up_time)

        cpu.update()
        # print(cpu)

        memory.update()
        print(memory)

        disk.update()
        print(disk)
        # #######

        cost = perf_counter() - start
        ramining = globals.update_rate - cost

        print("measurement cost", cost)
        if ramining > 0:
            sleep(ramining)


if __name__ == "__main__":
    main()
