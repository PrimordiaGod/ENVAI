import unittest
from jarvis.modules.context_memory import MemoryContextEngine

class TestMemoryContextEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MemoryContextEngine()
        self.user_id = 'test_user'

    def test_store_and_retrieve_context(self):
        ctx = {'foo': 'bar'}
        self.engine.store_context(self.user_id, ctx)
        retrieved = self.engine.retrieve_context(self.user_id)
        self.assertEqual(retrieved, ctx)

    def test_clear_context(self):
        ctx = {'foo': 'bar'}
        self.engine.store_context(self.user_id, ctx)
        self.engine.clear_context(self.user_id)
        self.assertEqual(self.engine.retrieve_context(self.user_id), {})

if __name__ == '__main__':
    unittest.main()