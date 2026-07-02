from typing import Any


class CPUCore:
    current_freq: float
    max_freq: float
    min_freq: float

    user: float | None
    system: float | None
    idle: float | None
    nice: float | None
    iowait: float | None

    user_percent: float | None
    system_percent: float | None
    idle_percent: float | None
    nice_percent: float | None
    iowait_percent: float | None

    def __init__(self, freq: Any) -> None:
        self.current_freq = freq.current
        self.min_freq = freq.min
        self.max_freq = freq.max

    def update_time(self, times: Any, times_percent: Any, freq: Any) -> None:
        self.user = times.user
        self.system = times.system
        self.idle = times.idle
        self.nice = times.nice
        self.iowait = times.iowait

        self.user_percent = times_percent.user
        self.system_percent = times_percent.system
        self.idle_percent = times_percent.idle
        self.nice_percent = times_percent.nice
        self.iowait_percent = times_percent.iowait

        self.current_freq = freq.current
        self.min_freq = freq.min
        self.max_freq = freq.max

    def __str__(self) -> str:
        return (
            f"max_freq: {self.max_freq}; min_freq: {self.min_freq};\n"
            + f"user: {self.user}; system: {self.system}; idle: {self.idle}; nice: {self.nice}; iowait: {self.iowait};\n"
            + f"user_percent: {self.user_percent}; system_percent: {self.system_percent}; idle_percent: {self.idle_percent}; nice_percent: {self.nice_percent}; iowait_percent: {self.iowait_percent};"
        )
