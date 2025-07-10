import unittest
import os
from jarvis.modules.selfmod_sandbox import SandboxSelfMod

class TestSandboxSelfMod(unittest.TestCase):
    def setUp(self):
        self.mod = SandboxSelfMod()
        self.log_file = self.mod.LOG_FILE
        # Clean up before test
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def tearDown(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_logging(self):
        self.mod.propose_change('diff1')
        self.mod.apply_change('diff2')
        self.mod.rollback()
        with open(self.log_file, 'r') as f:
            logs = f.read()
        self.assertIn('PROPOSE: diff1', logs)
        self.assertIn('APPLY: diff2', logs)
        self.assertIn('ROLLBACK requested.', logs)

if __name__ == '__main__':
    unittest.main()