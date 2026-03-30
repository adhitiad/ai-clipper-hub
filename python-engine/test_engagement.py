import unittest
import sys
from unittest.mock import patch, MagicMock

# Mock database module before importing engagement to avoid Pinecone initialization
sys.modules['database'] = MagicMock()

from pymongo import UpdateOne
import engagement

class TestEngagement(unittest.TestCase):
    def test_reply_to_new_comments(self):
        # Setup mocks
        mock_db = MagicMock()
        engagement.db = mock_db

        mock_llm = MagicMock()

        mock_db.published_clips.find.return_value.sort.return_value.limit.return_value = [
            {"niche": "niche_1"}
        ]

        def mock_find(query):
            mock_cursor = MagicMock()
            mock_cursor.limit.return_value = [
                {"_id": "comment_1", "text": "Hello", "niche": "niche_1"},
                {"_id": "comment_2", "text": "World", "niche": "niche_1"}
            ]
            return mock_cursor

        mock_db.raw_comments.find.side_effect = mock_find

        mock_llm.batch.return_value = [
            MagicMock(content="Reply 1"),
            MagicMock(content="Reply 2")
        ]

        with patch('engagement.ChatGroq', return_value=mock_llm):
            # Execute
            engagement.reply_to_new_comments()

            # Assertions
            mock_llm.batch.assert_called_once()
            prompts = mock_llm.batch.call_args[0][0]
            self.assertEqual(len(prompts), 2)
            self.assertIn("Hello", prompts[0])
            self.assertIn("World", prompts[1])

            mock_db.raw_comments.bulk_write.assert_called_once()
            operations = mock_db.raw_comments.bulk_write.call_args[0][0]
            self.assertEqual(len(operations), 2)
            self.assertIsInstance(operations[0], UpdateOne)
            self.assertEqual(operations[0]._filter, {"_id": "comment_1"})
            self.assertEqual(operations[0]._doc, {"$set": {"replied": True, "reply_text": "Reply 1"}})

if __name__ == '__main__':
    unittest.main()
