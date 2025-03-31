import msgpack
import logging
from simple_server import SimpleServer

class AEServer(SimpleServer):
    def __init__(self, recv_port: int, broadcast_port: int) -> None:
        super().__init__(recv_port, broadcast_port)
        self._serialize = msgpack.packb
        self._deserialize = msgpack.unpackb

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = AEServer(6666, 6667)
    try:
        while True:
            server.update()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
