import threading
from time import sleep

from websockets.sync.client import connect

import globalvars


class Websock:
    uri: str
    queue: list[bytes] = []
    queue_lock = threading.Lock()
    thread: threading.Thread

    def __init__(self, server_info: tuple[str, int]):
        self.uri = f"ws://{server_info[0]}:{server_info[1]}"
        # self.thread = threading.Thread(target=self.stream_info_sending)
        # self.thread.start()

    def send(self, info: bytes):
        with self.queue_lock:
            self.queue.append(info)

    def stream_info_sending(self):
        with connect(self.uri) as websocket:
            while not globalvars.kill_now:
                if self.queue_lock.locked or len(self.queue) == 0:
                    sleep(globalvars.update_rate)
                    continue

                with self.queue_lock:
                    if len(self.queue) == 0:
                        continue
                    data = self.queue.pop(0)
                websocket.send(data)
        print("streaming health to server stoped.")

    def close(self):
        self.queue = []
        self.queue_lock.release()
