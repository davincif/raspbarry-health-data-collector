import psutil
from time import time

import globals


class UpTime:
    boot_time: float = 0

    uptime: float = 0
    """in seconds"""

    def __init__(self) -> None:
        self.boot_time = psutil.boot_time()

        if globals.verbose:
            print("boot_time", self.boot_time)

    def update(self):
        self.uptime = time() - self.boot_time

    def marshal_unmutables(self):
        return {"bt": self.boot_time}

    def marshal_update(self):
        return {"ut": self.uptime}

    def __str__(self) -> str:
        """Formatted String: "12h 34m 56s"""
        total_seconds = int(self.uptime)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f"{hours}h {minutes:02d}m {seconds:02d}s"
