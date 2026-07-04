from typing import Any

import psutil

from models.temperature_info import TemperatureInfo, empty_temperature_info
from models.vendor import Vendor
import globalvars


class Temperature:
    cpu = empty_temperature_info()
    gpu = empty_temperature_info()

    def update(self):
        if globalvars.vendor == Vendor.UNKNOWN:
            return

        if globalvars.vendor == Vendor.RASBPARRY_PI:
            self.update_raspberrypi()
        elif globalvars.vendor == Vendor.THINKPAD:
            self.update_thinkpad()

    def update_raspberrypi(self):
        tempData = psutil.sensors_temperatures()

        cpu_thermal = tempData["cpu_thermal"][0]
        print("cpu_thermal", cpu_thermal)
        self.__set_info(self.cpu, cpu_thermal)

    def update_thinkpad(self):
        tempData = psutil.sensors_temperatures()

        thinkpad_thermal = tempData["thinkpad"]
        cpu_thermal = next(
            (info for info in thinkpad_thermal if info.label.upper() == "CPU"),
            None,
        )
        gpu_thermal = next(
            (info for info in thinkpad_thermal if info.label.upper() == "GPU"),
            None,
        )

        if cpu_thermal is not None:
            self.__set_info(self.cpu, cpu_thermal)

        if gpu_thermal is not None:
            self.__set_info(self.gpu, gpu_thermal)

    def __set_info(self, at: TemperatureInfo, info: Any):
        at["label"] = info.label
        at["current"] = info.current
        at["high"] = info.high
        at["critical"] = info.critical

    def marshal_unmutables(self):
        return {}

    def marshal_update(self):
        return {
            "cpu": self.cpu,
            "gpu": self.gpu,
        }

    def __str__(self) -> str:
        return f"{self.cpu}\n{self.gpu}"
