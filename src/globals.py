import psutil
from models.vendor import Vendor

vendor = Vendor.UNKNOWN
update_rate = 0.9
version = "0.0.1"
verbose = False


def set_globals():
    __define_os()


def __define_os():
    global vendor

    tempData = psutil.sensors_temperatures()

    if "cpu_thermal" in tempData:
        vendor = Vendor.RASBPARRY_PI
    elif "thinkpad" in tempData:
        vendor = Vendor.THINKPAD
    else:
        vendor = Vendor.UNKNOWN
        raise OSError("System not suported")

    print("vendor is", vendor)
