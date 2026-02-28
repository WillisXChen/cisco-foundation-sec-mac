import unittest
from unittest.mock import patch, MagicMock
from core.database import VectorDBManager

class TestVectorDBManager(unittest.TestCase):
    @patch('core.database.QdrantClient')
    def test_query_context(self, mock_qdrant_client_cls):
        # Setup mock QdrantClient
        mock_client = MagicMock()
        mock_qdrant_client_cls.return_value = mock_client
        
        # Setup mock search result
        mock_result = MagicMock()
        mock_result.document = "Playbook content on how to handle SQL injection."
        mock_result.metadata = {"title": "SQLi Handling"}
        mock_result.score = 0.95
        
        mock_client.query.return_value = [mock_result]
        
        # Initialize and test
        manager = VectorDBManager()
        context = manager.query_context("How do I fix SQL injection?")
        
        self.assertTrue(mock_client.query.called)
        self.assertIn("Internal System Context", context)
        self.assertIn("SQL injection", context)
        
    @patch('core.database.QdrantClient')
    def test_query_context_no_result(self, mock_qdrant_client_cls):
        mock_client = MagicMock()
        mock_qdrant_client_cls.return_value = mock_client
        mock_client.query.return_value = []
        
        manager = VectorDBManager()
        context = manager.query_context("Random question")
        
        self.assertEqual(context, "")

if __name__ == '__main__':
    unittest.main()
