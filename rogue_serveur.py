import msgpack
import logging
from base_server import BaseServer

class RogueServer:
    def __init__(self, recv_port: int, broadcast_port: int):
        self._server = BaseServer(recv_port, broadcast_port)
        self._log = logging.getLogger("RogueServer")

    def on_recv(self, packet: bytes):
        try:
            frame = msgpack.unpackb(packet, raw=False)

            if frame.get("type") == "message":
                original_message = frame["message"]
                self._log.info(f"[ROGUE] Message intercepté : {original_message}")

                frame["message"] = "### MODIFIÉ PAR ROGUE ###"
                self._log.info(f"[ROGUE] Message modifié : {frame['message']}")

                packet = msgpack.packb(frame, use_bin_type=True)
                return packet, msgpack.packb({"response": "ok"}, use_bin_type=True)

            return None, msgpack.packb({"response": "ok"}, use_bin_type=True)

        except Exception as e:
            self._log.error(f"[ROGUE ERROR] {e}")
            return None, msgpack.packb({"response": "ko"}, use_bin_type=True)

    def run(self):
        try:
            while True:
                self._server.update(self.on_recv)
        except KeyboardInterrupt:
            self._log.info("[ROGUE] Arrêt du serveur.")
            self._server.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    server = RogueServer(6666, 6667)
    server.run()
