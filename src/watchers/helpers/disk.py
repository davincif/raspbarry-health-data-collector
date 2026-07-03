from typing import Any

import psutil


class Disk:
    read_bytes = 0
    write_bytes = 0
    read_bytes = 0
    write_bytes = 0
    read_time = 0
    write_time = 0
    busy_time = 0

    disk_io_start: Any

    def __init__(self, disk_io_start: Any) -> None:
        if disk_io_start is not None:
            self.disk_io_start = disk_io_start

    def update(self, disk_io: Any):
        # Calculate the difference (bytes transferred during the interval)
        if disk_io is None:
            self.__set_to_defaul_value()
        else:
            self.read_bytes = disk_io.read_bytes - self.disk_io_start.read_bytes
            self.write_bytes = disk_io.write_bytes - self.disk_io_start.write_bytes
            self.read_bytes = disk_io.read_bytes - self.disk_io_start.read_bytes
            self.write_bytes = disk_io.write_bytes - self.disk_io_start.write_bytes
            self.read_time = disk_io.read_time - self.disk_io_start.read_time
            self.write_time = disk_io.write_time - self.disk_io_start.write_time
            self.busy_time = disk_io.busy_time - self.disk_io_start.busy_time

        self.disk_io_start = disk_io

    def __set_to_defaul_value(self):
        self.read_bytes = 0
        self.write_bytes = 0
        self.read_bytes = 0
        self.write_bytes = 0
        self.read_time = 0
        self.write_time = 0
        self.busy_time = 0

    def __str__(self) -> str:
        return f"read_bytes: {self.read_bytes}, write_bytes: {self.write_bytes}, read_bytes: {self.read_bytes}, write_bytes: {self.write_bytes}, read_time: {self.read_time}, write_time: {self.write_time}, busy_time: {self.busy_time};"
