import psutil


class Net:
    bytes_sent = 0
    bytes_recv = 0
    packets_sent = 0
    packets_recv = 0
    errin = 0
    errout = 0
    dropin = 0
    dropout = 0

    def __init__(self) -> None:
        self.update()

    def update(self):
        net = psutil.net_io_counters()

        self.bytes_sent = net.bytes_sent
        self.bytes_recv = net.bytes_recv
        self.packets_sent = net.packets_sent
        self.packets_recv = net.packets_recv
        self.errin = net.errin
        self.errout = net.errout
        self.dropin = net.dropin
        self.dropout = net.dropout

    def __str__(self) -> str:
        return f"bytes_sent: {self.bytes_sent}, bytes_recv: {self.bytes_recv}, packets_sent: {self.packets_sent}, packets_recv: {self.packets_recv}, errin: {self.errin}, errout: {self.errout}, dropin: {self.dropin}, dropout: {self.dropout};"
