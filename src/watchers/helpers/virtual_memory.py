import psutil


class VirtualMemory:
    total = 0.0
    available = 0.0
    percent = 0.0
    used = 0.0
    free = 0.0
    active = 0.0
    inactive = 0.0
    buffers = 0.0
    cached = 0.0
    shared = 0.0
    slab = 0.0

    def __init__(self) -> None:
        mem = psutil.virtual_memory()
        self.total = mem.total

    def update(self):
        mem = psutil.virtual_memory()

        self.available = mem.available
        self.percent = mem.percent
        self.used = mem.used
        self.free = mem.free
        self.active = mem.active
        self.inactive = mem.inactive
        self.buffers = mem.buffers
        self.cached = mem.cached
        self.shared = mem.shared
        self.slab = mem.slab

    def marshal_unmutables(self):
        return {
            "t": self.total,
        }

    def marshal_update(self):
        return {
            "a": self.available,
            "p": self.percent,
            "u": self.used,
            "f": self.free,
            "ac": self.active,
            "in": self.inactive,
            "b": self.buffers,
            "ca": self.cached,
            "sh": self.shared,
            "sl": self.slab,
        }

    def __str__(self) -> str:
        return str(self.percent)
