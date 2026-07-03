#!python3
"""
Author: Leonardo Da Vinci
Date: July of 2026
Description: A wacther for the raspberry pi linux environment
"""

import json
import signal
from time import perf_counter, sleep, time
from types import FrameType
import psutil

import globals
from watchers.cpu import CPU
from watchers.disks import Disks
from watchers.memory import Memory
from watchers.net import Net
from watchers.temperature import Temperature
from watchers.up_time import UpTime

kill_now = False
cost = 0

temp_sensor: Temperature
up_time: UpTime
cpu: CPU
memory: Memory
disk: Disks
net: Net


def main():
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)

    validate_os()

    globals.set_globals()
    watch()


def validate_os():
    if not (psutil.LINUX or psutil.POSIX):
        raise OSError("System not suported")


def watch():
    global kill_now

    print(
        f"raspbarry-health-data-collector version: {globals.version}\nby - davincif\ncheck me @ ldavincif.com\n"
    )

    initial_time = time()
    init()
    initial_data_to_transfer = serialize_unmutables()

    if globals.verbose:
        print("started at", initial_time)

    while not kill_now:
        start = perf_counter()

        update()
        data_to_transfer = serialize_update()

        cost = perf_counter() - start
        ramining = globals.update_rate - cost

        if ramining > 0:
            if globals.verbose:
                print("measurement cost", cost, "\n")

            if not kill_now:
                sleep(ramining)


def init():
    global temp_sensor, up_time, cpu, memory, disk, net

    temp_sensor = Temperature()
    up_time = UpTime()
    cpu = CPU()
    memory = Memory()
    disk = Disks()
    net = Net()


def update():
    global temp_sensor, up_time, cpu, memory, disk, net

    temp_sensor.update()
    up_time.update()
    cpu.update()
    memory.update()
    disk.update()
    net.update()

    if globals.verbose:
        print(temp_sensor)
        print(up_time)
        print(cpu)
        print(memory)
        print(disk)
        print(net)


def serialize_unmutables():
    global temp_sensor, up_time, cpu, memory, disk, net

    data = {
        "temp": temp_sensor.marshal_unmutables(),
        "uptime": up_time.marshal_unmutables(),
        "process": cpu.marshal_unmutables(),
        "memory": memory.marshal_unmutables(),
        "disk": disk.marshal_unmutables(),
        "net": net.marshal_unmutables(),
    }

    return json.dumps(data)


def serialize_update():
    global temp_sensor, up_time, cpu, memory, disk, net

    data = {
        "temp": temp_sensor.marshal_update(),
        "uptime": up_time.marshal_update(),
        "process": cpu.marshal_update(),
        "memory": memory.marshal_update(),
        "disk": disk.marshal_update(),
        "net": net.marshal_update(),
    }

    return json.dumps(data)


def exit_gracefully(signum: int, frame: FrameType | None):
    global kill_now

    print(f"singal {signal.Signals(signum).name} received, closing...")
    kill_now = True


if __name__ == "__main__":
    main()
