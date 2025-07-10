from jarvis.interfaces.storage import SecureStorageInterface
from cryptography.fernet import Fernet
import os

class EncryptedStorage(SecureStorageInterface):
    KEY_FILE = 'storage.key'
    STORAGE_DIR = 'secure_data'

    def __init__(self):
        if not os.path.exists(self.STORAGE_DIR):
            os.makedirs(self.STORAGE_DIR)
        if not os.path.exists(self.KEY_FILE):
            key = Fernet.generate_key()
            with open(self.KEY_FILE, 'wb') as f:
                f.write(key)
        else:
            with open(self.KEY_FILE, 'rb') as f:
                key = f.read()
        self.fernet = Fernet(key)

    def store_data(self, key: str, data: bytes) -> None:
        enc = self.fernet.encrypt(data)
        with open(os.path.join(self.STORAGE_DIR, key), 'wb') as f:
            f.write(enc)

    def retrieve_data(self, key: str) -> bytes:
        try:
            with open(os.path.join(self.STORAGE_DIR, key), 'rb') as f:
                enc = f.read()
            return self.fernet.decrypt(enc)
        except FileNotFoundError:
            return b''

    def delete_data(self, key: str) -> None:
        try:
            os.remove(os.path.join(self.STORAGE_DIR, key))
        except FileNotFoundError:
            pass