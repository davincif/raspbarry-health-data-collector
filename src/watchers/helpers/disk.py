from typing import Any


class Disk:
    read_count: int
    write_count: int
    read_bytes: int
    write_bytes: int
    read_time: int
    write_time: int
    busy_time: int

    def __init__(self, disk_io_start: Any) -> None:
        self.update(disk_io_start)

    def update(self, disk_io: Any):
        # Calculate the difference (bytes transferred during the interval)
        if disk_io is None:
            self.__set_to_zero()
        else:
            self.__update_values(disk_io or 0)

    def __update_values(self, disk_io: Any):
        self.read_count = disk_io.read_count
        self.write_count = disk_io.write_count
        self.read_bytes = disk_io.read_bytes
        self.write_bytes = disk_io.write_bytes
        self.read_time = disk_io.read_time
        self.write_time = disk_io.write_time
        self.busy_time = getattr(disk_io, "busy_time", 0)

    def __set_to_zero(self):
        self.read_count = 0
        self.write_count = 0
        self.read_bytes = 0
        self.write_bytes = 0
        self.read_time = 0
        self.write_time = 0
        self.busy_time = 0

    def marshal_update(self):
        return {
            "rc": self.read_count,
            "wc": self.write_count,
            "rb": self.read_bytes,
            "wb": self.write_bytes,
            "rt": self.read_time,
            "wt": self.write_time,
            "bt": self.busy_time,
        }

    def __str__(self) -> str:
        return f"read_bytes: {self.read_count}, write_bytes: {self.write_count}, read_bytes: {self.read_bytes}, write_bytes: {self.write_bytes}, read_time: {self.read_time}, write_time: {self.write_time}, busy_time: {self.busy_time};"
