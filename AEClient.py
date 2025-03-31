import logging
import base64
import os
from typing import Tuple

import msgpack
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

from pywebio.output import put_text
from names_generator import generate_name

from simple_client import SimpleClient

class AEClient(SimpleClient):
    def __init__(self, host: str, send_port: int, broadcast_port: int, nick: str, password: str):
        super().__init__(host, send_port, broadcast_port, nick)
        self.password = password
        self._log = logging.getLogger(f"AEClient[{nick.replace(' ', '_')}]")

    def derive_key_from_password(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC( #Fonction qui existe deja, pour appliquer Nitération de fois le SHA-256(ça hache ça hache)
            algorithm=hashes.SHA256(),
            length=32, #longueur standard pour AES-256.
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_message(self, password: str, message: str) -> Tuple[bytes, bytes]:
        salt = os.urandom(16)  # Génère un sel aléatoire pour chaque message
        key = self.derive_key_from_password(password, salt)  # Dérive une clé unique le salltt
        cipher = Fernet(key)  # Initialise le chiffreur (le Fernet)
        ciphertext = cipher.encrypt(message.encode())  # Chiffre le message
        return ciphertext, salt  # Retourne le message chiffré et le sel

    def decrypt_message(self, password: str, encrypted_message: bytes, salt: bytes, nick: str) -> str:
        # var nick is not used right now (further feature)
        key = self.derive_key_from_password(password, salt)
        cipher = Fernet(key)
        try:
            return cipher.decrypt(encrypted_message).decode()
        except Exception:
            return "[Message non lisible]"
        

    def send(self, frame: dict) -> dict:
  
        packed = msgpack.packb(frame, use_bin_type=True)
        response_packet = self._client.send(packed)   #Envoie du paquet
        unpacked = msgpack.unpackb(response_packet, raw=True)
        return {
            k.decode() if isinstance(k, bytes) else k: v.decode() if isinstance(v, bytes) else v #Décodage des clés
            for k, v in unpacked.items()
    }



    def message(self, message: str):
    # Comportement par défaut
        encrypted, salt = self.encrypt_message(self._password, message)
        frame = {"type": "message","nick": self._nick,"message": encrypted,"salt": salt,}
        response = self.send(frame)
    
        if response.get("response") != "ok":
            raise Exception("Message non envoyé")
    
    #Si la méthode n'est pas redéfinie dans une sous-classe on fait :
    raise NotImplementedError("La méthode 'message' doit être redéfinie dans une sous-classe.")


    def on_recv(self, packet: bytes):
        frame = msgpack.unpackb(packet, raw=False)
        if frame.get("type") == "message":
            decrypted = self.decrypt_message(self._password, frame["message"], frame["salt"], frame["nick"])
            put_text(f"{frame['nick']} : {decrypted}", scope='scrollable')

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    client = AEClient("localhost", 6666, 6667, generate_name(), "Best_Secr3t_ever_!")
    client.run()