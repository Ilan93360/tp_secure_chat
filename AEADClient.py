from AEClient import AEClient

class AEADClient(AEClient):
    def encrypt_message(self, password: str, message: str) -> tuple[bytes, bytes]:
        message_tagged = f"[{self._nick}] {message}"
        return super().encrypt_message(password, message_tagged)
    
    def decrypt_message(self, password: str, encrypted_message: bytes, salt: bytes, nick: str) -> str:
        decrypted_text = super().decrypt_message(password, encrypted_message, salt, nick)

        prefix_expected = f"[{nick}] "
        if not decrypted_text.startswith(prefix_expected):
            return "[AEAD ALERT: Message corrompu]"

        return decrypted_text[len(prefix_expected):]  

if __name__ == "__main__":
    import logging
    from names_generator import generate_name

    logging.basicConfig(level=logging.DEBUG)
    client = AEADClient("localhost", 6666, 6667, generate_name(), "Best_Secr3t_ever_!")
    client.run()