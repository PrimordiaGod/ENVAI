import unittest
from jarvis.modules.interaction_cli import CLIInteraction

class TestCLIInteraction(unittest.TestCase):
    def setUp(self):
        self.cli = CLIInteraction()

    def test_send_message(self):
        # Should return the message sent
        msg = "Hello, world!"
        result = self.cli.send_message(msg)
        self.assertEqual(result, msg)

    def test_get_user_input_exists(self):
        # Just check the method exists
        self.assertTrue(callable(getattr(self.cli, 'get_user_input', None)))

if __name__ == '__main__':
    unittest.main()