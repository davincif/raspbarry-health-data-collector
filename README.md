# Raspbarry Health Data Collector

The script is meant to be used in a Raspbarry PI with **linux distribution**, preferebly the **Raspbarry PI OS**. If the not in a PI OS the temperature wacher will likely no work.

The system also works on a ThinkPad with linux system.

## run

```sh
pip install requeriments.txt
python3 main.py
```

## Docker

```sh
sudo docker build --network=host -t ldavincif/pi-health-watcher .
sudo docker run -d --name pi-health-watcher ldavincif/pi-health-watcher
```

For running the cointainer

```sh
PORT=7325 ADDR=192.168.1.153 sudo docker compose up -d
```

<!-- ERROR TO DEAL WITH -->
<!-- ⟩ server_address=192.168.1.66 python src/main.py
raspbarry-health-watcher version: 0.0.2
by - davincif
check me @ ldavincif.com

vendor is Vendor.THINKPAD
connecting to ws://192.168.1.66:7325
server not responding: connection error
[Errno 111] Connection refused
trying again...
server not responding: connection error
[Errno 111] Connection refused
trying again...
connected!
keepalive ping failed
Traceback (most recent call last):
  File "/home/davincif/Documents/Projects/pi-health-watcher/venv/lib/python3.12/site-packages/websockets/sync/connection.py", line 784, in keepalive
    with self.send_context():
  File "/usr/lib/python3.12/contextlib.py", line 137, in __enter__
    return next(self.gen)
           ^^^^^^^^^^^^^^
  File "/home/davincif/Documents/Projects/pi-health-watcher/venv/lib/python3.12/site-packages/websockets/sync/connection.py", line 1020, in send_context
    raise self.protocol.close_exc from original_exc
websockets.exceptions.ConnectionClosedError: received 1011 (internal error) keepalive ping timeout; then sent 1011 (internal error) keepalive ping timeout
somewthing that the software don't know how to deal with went wrong: received 1011 (internal error) keepalive ping timeout; then sent 1011 (internal error) keepalive ping timeout -->
