from typing import Any

import psutil

from watchers.helpers.cpu_core import CPUCore


class CPU:
    cores: int
    logical_cores: int

    usage_percet: float | None
    one_min_avg: float | None
    five_min_avg: float | None
    fifteen_min_avg: float | None

    core: CPUCore
    virtual_cores: list[CPUCore] = []

    def __init__(self):
        psutil.cpu_times()
        psutil.cpu_percent()

        self.logical_cores = psutil.cpu_count() or 0
        self.cores = psutil.cpu_count(logical=False) or 0

        self.core = CPUCore(psutil.cpu_freq())
        self.__build_cores()

    def update(self):
        self.core.update_time(
            psutil.cpu_times(), psutil.cpu_times_percent(), psutil.cpu_freq()
        )

        times = psutil.cpu_times(percpu=True)
        times_percent = psutil.cpu_times_percent(percpu=True)
        freqs = psutil.cpu_freq(percpu=True)

        for core_idx in range(len(self.virtual_cores)):
            core = self.virtual_cores[core_idx]
            core.update_time(times[core_idx], times_percent[core_idx], freqs[core_idx])

        self.usage_percet = psutil.cpu_percent()

        [
            self.one_min_avg,
            self.five_min_avg,
            self.fifteen_min_avg,
        ] = psutil.getloadavg()
        # [
        #     self.one_min_avg,
        #     self.five_min_avg,
        #     self.fifteen_min_avg,
        # ] = [x / float(self.logical_cores) * 100 for x in psutil.getloadavg()]

    def marshal_unmutables(self):
        data: Any = {
            "cr": self.cores,
            "lcr": self.logical_cores,
            **self.core.marshal_unmutables(),
        }

        if self.logical_cores > 0:
            data["lcrinfo"] = [core.marshal_unmutables() for core in self.virtual_cores]

        return data

    def marshal_update(self):
        data = {
            "load": self.usage_percet,
            "1min": self.one_min_avg,
            "5min": self.five_min_avg,
            "15min": self.fifteen_min_avg,
            **self.core.marshal_update(),
        }

        if self.logical_cores > 0:
            data["lcrinfo"] = [core.marshal_update() for core in self.virtual_cores]

        return data

    def __build_cores(self):
        freqs = psutil.cpu_freq(percpu=True)
        self.virtual_cores = [CPUCore(freqs[idx]) for idx in range(self.logical_cores)]

    def __str__(self) -> str:
        return f"cpu: {str(self.core)}"
        # return (f"cpu: {str(self.core)}\n"
        #         + str([f"core-{idx+1}: {str(self.virtual_cores[idx])}" for idx in range(len(self.virtual_cores))]))
