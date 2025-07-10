import unittest
import os
from jarvis.modules.storage_encrypted import EncryptedStorage

class TestEncryptedStorage(unittest.TestCase):
    def setUp(self):
        self.storage = EncryptedStorage()
        self.key = 'testfile'
        self.data = b'secret data'
        # Clean up before test
        path = os.path.join(self.storage.STORAGE_DIR, self.key)
        if os.path.exists(path):
            os.remove(path)

    def tearDown(self):
        path = os.path.join(self.storage.STORAGE_DIR, self.key)
        if os.path.exists(path):
            os.remove(path)

    def test_store_and_retrieve(self):
        self.storage.store_data(self.key, self.data)
        retrieved = self.storage.retrieve_data(self.key)
        self.assertEqual(retrieved, self.data)

    def test_delete(self):
        self.storage.store_data(self.key, self.data)
        self.storage.delete_data(self.key)
        self.assertEqual(self.storage.retrieve_data(self.key), b'')

if __name__ == '__main__':
    unittest.main()