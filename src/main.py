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
import asyncio

from connection import find_data_orchestrator_server
import globalvars
from watchers.cpu import CPU
from watchers.disks import Disks
from watchers.memory import Memory
from watchers.net import Net
from watchers.temperature import Temperature
from watchers.up_time import UpTime
from websock import Websock

cost = 0

temp_sensor: Temperature
up_time: UpTime
cpu: CPU
memory: Memory
disk: Disks
net: Net
websock: Websock
isInited = False


async def main():
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)

    print(
        f"raspbarry-health-watcher version: {globalvars.version}\nby - davincif\ncheck me @ ldavincif.com\n"
    )

    validate_os()
    globalvars.set_globals()

    server = find_data_orchestrator_server()
    if server is None:
        raise Exception("health orchestrator server not found")

    print("server found at", server)

    watch(server)


def validate_os():
    if not (psutil.LINUX or psutil.POSIX):
        raise OSError("System not suported")


def watch(server: tuple[str, int]):
    global websock

    initial_time = time()
    init(server)
    initial_data_to_transfer = serialize_unmutables()
    # websock.send(initial_data_to_transfer.encode())

    if globalvars.verbose:
        print("started at", initial_time)

    while not globalvars.kill_now:
        start = perf_counter()

        update()
        data_to_transfer = serialize_update()
        # websock.send(data_to_transfer.encode())

        cost = perf_counter() - start
        ramining = globalvars.update_rate - cost

        if ramining > 0:
            if globalvars.verbose:
                print("measurement cost", cost, "\n")

            if not globalvars.kill_now:
                sleep(ramining)


def init(server: tuple[str, int]):
    global temp_sensor, up_time, cpu, memory, disk, net, websock, isInited

    temp_sensor = Temperature()
    up_time = UpTime()
    cpu = CPU()
    memory = Memory()
    disk = Disks()
    net = Net()
    websock = Websock(server)

    isInited = True


def update():
    global temp_sensor, up_time, cpu, memory, disk, net

    temp_sensor.update()
    up_time.update()
    cpu.update()
    memory.update()
    disk.update()
    net.update()

    if globalvars.verbose:
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
        "now": (perf_counter() - globalvars.server_now["counter"])
        + globalvars.server_now["now"],
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
        "now": (perf_counter() - globalvars.server_now["counter"])
        + globalvars.server_now["now"],
    }

    return json.dumps(data)


def exit_gracefully(signum: int, frame: FrameType | None):
    global websock

    print(f"singal {signal.Signals(signum).name} received, closing...")
    globalvars.kill_now = True
    if isInited:
        websock.close()


if __name__ == "__main__":
    asyncio.run(main())
