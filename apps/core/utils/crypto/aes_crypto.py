import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import urlsafe_b64decode, urlsafe_b64encode
from config.components.base import SECRET_KEY


class AESCryptor:
    def __init__(self):
        self.__encryptKey = SECRET_KEY
        self.__key = hashlib.md5(self.__encryptKey.encode("utf8")).digest()
        self.__block_size = AES.block_size

    def encode(self, plaintext):
        """ AES encryption """
        iv = AES.new(self.__key, AES.MODE_CBC).iv
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext.encode("utf8"), self.__block_size))
        return urlsafe_b64encode(iv + ciphertext).decode("utf8").rstrip("=")

    def decode(self, ciphertext):
        """ AES decryption """
        ciphertext = urlsafe_b64decode(ciphertext + "=" * (4 - len(ciphertext) % 4))
        iv = ciphertext[:self.__block_size]
        ciphertext = ciphertext[self.__block_size:]
        cipher = AES.new(self.__key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), self.__block_size).decode("utf8")
