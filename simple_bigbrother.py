
"""""
import socket

HOST = "127.0.0.1"  # Adresse du serveur
PORT = 12345        # Port du serveur

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("[*] Connecté en tant qu'espion.")

    while True:
        try:
            data = s.recv(1024)
            if not data:
                break
            print(f"[BIGBROTHER] Reçu: {data.decode().strip()}")
        except Exception as e:
            print(f"[!] Erreur: {e}")
            break
"""""

import logging
import pickle
from base_client import BaseClient

class SimpleBigBrother:
    def __init__(self, host: str, broadcast_port: int):
        self._client = BaseClient(host, 0, broadcast_port) 
        self.log = logging.getLogger(self.__class__.__name__)
        self._clients = set()
        self._serial_function = pickle.dumps
        self._deserial_function = pickle.loads

    def on_recv(self, packet: bytes):
        try:
            frame = pickle.loads(packet)
            if frame["type"] == "message":
                self.log.info(f"{frame['nick']} : {frame['message']}")
        except Exception as e:
            self.log.error(f"Error processing packet: {e}")

    def run(self):
        while True:
            self._client.update(self.on_recv)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    big_brother = SimpleBigBrother("localhost", 6667)
    big_brother.run()