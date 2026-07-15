import threading
from time import sleep

from websockets import ConnectionClosedOK
from websockets.sync.client import connect

import globalvars


class Websock:
    uri: str
    queue: list[bytes] = []
    queue_lock = threading.Lock()
    thread: threading.Thread

    def __init__(self, server_info: tuple[str, int]):
        self.uri = f"ws://{server_info[0]}:{server_info[1]}"
        print("connecting to", self.uri)

        self.thread = threading.Thread(target=self.stream_info_sending)
        self.thread.start()

    def send(self, info: bytes):
        with self.queue_lock:
            self.queue.append(info)

    def stream_info_sending(self):
        retries = 0
        while not globalvars.kill_now and retries < globalvars.timeout_retries_attempt:
            try:
                self.__consume_queue()
                print("health streaming to server stoped.")
            except TimeoutError as error:
                retries += 1
                print("server not responding: timeout")
                print(error)
                print("trying again...")
            except ConnectionError as error:
                retries += 1
                print("server not responding: connection error")
                print(error)
                print("trying again...")
                sleep(2)
            except Exception as error:
                print(
                    "somewthing that the software don't know how to deal with went wrong:",
                    error,
                )
                globalvars.kill_now = True
            finally:
                if retries == globalvars.timeout_retries_attempt:
                    print("maximum retries reached, giving up connection.")
                    globalvars.kill_now = True

    def close(self):
        self.queue.clear()
        try:
            self.queue_lock.release()
        except Exception:
            pass

    def __consume_queue(self):
        with connect(self.uri) as websocket:
            print("connected!")
            while not globalvars.kill_now:
                if self.queue_lock.locked() or len(self.queue) == 0:
                    sleep(globalvars.update_rate)
                    continue

                with self.queue_lock:
                    if len(self.queue) == 0:
                        continue
                    data = self.queue.pop(0)

                try:
                    websocket.send(data)
                except ConnectionClosedOK as error:
                    print("connection has been closed:", error)
                    break
