import json
import socket
from time import perf_counter, sleep

import globalvars


def find_data_orchestrator_server() -> tuple[str, int] | None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sleepTime = globalvars.update_rate * 4
    sock.settimeout(sleepTime)

    server_info: tuple[str, int] | None = None
    server_found = False
    data = b""
    addr = ""

    while not globalvars.kill_now and not server_found:
        try:
            print(
                f"broadcasting @ {("0.0.0.0", globalvars.AUTO_CONNECT_PORT)}. Wainting response..."
            )
            sock.sendto(
                __make_discovery_msg(), ("0.0.0.0", globalvars.AUTO_CONNECT_PORT)
            )

            # Aguarda resposta
            data, addr = sock.recvfrom(512)
            server_found = True
        except socket.timeout:
            print(f"[!] server not responding, trying again in {sleepTime}s...")
            sleep(sleepTime)

    if server_found:
        server_info = __handle_server_resp(data, addr)
    sock.close()

    return server_info


def __handle_server_resp(msg: bytes, addr: str):
    data = json.loads(msg.decode())
    globalvars.server_now = {"now": data["now"], "counter": perf_counter()}

    print("server answer")
    print("from", addr)
    print("data:", data)

    return (addr[0], data["port"])


def __make_discovery_msg() -> bytes:
    data = {"requester": socket.gethostname(), "request": "data-sender"}

    return json.dumps(data).encode()
