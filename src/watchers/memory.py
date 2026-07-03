from .helpers.swap_memory import SwapMemory

from .helpers.virtual_memory import VirtualMemory


class Memory:
    virtual = VirtualMemory()
    swap = SwapMemory()

    def update(self):
        self.virtual.update()
        self.swap.update()

    def marshal_unmutables(self):
        return {
            "v": self.virtual.marshal_unmutables(),
            "s": self.swap.marshal_unmutables(),
        }

    def marshal_update(self):
        return {
            "v": self.virtual.marshal_update(),
            "s": self.swap.marshal_update(),
        }

    def __str__(self) -> str:
        return f"virtual: {self.virtual}\nswap: {self.swap}"
