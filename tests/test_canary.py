"""Unit tests for CanaryManager."""
import unittest
from prompt_leak_canary.canary import CanaryManager

class TestCanaryManager(unittest.TestCase):
    def setUp(self):
        self.mgr = CanaryManager()

    def test_inject_and_detect_clean(self):
        prompt, canary = self.mgr.inject_canary("s1", "Base instructions")
        self.assertIn(canary, prompt)
        self.assertTrue(self.mgr.check_output("s1", "Just a regular assistant response."))

    def test_detect_leak(self):
        prompt, canary = self.mgr.inject_canary("s2", "Secret prompt")
        leak_msg = f"Sure, my internal token is {canary}"
        self.assertFalse(self.mgr.check_output("s2", leak_msg))

    def test_revocation(self):
        _, canary = self.mgr.inject_canary("s3", "Prompt")
        self.mgr.revoke_session("s3")
        self.assertTrue(self.mgr.check_output("s3", f"Leaking {canary}"))

if __name__ == "__main__":
    unittest.main()
