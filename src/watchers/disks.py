"""
TODO: this script used to watch all the disks in the PC individually, but I decided
that it would potencially lead to a security issue that I don't wanna deal with
right now.
"""

import psutil


from .helpers.disk import Disk


class Disks:
    total: float
    used: float
    free: float
    percent: float

    general: Disk
    # physicals: dict[str, Disk] = {}
    # physicals_name: set[str] = set()

    def __init__(self) -> None:
        usage = psutil.disk_usage("/")
        self.total = usage.total
        self.used = usage.used
        self.free = usage.free
        self.percent = usage.percent

        self.general = Disk(psutil.disk_io_counters())

    def update(self):
        self.general.update(psutil.disk_io_counters())

        # disks = psutil.disk_io_counters(perdisk=True)
        # for disk in disks:
        #     if disk in self.physicals:
        #         self.physicals[disk].update(disks[disk])
        #     else:
        #         self.physicals_name.add(disk)
        #         self.physicals[disk] = Disk(disks[disk])

        #     physicals_keys = set(self.physicals.keys())
        #     obsolete = self.physicals_name.difference(physicals_keys)
        #     self.physicals_name.difference_update(obsolete)
        #     for disk in obsolete:
        #         del self.physicals[disk]

    def __str__(self) -> str:
        return f"general {str(self.general)}"
