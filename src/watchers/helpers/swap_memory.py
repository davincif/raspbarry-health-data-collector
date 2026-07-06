import psutil


class SwapMemory:
    total = 0.0
    used = 0.0
    free = 0.0
    percent = 0.0
    sin = 0.0
    sout = 0.0

    def __init__(self) -> None:
        mem = psutil.swap_memory()
        self.total = mem.total

    def update(self):
        mem = psutil.swap_memory()

        self.used = mem.used
        self.free = mem.free
        self.percent = mem.percent
        self.sin = mem.sin
        self.sout = mem.sout

    def marshal_unmutables(self):
        return {
            "t": self.total,
        }

    def marshal_update(self):
        return {
            "u": self.used,
            "f": self.free,
            "p": self.percent,
            "si": self.sin,
            "so": self.sout,
        }

    def __str__(self) -> str:
        return str(self.used)
