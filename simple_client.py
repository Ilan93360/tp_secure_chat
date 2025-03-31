
import logging
import pickle
import threading
import time


from names_generator import generate_name
from pywebio.pin import put_input, pin_update, pin
from pywebio.output import put_button, put_row, put_scrollable, put_text, put_scope
from pywebio.session import register_thread
from pywebio.session import defer_call

from base_client import BaseClient


class SimpleClient:
    def __init__(self, host: str, send_port: int, broadcast_port: int, nick: str):
        self._client = BaseClient(host, send_port, broadcast_port)
        self._log = logging.getLogger(f"SimpleClient[{nick}]")
        self._nick = nick
        self._running = True

    def send(self, frame:dict)->dict:
        packet = pickle.dumps(frame)
        response_packet = self._client.send(packet)
        if response_packet:
            return pickle.loads(response_packet)
        
    def start_server(self):
        
        def _inner():
            put_scrollable(put_scope('scrollable'), height=500, keep_bottom=True)
            put_row([
                put_text(self._nick),
                put_input('message_input', placeholder='Your message'),
                put_button("send", self._on_send )
            ])

        t = threading.Thread(target=_inner)
        register_thread(t)
        defer_call(self.defer_callback)
        t.start()


    def _on_send(self):
        # called when the button send is hit
        self._log.debug("send callback")
        message = pin['message_input']
        if message:
            self._log.debug("message : "+message)
            self.message(message)
            pin_update('message_input', value='')
        
    def join(self):
        frame = {"type":"join", "nick":self._nick}
        response = self.send(frame)
        if response["response"] != "ok":
            raise Exception("Failed to join")
        
    def leave(self):
        frame = {"type": "leave", "nick": self._nick}
        response = self.send(frame)
        if response["response"] != "ok":
            raise Exception("Failed to leave")
        
    def message(self, message:str):
        frame = {"type": "message", "nick": self._nick, "message":message}
        response = self.send(frame)
        if response["response"] != "ok":
            raise Exception("Failed to send message")
        
    def on_recv(self, packet: bytes):
        frame = msgpack.unpackb(packet, raw=False)
        if frame.get("type") == "message":
        # Si le champ 'message' ou 'salt' n'est pas présent, on traite cela comme une erreur
            message = frame.get("message")
            salt = frame.get("salt")

            if not message or not salt:
                self._log.error(f"Message ou salt manquants dans le paquet de {frame['nick']}")
                return
        
            decrypted = self.decrypt_message(self._password, message, salt, frame["nick"])
            put_text(f"{frame['nick']} : {decrypted}", scope='scrollable')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = SimpleClient("localhost", 6666, 6667, generate_name())
    client.run()
