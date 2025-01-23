import base64
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


class RSACryptor:
    def __init__(self, bits=2048):
        self.key = RSA.generate(bits)
        self.private_key = self.key.export_key()
        self.public_key = self.key.publickey().export_key()

    def encrypt_rsa(self, plain_text, public_key):
        rsakey = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsakey)
        encrypted_text = cipher.encrypt(plain_text.encode())
        return base64.b64encode(encrypted_text).decode()

    def decrypt_rsa(self, encrypted_text, private_key):
        rsakey = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsakey)
        decoded_data = base64.b64decode(encrypted_text.encode())
        decrypted_text = cipher.decrypt(decoded_data).decode()
        return decrypted_text
