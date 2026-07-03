import psutil


class Net:

    def __init__(self) -> None:
        psutil.net_io_counters()
        psutil.net_io_counters(pernic=True)
