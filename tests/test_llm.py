import unittest
from unittest.mock import patch, MagicMock
from core.llm import LLMManager

class TestLLMManager(unittest.TestCase):
    def setUp(self):
        self.llm_manager = LLMManager()

    def test_classify_intent_general(self):
        # Should return False for casual talk
        self.assertFalse(self.llm_manager.classify_intent("Hello, how are you?"))

    def test_classify_intent_security_keyword(self):
        # Should return True because of "sql" and "error" keywords without needing LLM
        self.assertTrue(self.llm_manager.classify_intent("I have a SQL error in my query."))

    def test_get_active_system_message(self):
        sec_msg = self.llm_manager.get_active_system_message(True)
        gen_msg = self.llm_manager.get_active_system_message(False)
        self.assertIn("cybersecurity", sec_msg)
        self.assertIn("helpful AI assistant", gen_msg)

if __name__ == '__main__':
    unittest.main()
